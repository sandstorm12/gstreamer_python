This examples demonstrates how to use **tee** plugin to feed a single source to multiple stream branches.

Test pipeline:
    
    gst-launch-1.0 videotestsrc ! tee name = t t. ! queue ! videoconvert ! autovideosink t. ! queue ! videoconvert ! autovideosink
    
**Usage**: 

from **tee** directory:
`$ python tee.py`

Official document example:
https://gstreamer.freedesktop.org/documentation/tutorials/basic/multithreading-and-pad-availability.html?gi-language=c