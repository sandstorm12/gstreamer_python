# DOTGRAPH 
> GStreamer has the capability to output graph files(.dot files) that illustrate pipeline. These examples show how.

## Setup
install xdot to see graph files easily:
```
$ apt-get install xdot
```
set this vriable to specify the output folder for the dot files:
```
$ export GST_DEBUG_DUMP_DOT_DIR=/path/to/output/directory
```

## Run 
1. if you run gst-launch after you set the above varibale, it will automatically create a graph.

2. To obtain a graph from a inside python program add 
```
Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
``` 
to the program. the first varible is your pipeline object.   

see the example below. 
```
$ python3 dotgraph_example.py
```
After running, you can find the .dot file in the diretcory you specified in $GST_DEBUG_DUMP_DOT_DIR.
to see the graph, run:
```
$ xdot pipeline.dot
```