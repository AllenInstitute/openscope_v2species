# -*- coding: utf-8 -*-
# Stimulus design
#
# The experiment consists of two phases in which different sets of 30 sec long natural movies will be presented:
#   - Phase 1 consists of two natural movies (i.e., movie01 and movie02) and a constant gray screen (i.e., movie00).
#   - Phase 2 consists of 50 natural movies (i.e., movie03-movie52) and a constant gray screen (i.e., movie00).
#
# Animals are assigned into two groups (A and B), each presented with the movies in different order.
# In both groups, a total of 230 movies will be presented for a total time of 115 min:
#   1. For group A:
#           - Phase 1:
#               - 50 presentations of movie01 (25 min)
#               - 10 presentations of movie00 (5 min)
#               - 50 alternations between movie01 and movie02 (25 min)
#               - 10 presentations of movie00 (5 min)
#
#           - Phase 2:
#               - 20 presentations of movie03 (10 min)
#               - 10 presentations of movie00 (5 min)
#               - 50 sequential presentations of movie03 to movie52 (25 min)
#               - 10 presentations of movie00 (5 min)
#               - 20 alternations between movie03 and movie52 (10 min)
#
#   2. For group B:
#           - Phase 1:
#               - 50 alternations between movie01 and movie02 (25 min)
#               - 10 presentations of movie00 (5 min)
#               - 50 presentations of movie01 (25 min)
#               - 10 presentations of movie00 (5 min)
#
#           - Phase 2:
#               - 20 presentations of movie03 (10 min)
#               - 10 presentations of movie00 (5 min)
#               - 50 presentations of movie52 (25 min)
#               - 10 presentations of movie00 (5 min)
#               - 20 alternations between movie03 and movie52 (10 min)
import psychopy.visual
import camstim
import argparse
import numpy as np
from psychopy import monitors
from camstim import SweepStim, Foraging, Window, Warp, MovieStim
import glob
import logging
import yaml
import os

import datetime
import pickle as pkl
from copy import deepcopy

def run_optotagging(levels, conditions, waveforms, isis, sampleRate = 10000.):

    from toolbox.IO.nidaq import AnalogOutput
    from toolbox.IO.nidaq import DigitalOutput

    sweep_on = np.array([0,0,1,0,0,0,0,0], dtype=np.uint8)
    stim_on = np.array([0,0,1,1,0,0,0,0], dtype=np.uint8)
    stim_off = np.array([0,0,1,0,0,0,0,0], dtype=np.uint8)
    sweep_off = np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

    ao = AnalogOutput('Dev1', channels=[1])
    ao.cfg_sample_clock(sampleRate)

    do = DigitalOutput('Dev1', 2)

    do.start()
    ao.start()

    do.write(sweep_on)
    time.sleep(5)

    for i, level in enumerate(levels):

        print(level)

        data = waveforms[conditions[i]]

        do.write(stim_on)
        ao.write(data * level)
        do.write(stim_off)
        time.sleep(isis[i])

    do.write(sweep_off)
    do.clear()
    ao.clear()

def generatePulseTrain(pulseWidth, pulseInterval, numRepeats, riseTime, sampleRate = 10000.):

    data = np.zeros((int(sampleRate),), dtype=np.float64)
   # rise_samples =

    rise_and_fall = (((1 - np.cos(np.arange(sampleRate*riseTime/1000., dtype=np.float64)*2*np.pi/10))+1)-1)/2
    half_length = int(rise_and_fall.size / 2)
    rise = rise_and_fall[:half_length]
    fall = rise_and_fall[half_length:]

    peak_samples = int(sampleRate*(pulseWidth-riseTime*2)/1000)
    peak = np.ones((peak_samples,))

    pulse = np.concatenate((rise, \
                           peak, \
                           fall))

    interval = int(pulseInterval*sampleRate/1000.)

    for i in range(0, numRepeats):
        data[i*interval:i*interval+pulse.size] = pulse

    return data

