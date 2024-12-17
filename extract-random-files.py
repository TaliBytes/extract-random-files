import os
import random
import shutil
import tkinter as tk
from tkinter import filedialog

# hidden root window
root = tk.Tk()
root.withdraw()

# how many gigs worth of files should be copied?
threshold_GB = int(input("How many gigs of random files to copy?"))
threshold_GB = threshold_GB if (threshold_GB != None or threshold_GB != 0) else 32  # default 32GB
threshold_bytes = threshold_GB * (1024 ** 3)    # GB => bytes

# get dir to extract data from
init_dir = '/home'
directory = filedialog.askdirectory(title=f"Select directory from which to copy {threshold_GB}GB of random files from?", initialdir=init_dir)
extractDir = str(directory) + '/EXTRACTED'


# number of times dirs have been delved into and were found empty ... used for error break from loop later
empty_dir_errors = 0





# select a dir or file item ()
def selectItem(dir):
    global empty_dir_errors
    # get possible items to either delve into (sub-dirs) or extact (copyable files)
    items = [item for item in os.listdir(dir) if item != 'EXTRACTED']

    if items:      
        rand_item = f'{dir}/{random.choice(items)}'
        
        # delve deeper if chosen item is a sub-dir
        if os.path.isdir(rand_item):
            selectItem(rand_item)

        # copy if chosen item is a sub-dir
        if os.path.isfile(rand_item):
            destdir = f'{extractDir}/{os.path.basename(rand_item)}'

            # don't extract files that have already been copied
            if (os.path.exists(destdir)):
                return
            
            shutil.copy(rand_item, f"{destdir}")
            return

    else:
        # sub-dir is empty to restart at the top level, increment error count by 1
        print('directory has no sub-dirs or files... restarting from top')
        empty_dir_errors += 1

        # leave function if empty_dir_errors is too great
        if (empty_dir_errors >= 500):
            return



#returns size of dir, sub-dirs, and files IN BYTES
def get_dir_size(sizeThisDir):
    total_size = 0

    # explore sub-dirs and files
    for dirpath, dirnames, filenames in os.walk(sizeThisDir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)

            # only operate of files (avoid symb links and the like)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)

    return(total_size)





# where everything actually starts
if directory:
    print(f'Startd in {directory}\n\n\n')

    # since duplicates are not allowed, the script should not allow more data to be requested than is actually available
    directorySize = get_dir_size(directory)
    if (threshold_bytes > directorySize):
        threshold_bytes = directorySize
        threshold_GB = directorySize / (1024 ** 3)
        print('The size of the source directory selected is SMALLER than the number of GB of data requested to extract. The new target extaction size has been set to the same size as the source directory.\n')

    # create destination folder where files are copied to
    if not os.path.exists(extractDir): os.makedirs(extractDir)

    # loop indefinitely until either enough files have been extracted OR enough errors have accumulated
    while True:
        current_size = get_dir_size(extractDir)
        print(f"{current_size / (1024 ** 3):.2f}/{threshold_GB} GB ... empty_dir_errors: {empty_dir_errors}")

        if current_size >= threshold_bytes: break
        if empty_dir_errors >= 500: break

        selectItem(directory)   # extract an item if threshold size or errors not met

    # once finished, print results
    if empty_dir_errors >= 500:
        print(f'\n\nToo many empty directories caused script to terminate early to prevent indefinite copy attempts... some files may have been copied. Check the new /EXTRACTED folder in {directory}.')
    else:
        print(f'\n\nCopying of {threshold_GB}GB worth of random files is complete.')
    
else:
    print('User did not select a directory to extract files from, or selected an invalid directory.\n')
