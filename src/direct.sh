#!/usr/bin/env bash
v4l2-ctl -d /dev/video2 --set-ctrl=focus_auto=0

mplayer tv:// -tv driver=v4l2:device=/dev/video0:width=1920:height=1080
