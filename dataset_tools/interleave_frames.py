import os
import re
import click

def interleave2gif(datasetpath, ilfactor):
  # datasetpath = training/testing folder which has a subset for each "video clip" that is represented as separate frames
  # ilfactor = pick 1 frame every 'ilfactor' frames
  
  filelist = sorted(os.listdir(datasetpath))
  clipfolderlist = [os.path.join(datasetpath, x) for x in filelist if os.path.isdir(os.path.join(datasetpath, x))]

  for clipfolder in clipfolderlist:

    for j in range(ilfactor):
        newdir = clipfolder+f"_{j+1:02d}"
        assert not os.path.isdir(newdir), f"The folder we wanted to create ({newdir:s}) already exists"
        os.mkdir(newdir)
    
    imgs = sorted(os.listdir(clipfolder))
    framenums = [int(re.findall(r'\d+', x)[0]) for x in imgs]

    for j in range(len(imgs)):
        jm = framenums[j] % ilfactor
        jm = 8 if jm==0 else jm
        oldpath = os.path.join(clipfolder, imgs[j])
        newpath = os.path.join(clipfolder+f"_{jm:02d}", imgs[j])
        print('Moving',oldpath,'->',newpath)
        os.rename(oldpath, newpath)

    os.rmdir(clipfolder)

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
    python interleave_frames.py --dataset=datasets/trial --ilfactor 8
    """
    interleave2gif(dataset_dir, ilfactor)

###########################################################################################################

if __name__ == "__main__":
    main()
    