def optotagging(mouse_id, operation_mode='experiment', level_list = [1.15, 1.28, 1.345], output_dir = 'C:/ProgramData/camstim/output/'):

    sampleRate = 10000

    # 1 s cosine ramp:
    data_cosine = (((1 - np.cos(np.arange(sampleRate, dtype=np.float64)
                                * 2*np.pi/sampleRate)) + 1) - 1)/2  # create raised cosine waveform

    # 1 ms cosine ramp:
    rise_and_fall = (
        ((1 - np.cos(np.arange(sampleRate*0.001, dtype=np.float64)*2*np.pi/10))+1)-1)/2
    half_length = int(rise_and_fall.size / 2)

    # pulses with cosine ramp:
    pulse_2ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.001),)), rise_and_fall[half_length:]))
    pulse_5ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.004),)), rise_and_fall[half_length:]))
    pulse_10ms = np.concatenate((rise_and_fall[:half_length], np.ones(
        (int(sampleRate*0.009),)), rise_and_fall[half_length:]))

    data_2ms_10Hz = np.zeros((sampleRate,), dtype=np.float64)

    for i in range(0, 10):
        interval = int(sampleRate / 10)
        data_2ms_10Hz[i*interval:i*interval+pulse_2ms.size] = pulse_2ms

    data_5ms = np.zeros((sampleRate,), dtype=np.float64)
    data_5ms[:pulse_5ms.size] = pulse_5ms

    data_10ms = np.zeros((sampleRate,), dtype=np.float64)
    data_10ms[:pulse_10ms.size] = pulse_10ms

    data_10s = np.zeros((sampleRate*10,), dtype=np.float64)
    data_10s[:-2] = 1

    ##### THESE STIMULI ADDED FOR OPENSCOPE GLO PROJECT #####
    data_10ms_5Hz = generatePulseTrain(10, 200, 5, 1) # 1 second of 5Hz pulse train. Each pulse is 10 ms wide
    data_6ms_40Hz = generatePulseTrain(6, 25, 40, 1)  # 1 second of 40 Hz pulse train. Each pulse is 6 ms wide
    #########################################################

    # for experiment

    isi = 1.5
    isi_rand = 0.5
    numRepeats = 50

    condition_list = [3, 4, 5]
    waveforms = [data_2ms_10Hz, data_5ms, data_10ms, data_cosine, data_10ms_5Hz, data_6ms_40Hz]

    opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
    opto_conditions = condition_list*numRepeats*len(level_list)
    opto_conditions = np.sort(opto_conditions)
    opto_isis = np.random.random(opto_levels.shape) * isi_rand + isi

    p = np.random.permutation(len(opto_levels))

    # implement shuffle?
    opto_levels = opto_levels[p]
    opto_conditions = opto_conditions[p]

    # for testing

    if operation_mode=='test_levels':
        isi = 2.0
        isi_rand = 0.0

        numRepeats = 2

        condition_list = [0]
        waveforms = [data_10s, data_10s]

        opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
        opto_conditions = condition_list*numRepeats*len(level_list)
        opto_conditions = np.sort(opto_conditions)
        opto_isis = np.random.random(opto_levels.shape) * isi_rand + isi

    elif operation_mode=='pretest':
        numRepeats = 1

        condition_list = [0]
        data_2s = data_10s[-sampleRate*2:]
        waveforms = [data_2s]

        opto_levels = np.array(level_list*numRepeats*len(condition_list)) #     BLUE
        opto_conditions = condition_list*numRepeats*len(level_list)
        opto_conditions = np.sort(opto_conditions)
        opto_isis = [1]*len(opto_conditions)
    #

    outputDirectory = output_dir
    fileDate = str(datetime.datetime.now()).replace(':', '').replace(
        '.', '').replace('-', '').replace(' ', '')[2:14]
    fileName = os.path.join(outputDirectory, fileDate + '_'+mouse_id + '.opto.pkl')

    print('saving info to: ' + fileName)
    fl = open(fileName, 'wb')
    output = {}

    output['opto_levels'] = opto_levels
    output['opto_conditions'] = opto_conditions
    output['opto_ISIs'] = opto_isis
    output['opto_waveforms'] = waveforms

    pkl.dump(output, fl)
    fl.close()
    print('saved.')

    #
    run_optotagging(opto_levels, opto_conditions,
                    waveforms, opto_isis, float(sampleRate))
"""
end of optotagging section
"""

