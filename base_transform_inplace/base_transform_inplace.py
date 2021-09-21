import cv2
import logging
import numpy as np

from typing import Tuple
from gstreamer import Gst, GObject, GLib, GstBase
from gstreamer.utils import gst_buffer_with_caps_to_ndarray


FORMATS = "{RGBx,BGRx,xRGB,xBGR,RGBA,BGRA,ARGB,ABGR,RGB,BGR}"
CAP = f"video/x-raw,format={FORMATS},width=[1,2147483647]," + \
      "height=[1,2147483647],framerate=[0/1,2147483647/1]"

DEFAULT_KERNEL_SIZE = 3
DEFAULT_SIGMA_X = 1.0
DEFAULT_SIGMA_Y = 1.0


class GstGaussianBlur(GstBase.BaseTransform):
    GST_PLUGIN_NAME = 'base_transform_inplace'

    __gstmetadata__ = (
        "GaussianBlur",
        "Filter",
        "Apply Gaussian Blur to Buffer",
        "Taras Lishchenko <taras at lifestyletransfer dot com>"
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.from_string(CAP)
        ),
        Gst.PadTemplate.new(
            "sink",
            Gst.PadDirection.SINK,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.from_string(CAP)
        )
    )

    __gproperties__ = {
        "kernel": (
            GObject.TYPE_INT64,
            "Kernel Size",
            "Gaussian Kernel Size",
            1,
            GLib.MAXINT,
            DEFAULT_KERNEL_SIZE,
            GObject.ParamFlags.READWRITE
        ),
        "sigmaX": (
            GObject.TYPE_FLOAT,
            "Standart deviation in X",
            "Gaussian kernel standard deviation in X direction",
            1.0,
            GLib.MAXFLOAT,
            DEFAULT_SIGMA_X,
            GObject.ParamFlags.READWRITE
        ),
        "sigmaY": (
            GObject.TYPE_FLOAT,
            "Standart deviation in Y",
            "Gaussian kernel standard deviation in Y direction",
            1.0,
            GLib.MAXFLOAT,
            DEFAULT_SIGMA_Y,
            GObject.ParamFlags.READWRITE
        ),
    }

    def __init__(self):
        super(GstGaussianBlur, self).__init__()

        self.kernel_size = DEFAULT_KERNEL_SIZE
        self.sigma_x = DEFAULT_SIGMA_X
        self.sigma_y = DEFAULT_SIGMA_Y

    @static_method
    def gaussian_blur(img: np.ndarray, kernel_size: int = 3,
                  sigma: Tuple[int, int] = (1, 1)) -> np.ndarray:
        sigmaX, sigmaY = sigma

        blurred_image = cv2.GaussianBlur(
            img, (kernel_size, kernel_size),
            sigmaX=sigmaX, sigmaY=sigmaY
        )

        return blurred_image

    def do_get_property(self, prop: GObject.GParamSpec):
        if prop.name == 'kernel':
            return self.kernel_size
        elif prop.name == 'sigmaX':
            return self.sigma_x
        elif prop.name == 'sigmaY':
            return self.sigma_y
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop: GObject.GParamSpec, value):
        if prop.name == 'kernel':
            self.kernel_size = value
        elif prop.name == 'sigmaX':
            self.sigma_x = value
        elif prop.name == 'sigmaY':
            self.sigma_y = value
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_transform_ip(self, buffer: Gst.Buffer) -> Gst.FlowReturn:
        try:
            image = gst_buffer_with_caps_to_ndarray(
                buffer, self.sinkpad.get_current_caps()
            )

            image[:] = self.gaussian_blur(
                image, self.kernel_size, sigma=(self.sigma_x, self.sigma_y)
            )
        except Exception as e:
            logging.error(e)

        return Gst.FlowReturn.OK


GObject.type_register(GstGaussianBlur)
__gstelementfactory__ = (
    GstGaussianBlur.GST_PLUGIN_NAME,
    Gst.Rank.NONE, GstGaussianBlur
)
