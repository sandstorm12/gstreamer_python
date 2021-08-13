import gi
import os
import logging
import traceback

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GObject', '2.0')

from typing import List, Tuple
from gi.repository import Gst, GObject, GstBase, GLib


class GstTfDetectionPluginPy(Gst.Element):
    GST_PLUGIN_NAME = 'muxer'

    __gstmetadata__ = ("Muxer",
                       "Mux",
                       "Muxes all the frames into one stream",
                       "Sentiligence")

    _srctemplate = Gst.PadTemplate.new('src', Gst.PadDirection.SRC,
                                       Gst.PadPresence.ALWAYS,
                                       Gst.Caps.new_any())

    _sinktemplate = Gst.PadTemplate.new('sink_%u', Gst.PadDirection.SINK,
                                        Gst.PadPresence.REQUEST,
                                        Gst.Caps.new_any())

    __gsttemplates__ = (_srctemplate, _sinktemplate)

    __gproperties__ = {}

    def __init__(self):
        super(GstTfDetectionPluginPy, self).__init__()

        self.srcpad = Gst.Pad.new_from_template(self._srctemplate, 'src')
        self.add_pad(self.srcpad)

        self.sinks = []

    def chainfunc(self, pad: Gst.Pad, parent,
                  buffer: Gst.Buffer) -> Gst.FlowReturn:
        try:
            self.srcpad.push(buffer)

            return Gst.FlowReturn.OK
        except Exception as e:
            logging.error(e)
            traceback.print_exc()

            return Gst.FlowReturn.ERROR

    def do_request_new_pad(self, templ, name, caps):
        # Explanation how to init Pads
        # https://gstreamer.freedesktop.org/documentation/
        # plugin-development/basics/pads.html
        sinkpad = Gst.Pad.new_from_template(templ, name)

        # Set chain function
        # https://gstreamer.freedesktop.org/documentation/
        # plugin-development/basics/chainfn.html
        sinkpad.set_chain_function_full(self.chainfunc, None)

        # Set event function
        # https://gstreamer.freedesktop.org/documentation/
        # plugin-development/basics/eventfn.html
        sinkpad.set_event_function_full(self.eventfunc, None)

        self.add_pad(sinkpad)
        self.sinks.append(sinkpad)

        return sinkpad

    def do_get_property(self, prop: GObject.GParamSpec):
        raise AttributeError('Unknown property %s' % prop.name)

    def do_set_property(self, prop: GObject.GParamSpec, value):
        raise AttributeError('Unknown property %s' % prop.name)

    def eventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
        # Forwards event to SRC (DOWNSTREAM)
        # https://lazka.github.io/pgi-docs/Gst-1.0/callbacks.html#Gst.PadEventFunction

        # Ignoring EOS event to prevent pipeline from exiting
        print(event.type, event.type == Gst.EventType.EOS)
        if event.type == Gst.EventType.EOS:
            pass
        else:
            return self.srcpad.push_event(event)

    def srcqueryfunc(self, pad: Gst.Pad, parent, query: Gst.Query) -> bool:
        """ Forwards query bacj to SINK (UPSTREAM)
            https://lazka.github.io/pgi-docs/Gst-1.0/callbacks.html#Gst.PadQueryFunction

        :param parent: GstTfDetectionPluginPy
        """
        return self.sinkpad.query(query)

    def srceventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
        """ Forwards event back to SINK (UPSTREAM)
            https://lazka.github.io/pgi-docs/Gst-1.0/callbacks.html#Gst.PadEventFunction

        :param parent: GstTfDetectionPluginPy
        """
        return self.sinkpad.push_event(event)


# Required for registering plugin dynamically
# Explained:
# http://lifestyletransfer.com/how-to-write-gstreamer-plugin-with-python/
GObject.type_register(GstTfDetectionPluginPy)
__gstelementfactory__ = (GstTfDetectionPluginPy.GST_PLUGIN_NAME,
                         Gst.Rank.NONE, GstTfDetectionPluginPy)
