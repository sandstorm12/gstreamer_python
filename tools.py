"""
This file contains a set of functions and classes which intend to make it easier to write gstreamer codes

The use-cases are shown in dynamic.py, add_remove_stream.py, tee.py

Created by Aref, Oct. 4 2020

"""

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


def prep_pipe(pipeline: Gst.Pipeline, loop: GLib.MainLoop) -> None:
    """
    Adds a message handler to the bus and connects the bus to the loop

    :param pipeline: A Gst.Pipeline object
    :param loop: Main loop of the program
    :return: None
    """

    bus = pipeline.get_bus()
    bus.add_signal_watch()

    pipeline.set_state(Gst.State.PLAYING)

    bus.connect("message", on_message, loop)



def on_message(bus: Gst.Bus, message: Gst.Message, loop: GLib.MainLoop) -> bool:
    mtype = message.type
    """
        Gstreamer Message Types and how to parse
        https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
    """
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()

    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(err, debug)
        loop.quit()

    elif mtype == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(err, debug)

    else:
        pass

    return True


def add_many(pipeline: Gst.Pipeline, *elements: Gst.Element) -> None:
    """
    Adds the elements to the pipeline using Gst.Bin.add()
    https://gstreamer.freedesktop.org/documentation/gstreamer/gstbin.html?gi-language=python#gst_bin_add

    Usage:  "
            pipeline = Gst.Pipeline()
            elems = make_many('videotestsrc', 'videoconvert', 'autovideosink')
            add_many(pipeline, *elems)
            "

    :param pipeline:
    :param elements: GstElement objects
    """

    for elem in elements:
        ret = pipeline.add(elem)
        if not ret:
            raise TypeError('{} could not be added to the pipeline'.format(elem))


def make_many(*elements_name: str) -> list:
    """
    Creates GstElements using Gst.ElementFactory.make()
    https://gstreamer.freedesktop.org/documentation/gstreamer/gstelementfactory.html?gi-language=python#gst_element_factory_make

    Usage: " elems = make_many('videotestsrc', 'videoconvert', 'autovideosink') "

    :param elements_name: plugin names
    :return: A list containing GstElement objects
    """
    element_objs = []
    for elem_name in elements_name:
        ret = Gst.ElementFactory.make(elem_name)
        if ret is not None:
            element_objs.append(ret)
        else:
            raise TypeError('{} is not a valid gst-plugin'.format(elem_name))

    return element_objs


def link_many(*elements: Gst.Element, debug: bool = False) -> None:
    """
    Link multiple GstElements using Gst.Element.link()
    Note: You should add the elemets to the same Gst.Bin (Gst.Pipeline) before linking them.
    https://gstreamer.freedesktop.org/documentation/gstreamer/gstelement.html?gi-language=python#gst_element_link

    Usage:  "
            pipeline = Gst.Pipeline()
            elems = make_many('videotestsrc', 'videoconvert', 'autovideosink')
            add_many(pipeline, *elems)
            link_many(*elems)
            "

    :param elements: GstElements provided in the order which is intended to be linked
    :param debug: Enables debugging
    """
    for i in range(len(elements)):
        if not i == len(elements) - 1:  # if it is not the last element in the list, link it with the next one
            elements[i].link(elements[i + 1])
            if debug:
                print('{} linked to {}'.format(elements[i], elements[i + 1]))


class ChangeProp(object):
    """
    A convenient class used to demonstrate how to change plugins' properties while the pipeline is running
    It is intended to be used with Glib.timeout_add
    https://gstreamer.freedesktop.org/documentation/application-development/advanced/pipeline-manipulation.html?gi-language=python#changing-format-in-a-playing-pipeline
    """

    def __init__(self, elements: dict):
        self.flag = False

        self.filter_1 = elements.get('filter_1')
        self.videorate = elements.get('videorate')

    def change_prop_cb(self) -> bool:

        if self.flag:
            Gst.util_set_object_arg(self.filter_1, 'caps', 'video/x-raw, width=640, height=480, framerate=30/1')
            self.videorate.set_property('max-rate', 30)
            print('fps30')

            self.flag = not self.flag

        else:
            Gst.util_set_object_arg(self.filter_1, 'caps', 'video/x-raw, width=640, height=480, framerate=5/1')
            self.videorate.set_property('max-rate', 5)
            print('fps5')
            self.flag = not self.flag

        return True


