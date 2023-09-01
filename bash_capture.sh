#!/bin/sh
ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 "$1"
