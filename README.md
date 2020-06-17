# GenBox2D
Generate physical reasoning datasets with Box2D.

## Installation

### Install PHYRE

The simplest way to install PHYRE is via pip. As PHYRE requires **Python version 3.6**, we recommend installing PHYRE inside a virtual environment, e.g. using Conda.

Notice that currently you can only install PHYRE with pip in **Linux**. See this [issue](https://github.com/facebookresearch/phyre/issues/29) for latest updates on Mac.`

```(bash)
conda create -n phyre python=3.6 && conda activate phyre

pip install phyre
```

### Install pyBox2D

```(bash)
sudo apt-get install -y build-essential python-dev swig python-pygame git

git clone https://github.com/pybox2d/pybox2d

cd pybox2d

python setup.py build

sudo python setup.py install
```

## Getting Started


Tasks in PHYRE are defined with template id and mod id, e.g., task with id 00000:001 has 00000 as its template id and 001 as its mod id. You can either do a specific task with --task_id or a range of tasks with --start_template_id, --end_template_id and --num_mods.

To run the program, cd into `GenBox2D/src/main/python` and run `main.py`. For example:

```(bash)
# Single task
python main.py --task_id 00000:001

# Range tasks
python main.py --start_template_id 0 --end_template_id 5 --num_mods 2
```

There are two modes in GenBox2D, GUI mode and dataset mode

### GUI mode

GUI mode allows you to visualize the world created by pyBox2D with pygame package for graphics. To enable GUI mode, you need to set -i flag when running the main function. GUI mode will show the graphics **without** generating datasets. You can use keyboard to switch between tasks and use mouse to drag around the objects.

An example command to run the program in GUI mode:

```(bash)
python main.py --start_template_id 0 --end_template_id 5 --num_mods 2 -i
```

Some controls when interacting with GUI:

* Enter: switch to the next task.
* Backspace: switch to the previous task.
* ESC: exit GUI.
* Arrow keys: Move the screen.
* Scroll wheel: Zoom the screen.

### Dataset mode

Dataset mode will generate datasets with the way you want. The generated data are organized in the following file structure.

```
log-06-17-2020-01-15-31
├── 00000:000.log
├── 00000:001.log
├── 00001:000.log
├── 00001:001.log
├── 00002:007.log
├── 00002:011.log
└── ...
```

For each task, we save the information for the task and simulation results for every timestamp into JSON format. You can see the example JSON files under the [GenBox2D/example](https://github.com/eastlife/GenBox2D/tree/master/example) folder.


## Configure your datasets

GenBox2D provides multiple parameters to customize and prepare your datasets. Simply run `python main.py -h` to see these parameters. Also, you may want to change the physical properties by creating another config JSON under the `GenBox2D/config` folder.

