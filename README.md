# ffmpeg_debug_qp

Prints QP values of input sequence on a per-frame basis.

Requirements:

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

Usage:

    make
    ./ffmpeg_debug_qp test.mp4

Output:

    Frame_type: X ; pkt_size: XXX
    [h264 @ 0x7fcf61813e00] nal_unit_type: X, nal_ref_idc: X
    [h264 @ 0x7fcf61813e00] New frame, type: X
    [h264 @ 0x7fcf61813e00] AABBCCDD...

Where in the above, AA is the QP value of the first macroblock, BB of the second, etc.
For every macroblock row, there will be another row printed per frame.

## Acknowledgement

This code is based on:

- the code from [Fredrik Pihl](https://gist.github.com/figgis/ea9ac513cdd99a10abf1)
- which is adapted from the code example `demuxing_decoding.c` by Stefano Sabatini

See also [this thread](https://ffmpeg.org/pipermail/libav-user/2015-May/008122.html) on the libav-user mailing list.

Test video part of Big Buck Bunny (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org