import os
import re
import click
import sys

import cv2

def flip_frames(datasetpath, flip_axis):
    filelist = sorted(os.listdir(datasetpath))
    clipfolderlist = [os.path.join(datasetpath, x) for x in filelist if os.path.isdir(os.path.join(datasetpath, x))]

    for clipfolder in clipfolderlist:
        filelist = sorted(os.listdir(clipfolder))
        cliptimestamplist = [os.path.join(clipfolder, x) for x in filelist if os.path.isdir(os.path.join(clipfolder, x))]
        
        for cliptimestamp in cliptimestamplist:
                # Create new folders
                for j in flip_axis:
                    newdir = cliptimestamp+f"_{j}"
                    assert not os.path.isdir(newdir), f"The folder you wanted to create ({newdir:s}) already exists"
                    os.mkdir(newdir)

                    imgs = sorted(os.listdir(cliptimestamp))
                    for frame in imgs:
                        image = cv2.imread(os.path.join(cliptimestamp, frame))
                        flipped = cv2.flip(image, j)

                        cv2.imwrite(os.path.join(newdir, frame), flipped)

###########################################################################################################

@click.command()
@click.option("--dataset", "-d", "dataset_dir", help="Path to dataset directory", type=str, required=True, multiple=False)
@click.option("--flip_axis", "-f", "flip_axis", help="Axis along which to flip: 0 = x-axis, 1 = y-axis, -1 = x and y-axes", required = True, type=int, multiple=True)
def main(
    dataset_dir: str,
    flip_axis: int,
):
    """Split a video clipfolder from dataset into multiple clips
    Example:

    \b
    # Split the each video clips in horseback dataset into eight video clips
    python interleave_frames.py -d datasets/trial -c 10
    """
    flip_frames(dataset_dir, flip_axis)

###########################################################################################################

if __name__ == "__main__":
    main()
    