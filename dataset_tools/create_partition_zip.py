import os
from zipfile import ZipFile

def get_all_file_paths(directory):
  
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return sorted(file_paths)

MYPWD=os.getcwd()
FOLDER="/home/asvin/git/long-video-gan-az/datasets/flower"

os.chdir(FOLDER)

dirs = [x for x in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(),x))]
dirs = sorted(dirs)

for RES in dirs:
    CURRPATH=os.path.join(FOLDER,RES)
    FILENAME="partition_0000.zip"
    DESTPATH=os.path.join(FOLDER,'..','flowerzip',RES,FILENAME)
    
    os.chdir(CURRPATH)

    # Need to make zip files from directory that has folders for all clips
    if os.path.exists(FILENAME): os.remove(FILENAME)

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths('.')

    # writing files to a zipfile
    with ZipFile(FILENAME,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    os.system('cp '+FILENAME+' '+DESTPATH)

os.chdir(MYPWD)