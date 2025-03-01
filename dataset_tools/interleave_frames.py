import os
import re
import click

def interleave2gif(datasetpath, ilfactor):
  # datasetpath = training/testing folder which has a subset for each "video clip" that is represented as separate frames
  # ilfactor    = pick 1 frame every 'ilfactor' frames
  
  filelist = sorted(os.listdir(datasetpath))
  clipfolderlist = [os.path.join(datasetpath, x) for x in filelist if os.path.isdir(os.path.join(datasetpath, x))]

  for clipfolder in clipfolderlist:
    filelist = sorted(os.listdir(clipfolder))
    cliptimestamplist = [os.path.join(clipfolder, x) for x in filelist if os.path.isdir(os.path.join(clipfolder, x))]

    for cliptimestamp in cliptimestamplist:
        # Create new folders
        for j in range(ilfactor):
            newdir = cliptimestamp+f"_{j+1:04d}"
            assert not os.path.isdir(newdir), f"The folder you wanted to create ({newdir:s}) already exists"
            os.mkdir(newdir)

        # Get list of frames for current time interval for current video clip
        imgs = sorted(os.listdir(cliptimestamp))
        framenums = [int(re.findall(r'\d+', x)[0]) for x in imgs]

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
@click.option("--ilfactor", "-i", "ilfactor", help="Interleaving factor", default=8, type=int, multiple=False)
def main(
    dataset_dir: str,
    ilfactor: int,
):
    """Split a video clipfolder from dataset into multiple clips
    Example:

    \b
    # Split the each video clips in horseback dataset into eight video clips
    python interleave_frames.py -d datasets/test -i 8
    """
    interleave2gif(dataset_dir, ilfactor)

###########################################################################################################

if __name__ == "__main__":
    main()
    