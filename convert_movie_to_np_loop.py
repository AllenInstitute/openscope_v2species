import skvideo.io
import numpy as np
import os

vids_path = r'D:\phd\openscope_2024\movies_preperation\all_versions_v2\mp4_low_res_padding'
npy_path = r'D:\phd\openscope_2024\movies_preperation\all_versions_v2\npy_low_res_padding'

vids_list = os.listdir(vids_path)

i = 1
for vid_name in vids_list:
    print(vid_name[:-4])
    current_vid_path = os.path.join(vids_path,vid_name)
    current_vid = skvideo.io.vread(current_vid_path)
    current_vid_gray = current_vid[:, :, :, 0]

    file_name = 'movie' + str(i).zfill(2) +'.npy'
    current_npy_path = os.path.join(npy_path,file_name)
    np.save(current_npy_path, current_vid_gray)
    i += 1



