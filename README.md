# ideal-video-profile
A small Python script

Compares all the videos and images in a folder to find the ideal video profile if they were to be combined into one video (ie, the minimum resolution needed to fit all videos/pictures 100% and the max framerate found among all the videos). It also suggests the best standard profile (720p/1080p) that will accomodate your photos/videos, if one exists.

Good for making compilations of videos and pictures that come from a wide variety of sources. It makes it a bit easier, if you're one who cares about quality.

For personal use, so don't expect updates.

### Dependencies
Assuming you have python and pip already installed, they are: moviepy, cv2

Install dependencies with:

`pip install opencv-python moviepy`

### Usage

Tested on Linux 6.14, haven't tested Windows/Mac compatibility.

Specify the path of the folder containing the videos/images as an argument, default is the current directory.

Ex:
`python idealprofile.py ./folderyouwant`