class ChangeElem(object):
    """
    A convenient class used to demonstrate how to swap plugins while the pipeline is running
    It is intended to be used with Glib.timeout_add
    https://gstreamer.freedesktop.org/documentation/application-development/advanced/pipeline-manipulation.html?gi-language=python#dynamically-changing-the-pipeline
    """

    def __init__(self, pipeline: Gst.Pipeline, cur_effect: Gst.Element, next_effect: Gst.Element,
                 before_elem: Gst.Element, after_elem: Gst.Element, blockpad: Gst.Pad):
        self.cur_effect = cur_effect
        self.next_effect = next_effect
        self.blockpad = blockpad
        self.pipeline = pipeline
        self.before_elem = before_elem
        self.after_elem = after_elem
        self.add_elem = True

    def change_elem_cb(self) -> bool:
        self.blockpad.add_probe(Gst.PadProbeType.BLOCK_DOWNSTREAM, self.pad_probe_cb)

        return True

    def pad_probe_cb(self, pad: Gst.Pad, info: Gst.PadProbeInfo) -> Gst.PadProbeReturn:
        pad.remove_probe(info.id)

        src_pad = self.cur_effect.get_static_pad('src')
        src_pad.add_probe(Gst.PadProbeType.BLOCK | Gst.PadProbeType.EVENT_DOWNSTREAM, self.event_probe_cb)

        sink_pad = self.cur_effect.get_static_pad('sink')
        sink_pad.send_event(Gst.Event.new_eos())

        return Gst.PadProbeReturn.OK

    def event_probe_cb(self, pad: Gst.Pad, info: Gst.PadProbeInfo) -> Gst.PadProbeReturn:
        pad.remove_probe(info.id)

        print('Switching from {} to {}'.format(self.cur_effect.name, self.next_effect.name))

        self.cur_effect.set_state(Gst.State.NULL)

        self.pipeline.remove(self.cur_effect)
        self.pipeline.add(self.next_effect)
        self.before_elem.link(self.next_effect)
        self.next_effect.link(self.after_elem)

        self.next_effect.set_state(Gst.State.PLAYING)

        self.cur_effect, self.next_effect = self.next_effect, self.cur_effect

        return Gst.PadProbeReturn.DROP


class AddRemoveStream(object):
    """

    This class is used to show how to add/disconnect a stream to a pipeline while it is running

    """

    def __init__(self, pipeline: Gst.Pipeline, add_periodically: bool = True):

        self.add_periodically = add_periodically
        self.pipeline = pipeline
        self.flag = True

        self.elems = make_many('videotestsrc', 'queue', 'videoconvert', 'fpsdisplaysink')
        self.src, self.queue, self.convert, self.sink = self.elems

    def add_remove_stream_cb(self) -> bool:

        if self.flag:
            self.pipeline.set_state(Gst.State.PAUSED)

            add_many(self.pipeline, *self.elems)
            link_many(*self.elems)

            self.pipeline.set_state(Gst.State.PLAYING)

            print('Stream added')
            self.flag = not self.flag

        else:

            self.pipeline.set_state(Gst.State.PAUSED)

            self.pipeline.remove(self.src)
            self.pipeline.remove(self.convert)
            self.pipeline.remove(self.sink)
            self.pipeline.remove(self.queue)

            self.pipeline.set_state(Gst.State.PLAYING)

            print('Stream removed')
            self.flag = not self.flag

        return True
