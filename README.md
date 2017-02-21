# GiropticPyOsc

For use with Giroptic 360cam. Other 360° cams may work also, but are not tested.
This implementation is not feature complete and is not fully tested. More features are added in future releases.

Currently supported are:
* set capture mode
* take picture
* transfer last took picture to PC

More information:
* [Giroptic Open Spherical Camera on Scribd](https://de.scribd.com/document/321017362/Open-Spherical-Camera-API-Version-1-1-2#)
* [Open Spherical Camera API on Google Developers](https://developers.google.com/streetview/open-spherical-camera/)


## Usage

#### import package

```python
from giroptic_osc.cam360 import Giroptic360cam
```

#### connect to camera

```python
# default address is 192.168.1.168:80
cam = Giroptic360cam()
# if you have another address, port or use https
cam = Giroptic360cam(address='0.0.0.0', port=42, use_https=True)
```

#### take picture

```python
cam.take_image()
```

#### save to pc
```python
cam.save_last_file('C:/temp', 'tester')
```

#### set/get camera mode
```python
# camera modes: image, _video, _burst, _timelapse, _live
cam.set_capture_mode('image')
cam.get_capture_mode()
```

#### close connection
```python
cam.close_connection()
```



