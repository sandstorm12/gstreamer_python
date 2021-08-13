"""
This code is to show how to add/disconnect a stream to/from a pipeline dynamically (while the pipeline is running)

You should also check tools.py for some function calls and object instantiations.

Created by Aref, Oct. 4 2020

"""

import sys

sys.path.append('..')
import tools
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

if __name__ == '__main__':
    Gst.init(None)

    pipeline = Gst.Pipeline()

    elems = tools.make_many('videotestsrc', 'capsfilter', 'videoconvert', 'videoconvert', 'queue', 'fpsdisplaysink')
    tools.add_many(pipeline, *elems)

    src0, capsfilter, convert0, convert1, queue0, sink0 = elems
    # capsfilter.set_property('caps', 'video/x-raw,width=640,height=480')  # this throws an error for some reason
    Gst.util_set_object_arg(capsfilter, 'caps', 'video/x-raw,width=640,height=480')
    tools.link_many(*elems)

    loop = GLib.MainLoop()
    tools.prep_pipe(pipeline, loop)

    timeout = 2500  # ms
    add_remove_stream_obj = tools.AddRemoveStream(pipeline, add_periodically=True)
    # add_stream_obj.add_stream will be called every 'timeout' milliseconds
    GLib.timeout_add(timeout, add_remove_stream_obj.add_remove_stream_cb)

    loop.run()

    pipeline.set_state(Gst.State.NULL)
    del pipeline
