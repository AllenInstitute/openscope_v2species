# OpenScope visual loop:
A temporary repository for the OpenScope visual loop project


# Installation
## Dependencies:
  - Windows OS (see Camstim package)
  - python 2.7
  - psychopy 1.82.01
  - camstim 0.2.4
  - matplotlib 2.2.3

## Installation with Anaconda or Miniconda:
  1. Navigate to repository and install conda environment:
     <br>`conda env create -f environment.yml`

  2. Activate the environment:
     <br>`conda activate allen_stimulus`

  3. Install the AIBS camstim package in the environment:
     <br>`pip install camstim/.`

  4. Install matplotlib library:
     <br>`conda install matplotlib`

  5. Download required video clips from movie_clips.zip and extract into the data directory.

# Input files
The software requires two sets of input files. There should be a set of text files present under `data/stimulus_orderings` that indicate the display order of video clips for different phases of the experiment.
<br><br>In addition, there should be a set of video clips (stored as raw .npy files).
<br>These clips must be downloaded and extracted into the data folder from [full_movies.zip](https://weizmannacil-my.sharepoint.com/:u:/g/personal/daniel_deitch_weizmann_ac_il/EWhOP-X8pXJPnNVxuKn-GFUBe8lqn907TmDpa2u7dmF9Kw?e=JSLu76) and stored in the path `data/full_movies`.
<br><br>For debugging purposes please download shortened versions of the movie clips from [short_movies.zip](https://weizmannacil-my.sharepoint.com/:u:/g/personal/daniel_deitch_weizmann_ac_il/EZzpjTqcXG9Bn4Xe-u9pgXIBHzLbIWfmtd8xKI4lvwIwvQ?e=uLVxT0) and extracted into the data folder and store them in the path `data/short_movies`

# Running the scripts
  1. Activate the environment:
     <br>`conda activate allen_stimulus`
  2. Run the stimulus_loop.py script (for group A input 0 and for group B input 1):
     <br> `python stimulus_loop.py 0`

# Stimulus design
The experiment consists of two phases in which different sets of 30 sec long natural movies will be presented:
   - Phase 1 consists of two natural movies (i.e., movie01 and movie02) and a constant gray screen (i.e., movie00).
   - Phase 2 consists of 50 natural movies (i.e., movie03-movie52) and a constant gray screen (i.e., movie00).

Animals are assigned into two groups (A and B), each presented with the movies in different order.
<br>In both groups, a total of 230 movies will be presented for a total time of 115 min:
  1. For group A:
     - Phase 1:
       - 50 presentations of movie01 (25 min)
       - 10 presentations of movie00 (5 min)
       - 50 alternations between movie01 and movie02 (25 min)
       - 10 presentations of movie00 (5 min)

     - Phase 2:
       - 20 presentations of movie03 (10 min)
       - 10 presentations of movie00 (5 min)
       - 50 sequential presentations of movie03 to movie52 (25 min)
       - 10 presentations of movie00 (5 min)
       - 20 alternations between movie03 and movie52 (10 min)

  2. For group B:
     - Phase 1:
       - 50 alternations between movie01 and movie02 (25 min)
       -  10 presentations of movie00 (5 min)
       -  50 presentations of movie01 (25 min)
       -  10 presentations of movie00 (5 min)

     - Phase 2:
       - 20 presentations of movie03 (10 min)
       - 10 presentations of movie00 (5 min)
       - 50 presentations of movie52 (25 min)
       - 10 presentations of movie00 (5 min)
       - 20 alternations between movie03 and movie52 (10 min)
