"""
This code is to show how to change a plugin inside the pipeline dynamically (while the pipeline is running)

Also, it demonstrates how to change plugins' properties on the go (for example, the stream's fps)

It should be noted that for changing the fps dynamically, 'videorate' plugin should be used after the src in order to
set a bottleneck that drops a number of frames each second. The details could be seen at tools.ChangeProp.change_prop_cb
Note: Dynamic fps changing might not work with 'videotestsrc'

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

    elems = tools.make_many('v4l2src', 'capsfilter', 'videoconvert', 'queue', 'videoconvert', 'identity', 'edgetv',
                            'videoconvert', 'queue', 'fpsdisplaysink', 'videorate', 'videoconvert')

    src, filter_1, convert_0, queue_1, convert_1, effect, next_effect, convert_2, queue_2, sink, videorate, convert_3 \
        = elems

    Gst.util_set_object_arg(filter_1, 'caps', 'video/x-raw, width=640, height=480, framerate=30/1')
    videorate.set_property('max-rate', 30)
    videorate.set_property('drop-only', True)

    elements_dict = {'pipeline': pipeline, 'src': src, 'filter_1': filter_1, 'queue_1': queue_1, 'convert_1': convert_1,
                     'main_elem': effect, 'convert_2': convert_2,
                     'queue_2': queue_2, 'sink': sink, 'convert_0': convert_0, 'videorate': videorate}

    tools.add_many(pipeline, *elems)

    tools.link_many(src, videorate, convert_3, filter_1, queue_1, convert_1, effect, convert_2, queue_2, sink)

    loop = GLib.MainLoop()
    tools.prep_pipe(pipeline, loop)

    timeout = 2000  # ms

    # Changing fps using videorate element periodically
    change_prop_obj = tools.ChangeProp(elements_dict)

    # change_prop_obj.change_prop_cb will be called every 'timeout*2' milliseconds
    GLib.timeout_add(timeout * 2, change_prop_obj.change_prop_cb)

    # Changing effect with next_effect periodically
    blockpad = queue_1.get_static_pad('src')
    change_elem_obj = tools.ChangeElem(pipeline, cur_effect=effect, next_effect=next_effect, before_elem=convert_1,
                                       after_elem=convert_2, blockpad=blockpad)

    # change_elem_obj.change_elem_cb will be called every 'timeout' milliseconds
    GLib.timeout_add(timeout, change_elem_obj.change_elem_cb)

    loop.run()

    pipeline.set_state(Gst.State.NULL)
    del pipeline
