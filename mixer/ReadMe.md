# Mixer (blender)
This example extends an especial type of base class. This class acts like a muxer yet with a unique property. The Aggregator class waits until all src pads queued some buffers before calling the **do_aggregate** method.

## How to run?
> gst-launch-1.0 mixer name=m ! videoconvert ! autovideosink videotestsrc ! m. videotestsrc pattern=ball ! m. videotestsrc pattern=snow ! m.

## Description
The **do_aggregate** method is where custom code is placed. **self.finish_buffer(output_buffer)** is used to push the created buffer to the output.
