#! bin/bahs

echo $1
if [ ! -e tmp ]; then
    mkdir ./tmp
fi
ffmpeg -f video4linux2 -s 1920x1080 -i /dev/video0 -vframes 1 ./tmp/$1.jpg