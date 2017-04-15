# PiCameraTesting

## Objectives
The objectives of this project are as follows:
1. Identify the algorithms needed to perform human detection and tracking
2. Test the feasbility of using these algorithms on the Raspberry Pi platform

The algorithms are implemented in Python using the OpenCV library.

## Requirements
- Hardware
    - Raspberry Pi
    - PiCamera
    - USB Camera (optional)
- Software
    - OpenCV 3.2.0 and above
    - Python 3.4 and above (tested with up to Python 3.6.1)
    
## Installing Python3 and OpenCV on Raspbian Wheezy/Jessie
### Raspbian Wheezy
Because `python3` available on the repository is Python 3.2, it is strongly recommended to compile at _least_ Python 3.4 (3.6 recommended) from source and install it on the Pi.

#### Python 3.6
```
sudo apt-get update
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
tar xzvf Python-3.6.1.tgz
cd Python-3.6.1
./configure
make -j4
sudo make altinstall 
```
If any of the packages cannot be found, try a newer version number.

#### Virtualenv
It is highly recommended to use virtualenv to manage Python environments. 
```
sudo pip3.6 install virtualenv virtualenvwrapper
```
Open `~/.profile` using one's preferred editior and add in the following lines at the bottom of the file.

```
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
After saving and exiting, use `source ~/.profile` to load the changes made. 

```
mkvirtualenv humanDetection -p python3.6
workon humanDetection
```
All work will be performed inside the humanDetection python virtual environment. 

####OpenCV

```
cd ~
git clone https://github.com/Itseez/opencv.git
cd opencv
git checkout 3.2.0
cd ~
git clone https://github.com/Itseez/opencv_contrib.git
cd opencv_contrib
git checkout 3.2.0
```
It is _very_ important that both opencv and opencv_contrib are on the same version.

```
workon humandetection
pip install numpy "picamera[array]" imutils
cd ~/opencv
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \ -D CMAKE_INSTALL_PREFIX=/usr/local \ -D INSTALL_C_EXAMPLES=ON \ -D INSTALL_PYTHON_EXAMPLES=ON \ -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \ -D BUILD_EXAMPLES=ON ..
```
It is important to check the output of cmake to ensure that the Python interpreter point to the Python binary and the numpy points to the numpy install. If it doesn't point properly, delete the build folder and reinstall numpy. Afterwhich perform cmake again. 

```
make -j4
sudo make install
sudo ldconfig
cd /usr/local/lib/python3.6/site-packages/
sudo mv cv2.cpython-36m-arm-linux-gnueabihf.so cv2.so
cd ~/virtualenvs/humanDetection/lib/python3.6/site-packages
ln -s /usr/local/lib/python3.6/site-packages/cv2.so cv2.so
```
Test the install by `import cv2` inside the python interpreter. If it doesnt throw an error, `cv2.__version__` and observe the output. 

Test that the PiCamera is working properly using `raspistill -o output.jpg`. 

Adapted from [http://www.pyimagesearch.com/2015/07/27/installing-opencv-3-0-for-both-python-2-7-and-python-3-on-your-raspberry-pi-2/]