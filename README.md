# GStreamer Python Samples

A collection of various samples for learning and bootstrapping.

## Notice

This project is a personal project under development. Questions, feature requests, and bug reports are much appreciated.

New samples will be added gradually. If you need a certain sample, feel free to contact me at <sandstormeatwo@gmail.com>.

## Table of content:
1. Wrestle a little with different pipelines with built-in elements: [launch_pipeline](launch_pipeline)
2. Implementing a simple element with in-place buffer modification: [base_transform_inplace](base_transform_inplace)
3. Implementing a simple element that changes the input buffer properties: [base_transform](base_transform)
4. Use meta-data in a pipeline: [meta](meta)
5. Extend Gst.Element to build more powerful plugins and implement a muxer: [muxer](muxer)
6. Use appsink to obtain information out of a pipeline: [appsink](appsink)
7. Dynamic pipelines: [add-remove-stream](add-remove-stream) [dynamic-pipe](dynamic-pipe)
8. Use intel-gpu for hardware-accelerated decoding: [vaapi](vaapi)
9. Use custom src to produce a custom input export 


## Getting started


### System-wide installation on Debian-based systems

```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```


### Using docker

Build docker image:

```bash
docker build -f Dockerfile -t gstreamer_python .
```

Give desktop environment access to the docker to see the pipeline output (Tested on ubuntu 20.04)

```bash
xhost +local
```

Run the docker with desktop environment access

```bash
sudo docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix gstreamer:python /bin/bash
```


## Urgent issues and future work
1. Add a gitignore
2. Remove personal information
3. Prepare readme for each sample
4. Refactor readme
5. Add "how to set gstreamer python for python plugins" to the main readme
6. Add "how to build gst-python from source" to the main readme


## Issues and future work
1. Make each sample more useful
2. Refactor codes


## Contributors

1. Hamid Mohammadi <sandstormeatwo@gmail.com>


## Useful links

[How to install GStreamer python bindings](http://lifestyletransfer.com/how-to-install-gstreamer-python-bindings/)

[How to implement custom python plugins](http://lifestyletransfer.com/how-to-write-gstreamer-plugin-with-python/)


## Useful commands

Setting GStreamer path and python plugins

```bash
export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/venv/lib/gstreamer-1.0/:$PWD/gst/
```

Setting GStreamer debug-level:

```bash
export GST_DEBUG="*:2"
```

How to clear GStreamer plugins cache:

```bash
rm -rf ~/.cache/gstreamer-1.0/
```
