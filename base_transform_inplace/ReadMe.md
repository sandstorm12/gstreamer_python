# BaseTransform (GaussianBlur)

This example applies a gaussian blur filter on a video stream. The Gaussian filter is applied in-place, and no data is copied.

## Run example

```bash
python3 -m pip install -r requirements.txt

gst-launch-1.0 videotestsrc ! videoconvert ! video/x-raw,format=BGRx ! base_transform_inplace kernel=9 sigmaX=1.0 sigmaY=1.0 ! videoconvert ! autovideosink
```

## Explanation

First of all, correctly setting caps makes the negotiation phase smoother. Don't forget to set the width, height, and framerate properties in addition to the color-space properties. Setting element properties are straight-forward and are done in **do_set_property** method.
Here, the main method is the **do_transform_ip** method. The term "ip" stands for In Place. The numpy array corresponding to the buffer is obtained using:

```python
image = gst_buffer_with_caps_to_ndarray(
    buffer, self.sinkpad.get_current_caps()
)
```

And modifying the buffer is done through:

```python
image[:] = gaussian_blur(
    image, self.kernel_size, sigma=(self.sigma_x, self.sigma_y)
)
```

## Urgent issues and future work
1. [nothing yet]

## Issues and future work
1. [nothing yet]