def make_movie_stimulus(movie_paths, order, window):
    """Generate a Stimulus that plays a series of movie clips in a specified order."""

    # Convert the order into a list of display sequence tuples. There should be one display sequence list per movie
    # clip. Each display sequence list contains a set of tuples of the form (start_second, stop_second). Theses tuples
    # define the start and stop time for when to play the clip and are determined by the order vector
    movie_length = 30   # in seconds
    frame_rate = 30.0

    all_starts = np.arange(0, movie_length * len(order), movie_length).astype(float)
    display_sequences = []
    for i in np.unique(order):
        display_sequences.append(list(zip(all_starts[order == i], all_starts[order == i] + movie_length)))

    # Load each movie clip into its own MovieStim object. The display sequence will be set later so the clips play
    # in the correct order.
    stims = []
    unique_movies = np.unique(order)
    num_movies = len(unique_movies)
    for i in range(num_movies):
        current_movie_id = unique_movies[i]
        # If the order index is less than the number of movie clips, load the movie clip.
        if i < len(movie_paths):

            # The movie clips should be 30 seconds long and should be played at 30 fps.
            s = MovieStim(movie_path=movie_paths[current_movie_id],
                          window=window,
                          frame_length=1.0 / frame_rate,
                          size=(1920, 1080),
                          start_time=0.0,
                          stop_time=None,
                          flip_v=True, runs=len(display_sequences[i]))
            s.set_display_sequence(display_sequences[i])

        else:
            raise ValueError("Order index is greater than the number of movie clips.")

        stims.append(s)

    stim = SweepStim(window,
                     stimuli=stims,
                     # pre_blank_sec=1,
                     # post_blank_sec=1,
                     params={},
                     )

    return stim


if __name__ == "__main__":
    parser = argparse.ArgumentParser("mtrain")
    parser.add_argument("json_path", nargs="?", type=str, default="")

    args, _ = parser.parse_known_args() # <- this ensures that we ignore other arguments that might be needed by camstim
    
    # print args
    if args.json_path == "":
        logging.warning("No json path provided, using default parameters. THIS IS NOT THE EXPECTED BEHAVIOR FOR PRODUCTION RUNS")
        json_params = {}
    else:
        with open(args.json_path, 'r') as f:
            # we use the yaml package here because the json package loads as unicode, which prevents using the keys as parameters later
            json_params = yaml.load(f)
            logging.info("Loaded json parameters from mtrain")
            # end of mtrain part

    data_folder = json_params.get('data_folder', os.path.abspath("data"))
    
    # An integer representing the experiment group. Defaults to test group (value of 2).
    group = json_params.get('stimulus_orderings', 'movie_order_groupTEST')
    
    opto_disabled = json_params.get('disable_opto', True)
    dev_mode = json_params.get("dev_mode", True)

    # Paths to the movie clip files to load.
    movie_clip_files = glob.glob(os.path.join(data_folder, 'full_movies','*.npy'))

    # Load the movie clip order for each experimental group as provided by the Ziv lab:
    order = (np.loadtxt(os.path.join(data_folder, 'stimulus_orderings', group+".txt")).astype(int))

    dist = 15.0
    wid = 52.0

    # create a monitor
    if dev_mode:
        monitor = monitors.Monitor('testMonitor', distance=dist, width=wid)
    else:
        monitor = "Gamma1.Luminance50"

    # Create display window
    window = Window(fullscr=True,   # Will return an error due to default size. Ignore.
                    monitor=monitor,  # Will be set to a gamma calibrated profile by MPE
                    screen=0,
                    warp=Warp.Spherical
                    )

    ss = make_movie_stimulus(movie_clip_files, order, window)
    
    # add in foraging so we can track wheel, potentially give rewards, etc
    f = Foraging(window = window,
                    auto_update = False,
                    params= {}
                    )
    
    ss.add_item(f, "foraging")

    # run it
    try:
        ss.run()
    except SystemExit:
        print("We prevent camstim exiting the script to complete optotagging")

    if not(opto_disabled):
        from camstim.misc import get_config
        from camstim.zro import agent
        opto_params = deepcopy(json_params.get("opto_params"))
        opto_params["mouse_id"] = json_params["mouse_id"]
        opto_params["output_dir"] = agent.OUTPUT_DIR

        #Read opto levels from ZooKeeper
        opto_params["level_list"] = get_config('Optogenetics')["level_list"]

        optotagging(**opto_params)