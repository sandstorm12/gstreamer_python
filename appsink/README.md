# Appsink
> Examples for appsink usage.
##About
Appsink is a plugin for transmitting pipeline data into the application. to learn more check the [lifestyletransfer tutorial](lifestyletransfer.com/how-to-use-gstreamer-appsink-in-python/).
## Setup
you need to have gstreamer library and python bindings installed.
if you don't, follow this [link.](lifestyletransfer.com/how-to-install-gstreamer-python-bindings/)
Also, make sure you have the meta libraries for the second example. if you don't read below. 
## Meta libraries   
Get the meta libraries from [here.](https://github.com/jackersson/gst-python-hacks)
install them as explained in the repository's readme.
Change the meta file path according to your meta library path in run_apsink_test_meta and appsink_test_plugin_meta.py:
```
sys.path.append('/home/kim/sensifai/gst-python-hacks/gst-metadata') -> change this to your meta library path
```

## Run examples
Run a simple example that uses appsink for recieving image data:
```shell
$  python3 appsink_example_for_image.py
```

The next example uses appsink_test_plugin_meta to write meta in the buffer and receives it with appsink.
Move to the project root and Add the plugin directory to your GST_PLUGIN_PATH:
```
export GST_PLUGIN_PATH=:$GST_PLUGIN_PATH:$PWD/gst/
```


Run:
```shell
$  python3 appsink_example_for_meta.py
```

