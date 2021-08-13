"""
    python3 appsink_example_for_meta.py
    This program starts a toy pipeline and recieves the meta data(counter)
    from the appsink_test_plugin
    Caution: locating this file in /gst/python may cause problems.
    leave this file elsewhere.

"""


import gstreamer.utils as utils
from gstreamer import GstContext, GstPipeline, GstApp, Gst, GstVideo
import sys
import typing as typ
import time
import numpy as np
# change this to change the meta data libraries path
sys.path.append('/home/kim/sensifai/gst-python-hacks/gst-metadata')
from gst_buffer_info_meta import get_meta


def extract_buffer(sample: Gst.Sample) -> np.ndarray:
    """Extracts Gst.Buffer from Gst.Sample and converts to np.ndarray"""

    buffer = sample.get_buffer()  # Gst.Buffer
    buffer_info_meta = get_meta(buffer)
    buffer_info_meta = buffer_info_meta.description.decode('utf-8')
    return buffer_info_meta


def on_buffer(sink: GstApp.AppSink, data: typ.Any) -> Gst.FlowReturn:
    """Callback on 'new-sample' signal"""
    # Emit 'pull-sample' signal
    # https://lazka.github.io/pgi-docs/GstApp-1.0/classes/AppSink.html#
    # GstApp.AppSink.signals.pull_sample
    print("sample is in buffer")
    sample = sink.emit("pull-sample")  # Gst.Sample

    if isinstance(sample, Gst.Sample):
        counter = extract_buffer(sample)
        data.append(counter)
        print("recieved {count}".format(count=counter))
        return Gst.FlowReturn.OK
    else:
        return Gst.FlowReturn.ERROR


def run_pipeline(command):
    print("program started")
    counters = []
    with GstContext():  # create GstContext (hides MainLoop)
        # create GstPipeline (hides Gst.parse_launch)
        with GstPipeline(command) as pipeline:
            # get AppSink
            appsink = pipeline.get_by_cls(GstApp.AppSink).pop(0)
            # subscribe to <new-sample> signal
            appsink.connect("new-sample", on_buffer, counters)
            while not pipeline.is_done:
                time.sleep(.1)
    return counters


if __name__ == "__main__":
    DEFAULT_PIPELINE = utils.to_gst_string([
        "videotestsrc num-buffers=100",
        "capsfilter caps=video/x-raw,format=RGB,width=640,height=480",
        "appsink_example_plugin_meta",
        "queue",
        "appsink emit-signals=True"
    ])

    command = DEFAULT_PIPELINE
    counters = run_pipeline(command)
    # pass the counters list as data input for on_buffer function.
    # this is how we transmit data from pipleline to application,
    # cause we can't use custom data return in on_buffer
    print("Total meta data recieved is:  ", counters)
