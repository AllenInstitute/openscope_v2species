# OpenScope V2 species:
A temporary repository for the OpenScope V2 species project


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

In addition, there should be a set of video clips (stored as raw .npy files).
<br>These clips must be downloaded and extracted into the data folder from [full_movies.zip](https://weizmannacil-my.sharepoint.com/:u:/g/personal/daniel_deitch_weizmann_ac_il/EbetUfh76FtBtDkpqd-7gAEB43WxjSCKutxW8sJtvIfCiA?e=LPY5ND) and stored in the path `data/full_movies`.

For debugging purposes please download shortened versions of the movie clips from [short_movies.zip](https://weizmannacil-my.sharepoint.com/:u:/g/personal/daniel_deitch_weizmann_ac_il/EZzpjTqcXG9Bn4Xe-u9pgXIBHzLbIWfmtd8xKI4lvwIwvQ?e=uLVxT0) and extracted into the data folder and store them in the path `data/short_movies`.

# Running the scripts
  1. Activate the environment:
     <br>`conda activate allen_stimulus`
     
  3. Run the stimulus_v2species.py script:
     <br> `python stimulus_v2species.py`


# Stimulus design
The experiment consists of ...