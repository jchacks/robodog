# Robodog

Influenced by "[Freenove Robot Dog Kit for Raspberry Pi
](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)" available under the Creative Commons [BY NC SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) license.

## Installation

Execute the below inorder to setup the Dog.

- `apt update`
- `apt upgrade`
- `apt install -y libcap-dev` - Was missing on my system
- Optional:
  - If you want a headless install then you can skip
  - `sudo apt install -y python3-pyqt5 python3-opengl`
- `python3.9 -m venv .venv`
- `source .venv/bin/activate`
- `pip install --upgrade pip`
- `pip install ".[dog]"`

## Usage

I havent figured out how to run everything without root yet.

Adding to the kmem group didnt solve the problem.

- `sudo .venv/bin/python -m robodog.server.led`
- `sudo .venv/bin/python -m robodog.server.camera`

When forwarding GUI components via X11 (ssh) the forwarding will fail because we are running as root.
[This article from IBM](https://www.ibm.com/support/pages/x11-forwarding-ssh-connection-rejected-because-wrong-authentication) explains what is happening.
You can see the error message when connecting with higher verbosity e.g. `ssh -v -X user@pi`.

## Documentation

While investigating the libraries and packages used this documentation was found useful.

- https://www.ti.com/product/ADS7830 - Battery management?
- [Camera](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [FFmpeg streaming](https://trac.ffmpeg.org/wiki/StreamingGuide)
