from PIL import Image, ImageSequence
import os

im = Image.open("teaser_horseback.gif")
outdir = "datasets/test/folder1"

index = 1
for frame in ImageSequence.Iterator(im):
    framename = "frame%d.png" % index
    outpath = os.path.join(outdir, framename)
    frame.save(outpath)
    index += 1