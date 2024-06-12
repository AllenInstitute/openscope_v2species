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

import argparse
import numpy as np
from psychopy import monitors
from camstim import MovieStim, SweepStim, Window, Warp
import glob
import logging

# Make logging a bit prettier
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Paths to the movie clip files to load.
movie_clip_files = glob.glob('data/full_movies/*.npy')

# For debugging use only:
# Set path to shorter versions of the movie clip files (5 sec each).
# If they don't exist yet make sure to download XXX.zp file first
# and extract the "short_movies" folder to the data folder.
# Should be used for development stages only. Comment out if not debugging!
# movie_clip_files = glob.glob('data/short_movies/*.npy')


# MOVIE_ZIP_URL = "https://tigress-web.princeton.edu/~dmturner/allen_stimulus/movie_clips.zip"
# for clip_path in movie_clip_files:
#     if not os.path.exists(clip_path):
#         raise ValueError("Movie clip file not found: {}. Make sure ".format(clip_path) +
#                          "to download from {} and extract them to the data folder.".format(MOVIE_ZIP_URL))


# Load the movie clip order for each experimental group as provided by the Ziv lab:
order_groupA = (np.loadtxt('data_development/stimulus_orderings/movie_order_groupA.txt').astype(int))
order_groupB = (np.loadtxt('data_development/stimulus_orderings/movie_order_groupB.txt').astype(int))

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
    for i in np.unique(order):

        # If the order index is less than the number of movie clips, load the movie clip.
        if i < len(movie_paths):

            # The movie clips should be 30 seconds long and should be played at 30 fps.
            s = MovieStim(movie_path=movie_paths[i],
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
                     params=config,
                     )

    return stim


if __name__ == "__main__":

    parser = argparse.ArgumentParser("stimulus")
    parser.add_argument("group", help="An integer representing the experiment group. Defaults to group A (value of 0).",
                        nargs='?', type=int, default=0)
    args = parser.parse_args()

    # Copied monitor and window setup from:
    # https://github.com/AllenInstitute/openscope-glo-stim/blob/main/test-scripts/cohort-1-test-12min-drifting.py

    dist = 15.0
    wid = 52.0

    monitor = monitors.Monitor("testMonitor", distance=dist, width=wid) #"Gamma1.Luminance50"

    # Create display window
    window = Window(fullscr=True,   # Will return an error due to default size. Ignore.
                    monitor=monitor,  # Will be set to a gamma calibrated profile by MPE
                    screen=0,
                    warp=Warp.Spherical
                    )

    config = {
        'sync_sqr': True,
    }

    if args.group == 0:
        order = order_groupA
    elif args.group == 1:
        order = order_groupB

    ss = make_movie_stimulus(movie_clip_files, order, window)

    ss.run()
