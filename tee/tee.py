"""
This code is to show how to use 'tee' plugin to feed a single source to multiple stream branches

Created by Aref, Oct. 4 2020

"""

import sys

sys.path.append('..')
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

import tools

if __name__ == '__main__':
    Gst.init(None)

    pipe = Gst.Pipeline()
    elems = tools.make_many('videotestsrc', 'videoconvert', 'videoconvert', 'gaussianblur', 'fpsdisplaysink',
                            'fpsdisplaysink', 'tee', 'queue', 'queue')
    tools.add_many(pipe, *elems)

    src0, conv0, conv1, effect, sink0, sink1, tee0, queue0, queue1 = elems

    tools.link_many(src0, tee0, queue0, conv0, sink0)
    tools.link_many(tee0, queue1, conv1, sink1)

    loop = GLib.MainLoop()
    tools.prep_pipe(pipe, loop)

    loop.run()

    pipe.set_state(Gst.State.NULL)
    del pipe
