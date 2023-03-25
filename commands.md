First, a Docker warning:  
**DO NOT CTRL-C TO STOP A PROCESS IN A DOCKER CONTAINER**  
To gracefully stop a process in a Docker container, open a new terminal and run the following commands:
```
$ sudo docker ps # get the id of the running container
$ sudo docker stop -t 60 <container> # gracefully stop process inside Docker container and container altogether
```

## Generate low-resolution video using pre-trained horseback riding model
Run the following command in `~/git/long-video-gan` folder:
```
asvin@ece-A51998:~/git/long-video-gan$ sudo docker run --gpus '"device=0"' -it --rm --user $(id -u):$(id -g) -v `pwd`:/scratch --workdir /scratch -e HOME=/scratch long-video-gan python generate.py --outdir=outputs/horseback --seed=49 --save-lres=True --lres=https://nvlabs-fi-cdn.nvidia.com/long-video-gan/pretrained/horseback_lres.pkl
```
Successful execution of command should display the following:
```
[sudo] password for asvin: 
Downloading https://nvlabs-fi-cdn.nvidia.com/long-video-gan/pretrained/horseback_lres.pkl ... done
Generating video...
Setting up PyTorch plugin "bias_act_plugin"... Done.
Setting up PyTorch plugin "upfirdn2d_plugin"... Done.
Saving low-resolution video: outputs/horseback/seed=49_len=301_lres.mp4
Enjoy!
```

# Download horseback/biking datasets as .zip for training
Navigate to where you want to save the dataset (probbaly somewhere in `datasets/`) and run the following command:
```
wget -r -l5 -H -t1 -nd -N -np -A.zip -erobots=off [url of website] 
```
36x64 size horeback dataset URL is: https://nvlabs-fi-cdn.nvidia.com/long-video-gan/datasets/horseback/0036x0064/  
Currently the horseback 36x64 size dataset is saved at: `~/git/long-video-gan/datasets/horseback/0036x0064`

# Training Example
**Example**: Run the following command in `~/git/long-video-gan` folder to train on horseback dataset:
```
asvin@ece-A51998:~/git/long-video-gan$ sudo docker run --gpus '"device=0"' -it --rm --user $(id -u):$(id -g) -v `pwd`:/scratch --workdir /scratch -e HOME=/scratch long-video-gan python -m torch.distributed.run --nnodes=1 --nproc_per_node=1 train_lres.py --outdir=runs/lres --dataset=datasets/horseback --batch=8 --grad-accum=4 --gamma=1.0 
```
Notes:
- when `wandb` prompts for an input, I enter `3` to skip syncing of GPU stats like power usage, temperature, etc. to cloud. I've found that this `wandb` syncing can take a while. 
- change the number of steps in `train_lres.py` on line 271: `total_steps=1`, the original training script uses 1000000 steps :o
- to use both GPUs, change `gpu` flag to `--gpus '"device=0,1"'` (I think, I have yet to test this)  
- `--nproc_per_node` could possibly be 2 if using both GPUs (also have not tested it)  
- the original code uses `--batch=64 --grad-accum=2` but I run into memory errors  
- the original code evaluates metrics but I found this step took a long time so for now I am skipping it by leaving out the `--metrics` flag from the command  

Original training command for reference:
```
python -m torch.distributed.run --nnodes=1 --nproc_per_node=8 train_lres.py \
    --outdir=runs/lres --dataset=datasets/horseback --batch=64 --grad-accum=2 --gamma=1.0 --metric=fvd2048_128f
```

Successful execution of command should display the following:
```
[sudo] password for asvin: 
Random seed: 87542321
wandb: (1) Create a W&B account
wandb: (2) Use an existing W&B account
wandb: (3) Don't visualize my results
wandb: Enter your choice: 3
wandb: You chose "Don't visualize my results"
wandb: Tracking run with wandb version 0.14.0
wandb: W&B syncing is set to `offline` in this directory.  
wandb: Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
Setting up PyTorch plugin "bias_act_plugin"... Done.
Setting up PyTorch plugin "upfirdn2d_plugin"... Done.
Loading video dataset... 4.97s
Saving real videos... 1.45s
Constructing low res GAN model... 1.87s
Training for steps 0 - 1


VideoGenerator                           Parameters  Buffers  Output shape           Datatype  Mean        Std         Min (abs)   Max (abs) 
---                                      ---         ---      ---                    ---       ---         ---         ---         ---       
temporal_emb                             -           640128   [1, 1024, 640]         float32   -2.553e-01   9.954e-01   5.433e-07   3.695e+00
...
<top-level>                              6144        -        [1, 3, 128, 36, 64]    float32    1.607e-01   2.034e-01   8.196e-08   9.060e-01
---                                      ---         ---      ---                    ---       ---         ---         ---         ---       
Total                                    83215939    640197   -                      -         -           -           -           -         


VideoDiscriminator             Parameters  Buffers  Output shape          Datatype  Mean        Std         Min (abs)   Max (abs) 
---                            ---         ---      ---                   ---       ---         ---         ---         ---       
blocks.0.conv_vid              128         -        [1, 32, 128, 64, 64]  float32    4.595e-02   1.909e-01   0.000e+00   2.587e+00
...
epilogue.linear_1              1025        -        [1, 1]                float32   -1.398e-01         nan   1.398e-01   1.398e-01
---                            ---         ---      ---                   ---       ---         ---         ---         ---       
Total                          46424609    32       -                     -         -           -           -           -         

Finished training!
wandb: Waiting for W&B process to finish... (success).
wandb: You can sync this run to the cloud by running:
wandb: wandb sync runs/lres/00000-horseback-8batch-4accum-1.0gamma/wandb/offline-run-20230325_170700-h9fgki91
wandb: Find logs at: runs/lres/00000-horseback-8batch-4accum-1.0gamma/wandb/offline-run-20230325_170700-h9fgki91/logs
```

# Make dataset from video clips
1. Activate long-video-gan `conda` environment:
```
conda activate
conda activate long-video-gan
```
2. Generate dataset youtube video with video ID and timestamps specified in `*.json` file. Depending on where you want to save the dataset and youtube video, you may need to `mkdir` those folders first.
**Example**: generate horseback frames from `horseback.json` file
```
python -m dataset_tools.make_dataset_from_youtube dataset_tools/youtube_configs/horseback.json datasets/horseback_test video_cache/horseback_test
```
The script by default generates datasets with frames of 144x256 size.

## Copy files from server to local machine
On your **local machine**, run the following command:
```
scp asvin@genesis.ece.utexas.edu:/path/to/file/on/server/ .
```
