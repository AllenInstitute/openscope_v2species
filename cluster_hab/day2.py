"""
Habituation Day 2.

Total: 1175 seconds = 19.6 min

"""
import os
from psychopy import visual
from camstim import Stimulus, SweepStim, MovieStim, NaturalScenes
from camstim import Foraging
from camstim import Window, Warp

# Create display window
window = visual.Window(fullscr=True,
                monitor='Gamma1.Luminance50',
                screen=0,
                #warp=Warp.Spherical,
                )

############ Stimulus definitions #############################################

# Locally Sparse Noise
lsn8_path = r"//allen/aibs/mat/michaelbu/Locally_Sparse_Noise_Trimmed/short/lsn_mat_8x14_short.npy"

lsn8 = MovieStim(movie_path=lsn8_path,
                window=window,
                frame_length=0.25,
                size=(1260, 720),
                start_time=0.0,
                stop_time=None,
                runs=1,)

# Natural Scenes
scenes_folder = "//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/Natural Images"
image_files = [os.path.join(scenes_folder, f) for f in os.listdir(scenes_folder) if \
                len(f) > 4 and f[-4:] in ['.jpg','.png','.tif','tiff']]

ns = NaturalScenes(image_path_list=image_files,
                   window=window,
                   sweep_length=0.50,
                   start_time=0.0,
                   stop_time=None,
                   blank_length=0.0,
                   blank_sweeps=10,
                   runs=3,
                   shuffle=True,)

# Drifting gratings
dg = Stimulus(visual.GratingStim(window,
                                 pos=(0, 0),
                                 units='deg',
                                 size=(250, 250),
                                 mask="None",
                                 texRes=256,
                                 sf=0.1,
                                 ),
              sweep_params={
                'Contrast': ([0.8], 0),
                'TF': ([2.0, 4.0], 1),
                'SF': ([0.04], 2),
                'Ori': (range(0, 360, 45), 3),
                },
              sweep_length=2.0,
              start_time=0.0,
              blank_length=1.0,
              blank_sweeps=8,
              runs=5,
              shuffle=True,
              save_sweep_table=True,
              )

# Static Gratings
sg = Stimulus(visual.GratingStim(window,
                                 pos=(0, 0),
                                 units='deg',
                                 size=(250, 250),
                                 mask="None",
                                 texRes=256,
                                 sf=0.1,
                                 ),
              sweep_params={
                         'Contrast': ([0.8], 0),
                         'SF': ([0.02, 0.08, 0.32], 1),
                         'Ori': (range(0, 180, 30), 2),
                         },
              sweep_length=0.5,
              start_time=0.0,
              blank_length=0.0,
              blank_sweeps=10,
              runs=5,
              shuffle=True,
              save_sweep_table=True,
              )

# Set display sequences
lsn8_ds = [(90, 390)]
ns_ds = [(480, 675)]
dg_ds = [(765, 1035)]
sg_ds = [(1125, 1175)]

lsn8.set_display_sequence(lsn8_ds)
ns.set_display_sequence(ns_ds)
dg.set_display_sequence(dg_ds)
sg.set_display_sequence(sg_ds)

############ SweepStim Setup ##################################################
# kwargs
params = {
}

# create SweepStim instance
ss = SweepStim(window,
               stimuli=[lsn8, ns, dg, sg],
               pre_blank_sec=0,
               post_blank_sec=0,
               params=params,
               )

# add in foraging so we can track wheel, potentially give rewards, etc
f = Foraging(window=window,
             auto_update=False,
             params=params,
             nidaq_tasks={'digital_input': ss.di,
                          'digital_output': ss.do,})  #share di and do with SS
ss.add_item(f, "foraging")

# run it
ss.run()
