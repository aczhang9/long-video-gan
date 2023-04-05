import os
import re
import numpy as np
import click

def interleave2gif(datasetpath, cliplength):
  # datasetpath = training/testing folder which has a subset for each "video clip" that is represented as separate frames
  # cliplength  = pick a frame every x frames such that new clip has roughly "cliplength" frames
  
  filelist = sorted(os.listdir(datasetpath))
  clipfolderlist = [os.path.join(datasetpath, x) for x in filelist if os.path.isdir(os.path.join(datasetpath, x))]

  for clipfolder in clipfolderlist:
    filelist = sorted(os.listdir(clipfolder))
    cliptimestamplist = [os.path.join(clipfolder, x) for x in filelist if os.path.isdir(os.path.join(clipfolder, x))]

    for cliptimestamp in cliptimestamplist:
        # Get list of frames for current time interval for current video clip
        imgs = sorted(os.listdir(cliptimestamp))
        framenums = [int(re.findall(r'\d+', x)[0]) for x in imgs]
        
        ilfactor = int(np.floor(len(imgs)/cliplength))

        # Create new folders
        for j in range(ilfactor):
            newdir = cliptimestamp+f"_{j+1:04d}"
            assert not os.path.isdir(newdir), f"The folder we wanted to create ({newdir:s}) already exists"
            os.mkdir(newdir)

        # Move frames
        for j in range(len(imgs)):
            jm = framenums[j] % ilfactor
            jm = ilfactor if jm==0 else jm
            oldpath = os.path.join(cliptimestamp, imgs[j])
            newpath = os.path.join(cliptimestamp+f"_{jm:04d}", imgs[j])
            print('Moving',oldpath,'->',newpath)
            os.rename(oldpath, newpath)

        # Remove old folder
        os.rmdir(cliptimestamp)

###########################################################################################################

@click.command()
@click.option("--dataset", "-d", "dataset_dir", help="Path to dataset directory", type=str, required=True, multiple=False)
@click.option("--cliplength", "-c", "cliplength", help="Interleaving factor", default=10, type=int, multiple=False)
def main(
    dataset_dir: str,
    cliplength: int,
):
    """Split a video clipfolder from dataset into multiple clips
    Example:

    \b
    # Split the each video clips in horseback dataset into eight video clips
    python interleave_frames.py -d datasets/trial -c 10
    """
    interleave2gif(dataset_dir, cliplength)

###########################################################################################################

if __name__ == "__main__":
    main()
    