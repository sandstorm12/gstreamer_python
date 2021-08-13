# Muxer
To interleave the frames from multiple streams (or sources), we need a plugin that can read data from numerous src pads and queue them on a single sink pad. This plugin extends the Element class directly.

## How to run?
> gst-launch-1.0 muxer name=m videotestsrc ! m. videotestsrc ! m. m. ! videoconvert ! autovideosink

## Description
First of all, this plugin is implemented by directly extending the **Gst.Element**. **Gst.Element** gives us the possibility to use **REQUEST** and **SOMETIMES** pads. The management of pads and buffers are much flexible in **Gst.Element** extended classes.

    _sinktemplate = Gst.PadTemplate.new(
        'sink_%u', Gst.PadDirection.SINK,
        Gst.PadPresence.REQUEST,
        Gst.Caps.new_any()
    )

The **REQUEST** pads created when another element requests a pad. For example, if an unknown number of input streams are present, using **REQUEST** pads helps to generate a sufficient number of sink pads, like this example. The request pads are named based on the format given in the **PadTemplate**.
The **do_request_new_pad** creates new pads based on the requests for pads. Keeping a reference to the created pads helps better management of pads. The **eventfunc** given to each pad when created gives us the possibility to manage or filter events in the pipeline. Event's like EOS are important to filter as they can terminate the pipeline.

    sinkpad = Gst.Pad.new_from_template(templ, name)
    sinkpad.set_chain_function_full(self.chainfunc, None)
    sinkpad.set_event_function_full(self.eventfunc, None)

    self.add_pad(sinkpad)

    self.sinks.append(sinkpad)

**chainfunc** is where the actual buffer handling is happening. In this example, we just push the buffer received from all the sink pads to the single src pad that the element possesses.

    self.srcpad.push(buffer)
