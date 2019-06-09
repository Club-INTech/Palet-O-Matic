#! bin/bash

echo $1
if [ ! -e tmp ]; then
    mkdir ./tmp
fi
#v4l2-ctl -d /dev/video2 --set-ctrl=saturation=200
v4l2-ctl -d /dev/video0 --set-ctrl=saturation=128

ffmpeg -f video4linux2 -s 1920x1080 -i /dev/video0 -vframes 1 ./tmp/$1.jpg
