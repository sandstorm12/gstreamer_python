"""
This program runs a simple pipeline 
and saves the graph inside $GST_DEBUG_DUMP_DOT_DIR.
"""
import sys
import time
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk, GLib

Gst.init(None)

PIPELINE_SIMPLE = \
    "videotestsrc num-buffers=100 name=videosource pattern=ball" + \
    " ! videoconvert" + \
    " ! fpsdisplaysink"


def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()

    return True


mainloop = GObject.MainLoop()
pipeline = Gst.parse_launch(PIPELINE_SIMPLE)
Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "pipeline")

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_call, mainloop)
pipeline.set_state(Gst.State.PLAYING)
mainloop.run()