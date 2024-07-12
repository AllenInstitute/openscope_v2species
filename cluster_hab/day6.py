"""
Habituation Day 6.
on Ophys rig.

Total: 3544 seconds = 59.0 minutes

"""
import os
from psychopy import visual
from camstim import Stimulus, SweepStim, MovieStim, NaturalScenes
from camstim import Foraging
from camstim import Window, Warp

# Create display window
window = Window(fullscr=True,
                monitor='Gamma1.Luminance50',
                screen=0,
                warp=Warp.Spherical,)

############ Stimulus definitions #############################################
# Light leak habituation
# 1 Hz flash for 10 sec
leak0 = Stimulus(visual.GratingStim(window, tex=None, color=0,
                                       size=(1920,1200), units="pix"),
                    sweep_params={"Color":([-1,1], 0)},
                    sweep_length=0.5,
                    start_time=0.0,
                    runs=10,)
# 0.5 Hz flash for 10 sec
leak1 = Stimulus(visual.GratingStim(window, tex=None, color=0,
                                       size=(1920,1200), units="pix"),
                    sweep_params={"Color":([-1,1], 0)},
                    sweep_length=0.25,
                    start_time=10.0,
                    runs=20,)
# Natual Movie 1
nm1_path = r"//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/Movie_TOE1.npy"

nm1 = MovieStim(movie_path=nm1_path,
                window=window,
                frame_length=2.0/60.0,
                size=(1920, 1080),
                start_time=0.0,
                stop_time=None,
                flip_v=True,
                runs=10,)

# Natural Scenes
scenes_folder = "//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/Natural Images"
image_files = [os.path.join(scenes_folder, f) for f in os.listdir(scenes_folder) if \
                len(f) > 4 and f[-4:] in ['.jpg','.png','.tif','tiff']]

ns = NaturalScenes(image_path_list=image_files,
                   window=window,
                   sweep_length=0.25,
                   start_time=0.0,
                   stop_time=None,
                   blank_length=0.0,
                   blank_sweeps=100,
                   runs=20,
                   shuffle=True,)

# Drifting gratings type 1
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
                'TF': ([1.0, 2.0, 4.0, 8.0, 15.0], 1),
                'SF': ([0.04], 2),
                'Ori': (range(0, 360, 45), 3),
                },
              sweep_length=2.0,
              start_time=0.0,
              blank_length=1.0,
              blank_sweeps=20,
              runs=5,
              shuffle=True,
              save_sweep_table=True,
              )

# Locally Sparse Noise
lsn8_path = r"//allen/aibs/mat/michaelbu/Locally_Sparse_Noise_Trimmed/short/lsn_mat_8x14_short.npy"

lsn8 = MovieStim(movie_path=lsn8_path,
                window=window,
                frame_length=0.25,
                size=(1260, 720),
                start_time=0.0,
                stop_time=None,
                runs=1,)

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
                         'SF': ([0.02, 0.04, 0.08, 0.16, 0.32], 1),
                         'Ori': (range(0, 180, 30), 2),
                         'Phase': ([0, 0.25, 0.5], 3),
                         },
              sweep_length=0.25,
              start_time=0.0,
              blank_length=0.0,
              blank_sweeps=25,
              runs=20,
              shuffle=True,
              save_sweep_table=True,
              )

# Locally Sparse Noise
lsn4_path = "//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/sparse_noise_no_boundary_16x28_scaled.npy"

lsn4 = MovieStim(movie_path=lsn4_path,
                window=window,
                frame_length=0.25,
                size=(1260, 720),
                start_time=0.0,
                stop_time=None,
                runs=1,)

# Set display sequences
nm1_ds = [(90, 390)]
ns_ds = [(1790, 2386)]
dg_ds = [(480, 1110)]
lsn8_ds = [(2476, 3076)]
sg_ds = [(3166, 3634)]
lsn4_ds = [(1200, 1700)]

nm1.set_display_sequence(nm1_ds)
ns.set_display_sequence(ns_ds)
dg.set_display_sequence(dg_ds)
lsn8.set_display_sequence(lsn8_ds)
sg.set_display_sequence(sg_ds)
lsn4.set_display_sequence(lsn4_ds)

############ SweepStim Setup ##################################################
# kwargs
params = {}

# create SweepStim instance
ss = SweepStim(window,
               stimuli=[leak0, leak1, nm1, ns, dg, lsn8, sg, lsn4],
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
