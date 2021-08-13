# Custom SRC
We can use a custom src when we need a src that does a custom task at the start of the pipeline.
# Setup 
run:
```
source setup.sh
```

## How to Run? 
to run the src element:
```
gst-launch-1.0 custom_audio_src ! autoaudiosink
```

## Description

### Liveness
to put the src element in liveness mode(which we always need), Three things are needed:

   1. Calling GstBase.BaseSrc.set_live(True)

   2. Reporting the latency by handling the LATENCY query, which is what we do in do_gst_base_src_query. The attentive reader might have noticed that even though the GstBaseSrc virtual method is named query, we didn't implement it as do_query: that is because GstElement also exposes a virtual method with the same name, and we have to lift the ambiguity. Try implementing do_query and see what happens.

   3. Implementing get_times to let the base class know when it should actually push the buffer out.


*do_start* and *do_caps* functions are for initialization purposes and they are usually the same for all of our applications.

The **do_create** function is the most important function in this plugin.
This function generates the data for buffer and pushs it to the buffer.
As you can see in the program, we need to keep pointers for every data start and end point. 

P.S: you might see that in some examples, people use the do_fill function instead of do_create and buf.map(Gst.MapFlags.WRITE) method for mapping the buffer. Our current gstreamer version doesn't support this way of writing into buffer since it is added in newer version.





