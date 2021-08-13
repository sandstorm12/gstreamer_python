# Custom Sink
We can use a custom sink when we need a sink that does a custom task at the end of the pipeline.

# How to Run? 
to run the sink element:
```
gst-launch-1.0 fakesrc num-buffers=10 ! custom-sink
```

# Description
the do_render function is the equivalent of the transform_ip function.
Everytime the data reaches the custom sink, this function is called.

