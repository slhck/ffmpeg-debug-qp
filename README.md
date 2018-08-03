# `ffmpeg_debug_qp`

Authors: Werner Robitza, Steve Göring

Synopsis: Prints QP values of input sequence on a per-frame basis to STDERR.

# Requirements

For building

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

For example on Ubuntu:

    sudo add-apt-repository ppa:jonathonf/ffmpeg-3
    sudp apt update
    sudo apt install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev
    sudo apt install build-essentials

Supported input:

- MPEG-2
- MPEG-4 Part 2
- H.264 / MPEG-4 Part 10 (AVC)

Supported formats:

- MPEG-4 Part 14
- H.264 Annex B bytestreams

# Usage

Build and run the tool:

    make
    ./ffmpeg_debug_qp test.mp4

The output will be as follows:

    ...
    [h264 @ 0x7fcf61813e00] nal_unit_type: X, nal_ref_idc: X
    [h264 @ 0x7fcf61813e00] New frame, type: X
    [h264 @ 0x7fcf61813e00] AABBCCDD...

Where in the above, AA is the QP value of the first macroblock, BB of the second, etc.
For every macroblock row, there will be another row printed per frame.

You can parse the values with the `parse-qp-output.py` script, e.g.

    $ ./ffmpeg-debug-qp test.mp4 2> qp-values.txt
    $ ./parse-qp-output.py qp-values.txt qp-values.json

This produces a JSON file that is easier to parse.

# Acknowledgement

This code is based on:

- the code from [Fredrik Pihl](https://gist.github.com/figgis/ea9ac513cdd99a10abf1)
- which is adapted from the code example `demuxing_decoding.c` by Stefano Sabatini

See also [this thread](https://ffmpeg.org/pipermail/libav-user/2015-May/008122.html) on the libav-user mailing list.

Test video part of Big Buck Bunny (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org

# License

MIT License

Copyright (c) 2016-2017 Werner Robitza, Steve Göring, Fredrik Pihl, Stefano Sabatini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
