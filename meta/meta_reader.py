import sys

# Appending the path to meta read/write packages
sys.path.append('/home/hamid/Desktop/gstreamer_test/' +
                'gst-python-plugins/gst-python-hacks/gst-metadata')

import time
import pickle
import logging
import traceback

from gstreamer import Gst, GObject, GLib, GstBase
from gst_buffer_info_meta import write_meta, remove_meta, get_meta


class GstGaussianBlur(GstBase.BaseTransform):
    GST_PLUGIN_NAME = 'meta_reader'

    __gstmetadata__ = ("MetaWriter",
                       "Filter",
                       "Writes meta to the passing buffers",
                       "Sentiligence")

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()))

    __gproperties__ = {}

    def __init__(self):
        super(GstGaussianBlur, self).__init__()

        self.counter = 0

    def do_get_property(self, prop: GObject.GParamSpec):
        raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop: GObject.GParamSpec, value):
        raise AttributeError('unknown property %s' % prop.name)

    def do_transform_ip(self, buffer: Gst.Buffer) -> Gst.FlowReturn:
        try:
            buffer_info_meta = get_meta(buffer)
            buffer_info_meta = buffer_info_meta.description.decode('utf-8')
            meta = pickle.loads(eval(buffer_info_meta))

            print('META:', meta)

            remove_meta(buffer)
        except Exception as e:
            logging.error(e)

        # print('INIT: do_transform_ip')

        return Gst.FlowReturn.OK


# Required for registering plugin dynamically
# Explained:
# http://lifestyletransfer.com/how-to-write-gstreamer-plugin-with-python/
GObject.type_register(GstGaussianBlur)
__gstelementfactory__ = (GstGaussianBlur.GST_PLUGIN_NAME,
                         Gst.Rank.NONE, GstGaussianBlur)
