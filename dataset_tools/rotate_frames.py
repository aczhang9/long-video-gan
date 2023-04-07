import os
import re
import click
import sys

import cv2

def rotate_frames(datasetpath, rotation_angle):
    filelist = sorted(os.listdir(datasetpath))
    clipfolderlist = [os.path.join(datasetpath, x) for x in filelist if os.path.isdir(os.path.join(datasetpath, x))]

    for clipfolder in clipfolderlist:
        filelist = sorted(os.listdir(clipfolder))
        cliptimestamplist = [os.path.join(clipfolder, x) for x in filelist if os.path.isdir(os.path.join(clipfolder, x))]
        
        for cliptimestamp in cliptimestamplist:
                # Create new folders
                for j in rotation_angle:
                    newdir = cliptimestamp+f"_{j}"
                    assert not os.path.isdir(newdir), f"The folder you wanted to create ({newdir:s}) already exists"
                    os.mkdir(newdir)

                    imgs = sorted(os.listdir(cliptimestamp))
                    for frame in imgs:
                        image = cv2.imread(os.path.join(cliptimestamp, frame))
                        (h, w) = image.shape[:2]
                        (cX, cY) = (w // 2, h // 2)

                        # rotate our image by 45 degrees around the center of the image
                        M = cv2.getRotationMatrix2D((cX, cY), j, 1.0)
                        rotated = cv2.warpAffine(image, M, (w, h))
                        cv2.imwrite(os.path.join(newdir, frame), rotated)

###########################################################################################################

@click.command()
@click.option("--dataset", "-d", "dataset_dir", help="Path to dataset directory", type=str, required=True, multiple=False)
@click.option("--rotation_angle", "-r", "rotation_angle", help="Angle to rotate", default=[180], type=int, multiple=True)
def main(
    dataset_dir: str,
    rotation_angle: int,
):
    """Split a video clipfolder from dataset into multiple clips
    Example:

    \b
    # Split the each video clips in horseback dataset into eight video clips
    python interleave_frames.py -d datasets/trial -c 10
    """
    rotate_frames(dataset_dir, rotation_angle)

###########################################################################################################

if __name__ == "__main__":
    main()
    