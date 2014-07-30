RPi-LED-SpectrumAnalyzer
========================

Spectrum analyzer for RaspberryPi that lets you use LPD8806 or WS2801 LED
chipset, and also takes input either from a local file or via airplay/line-in.

## Inspiration

This project started by following a [guide on Adafruit](https://learn.adafruit.com/raspberry-pi-spectrum-analyzer-display-on-rgb-led-strip).  After encountering some issues getting the code to work with our hardware, we refactored into this repository.

To get the hardware setup (i.e. - configure Raspberry Pi, wire up LEDs, tune SPI) the guide referenced above is a good starting point.  Once you verify that the LEDs are functional, you can clone this repository into a new directory then follow instructions below to install and run.

## Install

Run the install shell script using

    bash install.sh

This will create a python virtual environment for you at BUILD/venv.  Source
this virtualenv for all future work, on this project.

    source BUILD/venv/bin/activate

## Usage

`run.py` is the main entry point.  `python run.py` will give you usage information.

You can use a local file as input, as follows:

    python run.py local /path/to/file.mp3

To use airplay, run:

    python run.py airplay

To use line input, run:

    python run.py linein

## Attributions

The sample file included in this project is Lack Of Colour by Krish Ashok,
licensed under a Creative Commons Licence.
