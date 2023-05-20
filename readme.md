### requirement
- python 3.11.3
- opencv-contrib-python-headless==4.7.0.72
- opencv-python-headless==4.7.0.72
- gunicorn==gunicorn
- falcon==3.1.1
- urllib3==2.0.2
- requests==2.30.0
- Pillow==9.5.0

### feature
Thumb with aspect ratio
Crop with parameter location
Flip
Rotate
Face Crop

### macos requirement
if you running this service in macOs please run install_certifi_macbook_fixed.py first

### access list
whitelist domain in config.json

### Examples
    Default:
        http://:8080/url?xxx.jpg #nothing happens
    Thumb with Aspect ratio:
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&a=xxx&q=xx
    Crop:
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&c=tl
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&c=rl
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&c=bl
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&c=br
        http://:8080/?url=xxx.jpg&w=xxx&h=xxx&c=center
    Flip:
        http://:8080/?url=xxx.jpg&f=true
    Rotate:
        http://:8080/?url=xxx.jpg&r=xx
    Overlay:
        http://:8080/?url=xxx.jpg&o=image
        http://:8080/?url=xxx.jpg&o=text
        http://:8080/?url=xxx.jpg&o=true
    FaceDetect:
        http://:8080/?url=xxx.jpg&face=detect
        http://:8080/?url=xxx.jpg&face=crop
