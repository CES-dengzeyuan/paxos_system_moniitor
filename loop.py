from get_fig import *

import os

folder_path = '压测结果'

# Iterate over all the files in the folder and its subfolders
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        filename = os.path.join(root, file_name)
        plot(filename)