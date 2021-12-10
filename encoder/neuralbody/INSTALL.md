### Set up the python environment

```
conda create -n neuralbody python=3.7
conda activate neuralbody

# make sure that the pytorch cuda is consistent with the system cuda
# e.g., if your system cuda is 10.0, install torch 1.4 built from cuda 10.0
pip install torch==1.4.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html

pip install -r requirements.txt

# install spconv
cd
git clone https://github.com/traveller59/spconv --recursive
cd spconv
git checkout abf0acf30f5526ea93e687e3f424f62d9cd8313a
export CUDA_HOME="/usr/local/cuda-10.0"
python setup.py bdist_wheel
cd dist
pip install spconv-1.2.1-cp36-cp36m-linux_x86_64.whl
```

### Set up datasets

#### People-Snapshot dataset

1. Download the People-Snapshot dataset [here](https://graphics.tu-bs.de/people-snapshot).
2. Process the People-Snapshot dataset using the [script](https://github.com/zju3dv/neuralbody#process-people-snapshot).
3. Create a soft link:
    ```
    ROOT=/path/to/neuralbody
    cd $ROOT/data
    ln -s /path/to/people_snapshot people_snapshot
    ```

#### ZJU-Mocap dataset

1. Download the ZJU-Mocap dataset using the [script](zju_smpl/download.sh) or from [here](https://zjueducn-my.sharepoint.com/:f:/g/personal/pengsida_zju_edu_cn/Eo9zn4x_xcZKmYHZNjzel7gBdWf_d4m-pISHhPWB-GZBYw?e=Hf4mz7).
2. Create a soft link:
    ```
    ROOT=/path/to/neuralbody
    cd $ROOT/data
    ln -s /path/to/zju_mocap zju_mocap
    ```
