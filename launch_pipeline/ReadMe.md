# LaunchPipeline
This example demonstrates how to build and run a GStreamer pipeline within python code. Moreover, more complex pipelines, fire sources, and RTSP sources are used in different pipelines.

## How to run?
> python3 launch_pipeline.py

## Description
The **Gst.parse_launch(PIPELINE_DESCRIPTION)** creates a pipeline object based on the given pipeline description. The named elements can be obtained from the pipeline object using the **get_by_name(name)** method. You can get the bus object from the pipeline using the **get_bus** method. Setting listener functions on the bus enable us to receive various events from the pipeline and respond to them.

### PIPELINE_SIMPLE
A simple **videotestsrc** with pattern property set to the ball animation. The **videoconvert** element converts the input color-space to the color-space suitable for the following elements. The **fpsdisplaysink** can display the current fps, average fps, the total number of frames, and the number of dropped frames as a text overlay.

    gst-launch-1.0 videotestsrc name=videosource pattern=ball ! videoconvert ! fpsdisplaysink

### PIPELINE_CAPS
Three elements are handy in many pipelines. **Videoconvert**, **videoscale**, **videorate**. **Videoconvert** element changes the color-space of the incoming video stream. **Videoscale** element can resize the video stream. And **videorate** element changes the framerate of the stream by dropping excessive frames. These elements can automatically find a suitable color-space, scale, and framerate. However, it is possible to set these manually by defining a **capfilter** like the example below:

    gst-launch-1.0 videotestsrc name=videosource pattern=ball ! videoconvert ! videoscale ! videorate ! video/x-raw,format=BGRx,width=720,height=480,framerate=60/1 ! videoconvert ! fpsdisplaysink

### PIPELINE_MIXER
To create more complex pipelines, it is possible to name elements. In this example, we have created a **videomixer**. **Videomixer** element can combine to video streams into a single stream by putting the videos beside each other. To refer to the named elements, we use the element name followed by a dot. Not placing the exclamation sign in the pipeline description after an element means describing a new branch in the pipeline.

    gst-launch-1.0 videotestsrc name=videosource pattern=ball ! video/x-raw,format=RGBA,width=1280,height=720 ! videobox left=-1280 ! mixer. videotestsrc name=videosource2 pattern=snow ! video/x-raw,format=RGBA,width=1280,height=720 ! videobox left=0 ! mixer. videomixer name=mixer ! videoconvert ! autovideosink

### PIPELINE_TEE
Beside merging pipeline streams, they can be branched too. Branching streams can be done using **tee** or a **custom element**. The branched streams are copied by reference.

    gst-launch-1.0 videotestsrc name=videosource ! videoconvert ! t. tee name=t ! queue ! fpsdisplaysink t. ! queue ! fpsdisplaysink

### PIPELINE_FILE and PIPELINE_STREAM
The main use of GStreamer pipelines is to use file or stream sources. This can be done using **filesrc** or **rtspsrc** elements. Setting the location property on these elements specifies the file or stream source. **Decodebin** is a smart element that can decode video streams based on its format. Note that **videotestsrc** creates an uncompressed video stream.

    gst-launch-1.0 filesrc location=/home/hamid/Desktop/test.mp4 ! decodebin ! videoconvert ! fpsdisplaysink

    gst-launch-1.0 rtspsrc location=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov ! decodebin ! videoconvert ! fpsdisplaysink
