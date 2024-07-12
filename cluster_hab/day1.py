"""
Habituation Day 1.

Total: 606 seconds = 10.1 min

"""

from psychopy import visual
from camstim import Stimulus, SweepStim, MovieStim
from camstim import Foraging
from camstim import Window, Warp

# Create display window
window = visual.Window(fullscr=True,
                monitor='Gamma1.Luminance50',
                screen=0,
                #warp=Warp.Spherical,
                )

############ Stimulus definitions #############################################
# Natual Movie 2
nm2_path = r"//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/Movie_TOE2.npy"

nm2 = MovieStim(movie_path=nm2_path,
                window=window,
                frame_length=2.0/60.0,
                size=(1920, 1080),
                start_time=0.0,
                stop_time=None,
                flip_v=True,
                runs=4,)

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
                'TF': ([1.0, 2.0], 1),
                'SF': ([0.04], 2),
                'Ori': (range(0, 270, 45), 3),
                },
              sweep_length=2.0,
              start_time=0.0,
              blank_length=1.0,
              blank_sweeps=5,
              runs=5,
              shuffle=True,
              save_sweep_table=True,
              )

# Locally Sparse Noise
lsn_path = "//allen/programs/braintv/workgroups/neuralcoding/Saskia/Visual Stimuli 151207/sparse_noise_no_boundary_16x28_scaled.npy"

lsn = MovieStim(movie_path=lsn_path,
                window=window,
                frame_length=0.5,
                size=(1260, 720),
                start_time=0.0,
                stop_time=None,
                runs=1,)

# Set display sequences
nm2_ds = [(60, 180)]
dg_ds = [(225, 441)]
lsn_ds = [(486, 606)]

nm2.set_display_sequence(nm2_ds)
dg.set_display_sequence(dg_ds)
lsn.set_display_sequence(lsn_ds)

############ SweepStim Setup ##################################################
# kwargs
params = {
}

# create SweepStim instance
ss = SweepStim(window,
               stimuli=[nm2, dg, lsn],
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