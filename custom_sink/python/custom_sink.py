#!/usr/bin/env python
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# sinkelement.py
# (c) 2005 Edward Hervey <edward@fluendo.com>
# (c) 2007 Jan Schmidt <jan@fluendo.com>
# Licensed under LGPL
#
# Small test application to show how to write a sink element
# in 20 lines in python and place into the gstreamer registry
# so it can be autoplugged or used from parse_launch.

#  $ GST_DEBUG=python:4 gst-launch-1.0 fakesrc num-buffers=10 ! custom_sink
# code src link:https://gitlab.freedesktop.org/gstreamer/gst-python/-/tree/master/examples/plugins/python
import gi

gi.require_version('GstBase', '1.0')
from gi.repository import Gst, GObject, GstBase

Gst.init(None)


#
# Simple Sink element created entirely in python
#
class MySink(GstBase.BaseSink):
    __gstmetadata__ = ('custom_sink', 'Sink', \
                       'Custom test sink element', 'Edward Hervey')

    __gsttemplates__ = Gst.PadTemplate.new("sink",
                                           Gst.PadDirection.SINK,
                                           Gst.PadPresence.ALWAYS,
                                           Gst.Caps.new_any())

    def do_render(self, buffer):
        print("custom sink render function")
        Gst.info("timestamp(buffer):%s" % (Gst.TIME_ARGS(buffer.pts)))
        return Gst.FlowReturn.OK


GObject.type_register(MySink)
__gstelementfactory__ = ("custom_sink", Gst.Rank.NONE, MySink)
