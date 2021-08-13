"""
    A toy plugin that writes meta data in the buffer.
"""

import logging
import sys
from gstreamer import Gst, GObject, GLib, GstBase
# change this to change the meta data libraries path
sys.path.append('/home/kim/sensifai/gst-python-hacks/gst-metadata')
from gst_buffer_info_meta import write_meta
counter = 0


class AppsinkTest(GstBase.BaseTransform):
    GST_PLUGIN_NAME = 'appsink_example_plugin_meta'

    __gstmetadata__ = ("appsink_test_plugin",  # Name
                       "Filter",  # Transform
                       "A test plugin to show appsink funcionality,"
                       "It writes a counter meta data in buffer.",
                       # Description
                       "Kimiya Saadat")  # Author

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any())
                        )
    # sample property. can be deleted.
    __gproperties__ = {
        "int-prop": (GObject.TYPE_INT64,  # type
                     "integer prop",  # nick
                     "A property that contains an integer",  # blurb
                     1,  # min
                     GLib.MAXINT,  # max
                     1,  # default
                     GObject.ParamFlags.READWRITE  # flags
                     )
    }

    def __init__(self):
        super(AppsinkTest, self).__init__()

    def do_get_property(self, prop: GObject.GParamSpec):
        if prop.name == 'int-prop':
            return self.int_prop
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop: GObject.GParamSpec, value):
        if prop.name == 'int-prop':
            self.int_prop = value
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_transform_ip(self, buffer: Gst.Buffer) -> Gst.FlowReturn:
        global counter
        try:
            counter += 1
            print("sent", counter)
            write_meta(buffer, description=str(counter))
        except Exception as e:
            logging.error(e)
        return Gst.FlowReturn.OK


GObject.type_register(AppsinkTest)
__gstelementfactory__ = (AppsinkTest.GST_PLUGIN_NAME,
                         Gst.Rank.NONE, AppsinkTest)
