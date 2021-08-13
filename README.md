# A GStreamer Guide
If it is hard to write, it should be hard to read.

# Getting started

Install gstreamer on a Debian-based system:
```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

## Outline:
1. Wrestle a little with different pipelines with built-in elements: [launch_pipeline](launch_pipeline)
2. Implementing a simple element with in-place buffer modification: [base_transform_inplace](base_transform_inplace)
3. Implementing a simple element that changes the input buffer properties: [base_transform](base_transform)
4. Use meta-data in a pipeline: [meta](meta)
5. Extend Gst.Element to build more powerful plugins and implement a muxer: [muxer](muxer)
6. Use appsink to obtain information out of a pipeline: [appsink](appsink)
7. Dynamic pipelines: [add-remove-stream](add-remove-stream) [dynamic-pipe](dynamic-pipe)
8. Use intel-gpu for hardware-accelerated decoding: [vaapi](vaapi)
9. Use custom src to produce a custom input at the start of the pipeline. [custom_src](custom_src)
10. Use custom sink to get pipeline data and access/modify it at the end of the pipeline. [custom_sink](custom_sink)

## How to use the docker?
Firstly, you need unfiltered connection to clone some of the repositories.

Build docker:

```bash
sudo docker build -t gstreamer:python .
```

Give desktop environment access to docker:

```bash
xhost +local
```

Run the docker with desktop environment access:

```bash
sudo docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix gstreamer:python /bin/bash
```


## Some essential links:
[How to install GStreamer python bindings](http://lifestyletransfer.com/how-to-install-gstreamer-python-bindings/)

[How to implement custom python plugins](http://lifestyletransfer.com/how-to-write-gstreamer-plugin-with-python/)

## Some necessary commands
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

## Urgent issues and future work
1. Add a gitignore
2. Organize repo like your other github repos
3. Refactor codes
4. Remove cpp samples
5. Remove personal information
6. Prepare readme for each sample
7. Make each sample more useful
8. Refactor readme

## Issues and future work
1. [Nothing yet]
