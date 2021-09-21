# BaseTransform (Crop)

This sample is an example to demonstrate implementing a GStreamer plugin to modify a video stream. This plugin creates a new buffer for each frame and does not change the buffer in-place.

## Run example

```bash
gst-launch-1.0 videotestsrc ! videoconvert ! video/x-raw,format=BGR,width=320,height=240 ! base_transform left=20 top=20 bottom=20 right=20 ! videoconvert ! autovideosink
```

## Explaination


The main task is executed in the **do_transform** method. Input and output buffers are accessible in this function. Changing the output buffer content is enough to do the transformation.

```python
out_image[:] = cv2.copyMakeBorder(image, ...)
```

As the buffers are not modified in place, the output buffer can have different dimensions compared to the input buffer. The **do_fixate_caps** method is where the output buffer properties are set.


```python
new_format = othercaps.get_structure(0).copy()

new_format.fixate_field_nearest_int("width", width)
new_format.fixate_field_nearest_int("height", height)

print(new_format)
new_caps = Gst.Caps.new_empty()
new_caps.append_structure(new_format)
```

The **do_set_caps** does an interesting task. It can set the element to passthrough mode (which sends the input directly to the output) if the user's transformation is not valid.

```python
if in_h == out_h and in_w == out_w:
    self.set_passthrough(True)
```

## Urgent issues and future work
1. [nothing yet]


## Issues and future work
1. Refactor the example
2. Make copy-rights explicit
3. Make the example more interesting (vague)
