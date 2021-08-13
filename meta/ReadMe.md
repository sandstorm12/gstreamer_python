# Meta-data
Each buffer in GStream could be accompanied by meta-data. Using meta-data in python needs especial bindings that are explained here:

> http://lifestyletransfer.com/how-to-add-metadata-to-gstreamer-buffer-in-python/

In these examples, the pickle library is used to serialize and deserialize a custom python object. The meta is written:

    write_meta(buffer, str(pickle.dumps(meta)))

And read:

    buffer_info_meta = get_meta(buffer)
    buffer_info_meta = buffer_info_meta.description.decode('utf-8')
    meta = pickle.loads(eval(buffer_info_meta))

## How to run?
> gst-launch-1.0 mixer name=m ! videoconvert ! autovideosink videotestsrc ! m. videotestsrc pattern=ball ! m. videotestsrc pattern=snow ! m.
