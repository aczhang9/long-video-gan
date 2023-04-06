import os
import json
import argparse
from zipfile import ZipFile, ZIP_STORED


def makejson(videodir):
    dirs = [x for x in os.listdir(videodir) if os.path.isdir(os.path.join(videodir,x))]
    # dirs would be something like 2LC-MiLvWqk, 95uurSUYbgQ, ...
    frame_paths = []
    for dir in dirs:
        timestamps = os.listdir(os.path.join(videodir,dir))
        # timestamps would be something like 0_05-0_28_0001, 0_05-0_28_0002, ...
        for ts in timestamps:
            video_relative_dir = os.path.join(dir,ts)
            frames = sorted(os.listdir(os.path.join(videodir,dir,ts)))
            frame_paths.append((video_relative_dir, frames))

    frame_paths_json = json.dumps(dict(frame_paths), indent=2, sort_keys=True)
    json_path = os.path.join(videodir,"frame_paths.json")
    with open(json_path, "w") as outfile:
        outfile.write(frame_paths_json)

def makejsonall(datasetdir):
    assert os.path.isdir(datasetdir)
    dirs = [os.path.join(datasetdir,x) for x in os.listdir(datasetdir) if os.path.isdir(os.path.join(datasetdir,x))]
    # dirs would be something like 0036x0064, 0036x0064_test, ...
    for x in dirs:
        makejson(x)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new frame_path.json file for train/test folder")
    parser.add_argument("dataset", help="Path to dataset with train and test folder")
    args = parser.parse_args()

    '''
    Used this function like this from the long-vide-gan-az directory:
    python dataset_tools/make_frame_path_json.py datasets/flower
    '''

    makejsonall(args.dataset)