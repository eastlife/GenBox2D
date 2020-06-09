# We recommand to create conda environment and work under the virtual environment
# conda create -n phyre python=3.6 && conda activate phyre

# install PHYRE
pip install phyre

# install pyBox2D

apt-get install -y build-essential python-dev swig python-pygame git

git clone https://github.com/pybox2d/pybox2d

python pybox2d/setup.py build

python pybox2d/setup.py install
