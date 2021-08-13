**dynamic.py** demonstrates:

1. How to add/remove/swap an element in the pipeline while it is running.
2. How to change an element or a plugin properties(arguments) while the pipeline is running (especially how to change 
the FPS dynamically)

There is a method and a function to change the elements' properties:

1. **Gst.util_set_object_arg(object, argument_name, value):** https://gstreamer.freedesktop.org/documentation/gstreamer/gstutils.html?gi-language=python#gst_util_set_object_arg

        Gst.util_set_object_arg(capsfilter, 'caps', 'video/x-raw, width=640, height=480, framerate=30/1')
        
2. **Gst.Object.set_property(property_name, value):**

        videorate.set_property('max-rate', 30)

My advice is to use the method (set_property) over the function (util_set_object_arg) when it is feasible since the function does not return anything when something
goes wrong and the debugging would be hard. I had a problem using the method for setting caps property for **capsfilter**
plugin, so I had to use the function.

To change the FPS of the stream we should use **videorate** plugin. 
https://gstreamer.freedesktop.org/documentation/videorate/index.html?gi-language=c

This element takes an incoming stream of timestamped video frames. It will produce a perfect stream that matches the source pad's framerate.
If you want to change the framerate there, it has a max-rate property that indicates what is the maximum frame rate that the plugin
lets pass through the pipeline. If the max-rate is lower than input's framerate it just drops some of the frames. 
use `gst-inspect-1.0 videorate` for more details about its properties.

Also it is important that the videorate's src-pad and the next element's sink-pad negotiate properly; that is, their
capabilities should match each other. Because this caps negotiation process is dynamic in our example,
we need to use a **capsfilter** element after the videorate in the pipeline, and modify the 
the framerate in that element before setting the max-rate property in videorate (it should be ready for the incoming modified caps).

        Gst.util_set_object_arg(capsfilter, 'caps', 'video/x-raw, width=640, height=480, framerate=30/1')
        videorate.set_property('max-rate', 30)
        
Static test pipeline:

        gst-launch-1.0 v4l2src ! videorate max-rate=5 ! videoconvert ! capsfilter caps=video/x-raw,width=640,height=480,framerate=5/1 ! queue ! videoconvert ! gaussianblur ! videoconvert ! fpsdisplaysink
        
   
**Usage**: 

from **dynamic-pipe** directory:
`$ python dynamic.py`

The steps for dynamic pipeline manipulation are explained in detail in the official Gstreamer documents:

**https://gstreamer.freedesktop.org/documentation/application-development/advanced/pipeline-manipulation.html?gi-language=python#dynamically-changing-the-pipeline**

**https://gstreamer.freedesktop.org/documentation/application-development/advanced/pipeline-manipulation.html?gi-language=python#changing-format-in-a-playing-pipeline**



