"""
    python3 appsink_test_image.py
    This program starts a toy pipeline and recieves the data(image)
    Caution: locating this file in /gst/python may cause problems.
    leave this file elsewhere.

"""

import time
import numpy as np
from gstreamer import GstContext, GstPipeline, GstApp, Gst, GstVideo
import gstreamer.utils as utils

counter = 0


def extract_buffer(sample: Gst.Sample) -> np.ndarray:
    """Extracts Gst.Buffer from Gst.Sample and converts to np.ndarray"""

    buffer = sample.get_buffer()  # Gst.Buffer

    caps_format = sample.get_caps().get_structure(0)  # Gst.Structure

    # GstVideo.VideoFormat
    video_format = GstVideo.VideoFormat.from_string(
        caps_format.get_value('format'))

    w, h = caps_format.get_value('width'), caps_format.get_value('height')
    c = utils.get_num_channels(video_format)

    buffer_size = buffer.get_size()
    shape = (h, w, c) if (h * w * c == buffer_size) else buffer_size
    array = np.ndarray(shape=shape,
                       buffer=buffer.extract_dup(0, buffer_size),
                       dtype=utils.get_np_dtype(video_format))

    return np.squeeze(array)  # remove single dimension if exists


def on_buffer(sink: GstApp.AppSink) -> Gst.FlowReturn:
    global counter
    counter += 1
    """Callback on 'new-sample' signal"""
    # Emit 'pull-sample' signal
    # https://lazka.github.io/pgi-docs/GstApp-1.0/classes/AppSink.html#
    # GstApp.AppSink.signals.pull_sample

    sample = sink.emit("pull-sample")  # Gst.Sample

    if isinstance(sample, Gst.Sample):
        array = extract_buffer(sample)
        print(
            "{count}: Received {type} with shape"
            " {shape} of type {dtype}".format(
                count=counter,
                type=type(array),
                shape=array.shape,
                dtype=array.dtype))
        return Gst.FlowReturn.OK

    return Gst.FlowReturn.ERROR


def run_pipeline(command):
    print("program started")
    with GstContext():  # create GstContext (hides MainLoop)
        # create GstPipeline (hides Gst.parse_launch)
        with GstPipeline(command) as pipeline:
            # get AppSink
            appsink = pipeline.get_by_cls(GstApp.AppSink).pop(0)
            # subscribe to <new-sample> signal
            appsink.connect("new-sample", on_buffer)
            while not pipeline.is_done:
                time.sleep(.1)


if __name__ == "__main__":
    DEFAULT_PIPELINE = utils.to_gst_string([
        "videotestsrc num-buffers=100",
        "capsfilter caps=video/x-raw,format=RGB,width=640,height=480",
        "queue",
        "appsink emit-signals=True"
    ])

    command = DEFAULT_PIPELINE
    counters = run_pipeline(command)
