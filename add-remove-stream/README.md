To add a stream to the pipeline while it's running we need to:

1. Set the pipeline's state to PAUSED.
2. Add the elements we want to the pipeline. 
3. Link them in the proper order.
4. Set the pipeline's state back to PLAYING.

        self.pipeline.set_state(Gst.State.PAUSED)
    
        add_many(self.pipeline, *self.elems)
        link_many(*self.elems)
    
        self.pipeline.set_state(Gst.State.PLAYING)


In order to remove a stream from the pipeline:

1. Set the pipeline's state to PAUSED.
2. Remove the elements from the pipeline.
3. Set the pipeline's state back to PLAYING.

        self.pipeline.set_state(Gst.State.PAUSED)

        self.pipeline.remove(self.src)
        self.pipeline.remove(self.queue)
        self.pipeline.remove(self.convert)
        self.pipeline.remove(self.sink)

        self.pipeline.set_state(Gst.State.PLAYING)


**Usage:**
    
from **add-remove-stream** directory: `$ python add_remove_stream.py`