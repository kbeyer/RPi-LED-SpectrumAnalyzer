set -e

# Defaults to install where install.sh is located
INSTALL_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

BUILD_DIR=${INSTALL_DIR}/BUILD
mkdir -p $BUILD_DIR

pushd $BUILD_DIR

# Install dependencies that can be obtained from apt repos
sudo apt-get install python-dev
## ffmpeg can either be ffmpeg or libav-tools depending on distro
sudo apt-get install -y ffmpeg || true
sudo apt-get install -y libav-tools || true
sudo apt-get install -y lame flac faad vorbis-tools
sudo apt-get install -y python-alsaaudio
sudo apt-get install -y python-imaging
sudo apt-get install -y python-numpy
sudo apt-get install -y python-virtualenv

# Dependencies for shairplay
sudo apt-get install -y autoconf automake libtool
sudo apt-get install -y libltdl-dev libao-dev libavahi-compat-libdnssd-dev
sudo apt-get install -y avahi-daemon

# Create a virtualenv
VENV=./venv
virtualenv $VENV --system-site-packages

# Source it
source $VENV/bin/activate

# Install mutagen
pip install mutagen

# Install decoder
wget -c http://www.brailleweb.com/downloads/decoder-1.5XB-Unix.zip
unzip -o decoder-1.5XB-Unix.zip
cp decoder-1.5XB-Unix/{codecs.pdc,*.py} $VENV/lib/python2.7/site-packages/
rm -rf decoder-1.5XB-Unix/

# Check to see if we have git
git --version > /dev/null

# Install py-spidev
pip install -e git+https://github.com/doceme/py-spidev.git#egg=spidev

# Install RPi-LED code
# FIXME: Use Kyle's fork for the different driver.
pip install -e git+git@github.com:adammhaile/RPi-LPD8806.git#egg=raspledstrip

# Install shairplay
wget -c https://github.com/juhovh/shairplay/archive/master.zip
unzip -o master.zip
cd shairplay-master
# we need to run it twice, since it fails the first time for some reason
./autogen.sh || true
./autogen.sh || true
./configure --prefix=$BUILD_DIR/venv
make
make install
# fixme: is it worth detecting the architecture?
cp $BUILD_DIR/venv/lib/libshairplay.so  $BUILD_DIR/venv/lib/libshairplay64.so
cp $BUILD_DIR/venv/lib/libshairplay.so $BUILD_DIR/venv/lib/libshairplay32.so
cp src/bindings/python/Shairplay.py $BUILD_DIR/venv/lib/python2.7/site-packages/

# Copy our patches to raspledstrip
cd $INSTALL_DIR
# fixme: the patches could be cleaned up, but don't have the time right now...
cp patches/ $BUILD_DIR/venv/src/raspledstrip/raspledstrip/
