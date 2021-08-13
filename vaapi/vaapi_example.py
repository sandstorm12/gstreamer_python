"""
    python3 vaapi_example.py
    This program starts a toy pipeline that uses
    vaaapi for stream decoding.

"""

import time
import numpy as np
from gstreamer import GstContext, GstPipeline, GstApp, Gst, GstVideo
import gstreamer.utils as utils

counter = 0


def run_pipeline(command):
    print("program started")
    with GstContext():  # create GstContext (hides MainLoop)
        # create GstPipeline (hides Gst.parse_launch)
        with GstPipeline(command) as pipeline:
            while not pipeline.is_done:
                time.sleep(.1)


if __name__ == "__main__":
    DEFAULT_PIPELINE = utils.to_gst_string([
        "filesrc location = test.mp4", "qtdemux", "h264parse",
        "vaapidecodebin", "autovideosink"
    ])
    command = DEFAULT_PIPELINE
    counters = run_pipeline(command)
