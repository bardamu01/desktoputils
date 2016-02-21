#!/bin/bash

# A script that helps with downscaling a video to half its size. 
# Note, also does video recompression. Original audio is preserved.
#  
# Example usage: $0 input.mp4 output.mp4
# 
# Known to be working with:
# * mp4 video:h264, audio:aac


input=$1
output=$2

tmppath=/tmp/video_conversion/

inputbn=`basename $1`
original_video_no_sound=$tmppath/original_video_no_sound_$inputbn
downsized_video_no_sound=$tmppath/downsized_no_sound_$inputbn
original_sound=$tmppath/original_sound_$inputbn.aac 

echo Working in $tmppath
mkdir -p $tmppath

echo Extracting just video from video
ffmpeg -i $input -c copy -an  ${original_video_no_sound}

echo Extracting audio from video
ffmpeg -i $input -vn -acodec copy ${original_sound}

echo Downscaling video by half
ffmpeg -strict -2 -i ${original_video_no_sound} -vf scale=iw/2:-1 ${downsized_video_no_sound}

echo Adding audio back
ffmpeg -i ${downsized_video_no_sound} -i ${original_sound} -bsf:a aac_adtstoasc -codec copy -shortest $output

echo Cleaning up temporary files
rm -rf $tmppath

echo "Done! :) Check out: $output"


