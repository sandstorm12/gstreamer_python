# VAAPI
> This repo consists of some examples for vaapi. vaapi is an api in gstreamer that helps you decode streams with cpu's gpu.
## Setup

To install vaapi, follow this [guide.](lifestyletransfer.com/how-to-install-gstreamer-vaapi-plugins-on-ubuntu/)
    
some things that might occur:   

if you decided to build the gstreamer vaapi from the scratch, you might miss codecparsers and you can install it with:
```
$ sudo apt-get install --reinstall gstreamer1.0-alsa gstreamer1.0-libav gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-pulseaudio libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-good1.0-0 libgstreamer1.0-0
```
## Check Setup
Run:
```$ gst-inspect-1.0 vaapi ```

if the plugin was not found check the installation again and run:
``` rm -r ~/.cache/gstreamer-1.0/ ```

 if it spit out some jibrish errors "before pointing out that the package is not found or before showing package properties" this might help:   
 ```
 $ export GST_VAAPI_ALL_DRIVERS=1
```
**Note** : the examples in the original tutorial might cause errors because the "vaapih264dec" plugin is no longer in the gstreamer vaapi package.
try replacing it with "vaapidecodebin".
see below examples for more information,
## Run examples

run the below code to see an example of a pipleline with vaapi in python:
```
 python3 vaapi_example.py
```

decoede an quicktime H.264 file by vaapi:   
```shell
$  gst-launch-1.0 filesrc location=path/to/mp4/file ! qtdemux ! h264parse ! vaapidecodebin !  autovideosink
```
decode a quicktime H.264 file by vaapi with 5 frame per second:
 ```
$ gst-launch-1.0 filesrc location=path/to/mp4/file ! qtdemux ! h264parse ! vaapidecodebin ! videorate ! video/x-raw,framerate=5/1 ! fpsdisplaysink sync=true
```
decode an mkv file:
```
gst-launch-1.0 filesrc location=/path/to/mkv/file ! matroskademux ! vaapidecodebin ! autovideosink
```

decode an rtsp H.264 stream:
```
gst-launch-1.0 -e rtspsrc location=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov ! rtph264depay ! vaapidecodebin ! autovideosink
```
**Note**: you can use vaapisink instead of autovideosink. keep in mind that unlike autovideosink, vaapisink uses cpu's gpu for rendering the stream.


## Issues
1. some multistream pipelines crash due to too much ram usage

