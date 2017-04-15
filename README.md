# PiCameraTesting

## Objectives
The objectives of this project are as follows:
1. Identify the algorithms needed to perform human detection and tracking
2. Test the feasbility of using these algorithms on the Raspberry Pi platform

The algorithms are implemented in Python using the OpenCV library.

## Requirements
- Hardware
    Raspberry Pi
    PiCamera
    USB Camera (optional)
- Software
    OpenCV 3.2.0 and above
    Python 3.4 and above (tested with up to Python 3.6.1)
    
## Installing Python3 and OpenCV on Raspbian Wheezy/Jessie
### Raspbian Wheezy
Because `python3` available on the repository is Python 3.2, it is strongly recommended to compile at least Python 3.4 (3.6 recommended) from source and install it on the Pi. 
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
