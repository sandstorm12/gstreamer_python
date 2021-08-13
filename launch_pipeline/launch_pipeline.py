import sys
import time
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gst, Gtk, GLib

Gst.init(None)


PIPELINE_SIMPLE = \
    "videotestsrc name=videosource pattern=ball" + \
    " ! videoconvert" + \
    " ! fpsdisplaysink"

PIPELINE_CAPS = \
    "videotestsrc name=videosource pattern=ball" + \
    " ! videoconvert" + \
    " ! videoscale" + \
    " ! videorate" + \
    " ! video/x-raw,format=BGRx,width=720,height=480,framerate=60/1" + \
    " ! videoconvert" + \
    " ! fpsdisplaysink"

PIPELINE_MIXER = \
    "videotestsrc name=videosource pattern=ball" + \
    " ! video/x-raw,format=RGBA,width=1280,height=720" + \
    " ! videobox left=-1280" + \
    " ! mixer." + \
    " videotestsrc name=videosource2 pattern=snow" + \
    " ! video/x-raw,format=RGBA,width=1280,height=720" + \
    " ! videobox left=0" + \
    " ! mixer." + \
    " videomixer name=mixer" + \
    " ! videoconvert" + \
    " ! autovideosink"

PIPELINE_TEE = \
    "videotestsrc name=videosource" + \
    " ! videoconvert" + \
    " ! t." + \
    " tee name=t" + \
    " ! queue" + \
    " ! fpsdisplaysink" + \
    " t." + \
    " ! queue" + \
    " ! fpsdisplaysink"

PIPELINE_FILE = \
    "filesrc location=/home/hamid/Desktop/test.mp4" + \
    " ! decodebin" + \
    " ! videoconvert" + \
    " ! fpsdisplaysink"

PIPELINE_STREAM = \
    "rtspsrc location=rtsp://wowzaec2demo.streamlock.net" +\
    "/vod/mp4:BigBuckBunny_115k.mov" + \
    " ! decodebin" + \
    " ! videoconvert" + \
    " ! fpsdisplaysink"


def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()

    return True


mainloop = GObject.MainLoop()

# pipeline = Gst.parse_launch(PIPELINE_SIMPLE)
# pipeline = Gst.parse_launch(PIPELINE_CAPS)
# pipeline = Gst.parse_launch(PIPELINE_MIXER)
# pipeline = Gst.parse_launch(PIPELINE_TEE)
# pipeline = Gst.parse_launch(PIPELINE_FILE)
pipeline = Gst.parse_launch(PIPELINE_STREAM)

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_call, mainloop)

# videotestsrc = pipeline.get_by_name("videosource")
# pattern = videotestsrc.get_property('pattern')
# print('PATTRN: {}'.format(pattern))
# videotestsrc.set_property('pattern', 'ball')

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()
