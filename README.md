# `ffmpeg_debug_qp`

[![Build status](https://ci.appveyor.com/api/projects/status/u4w9c6bas9bblbqw/branch/master?svg=true)](https://ci.appveyor.com/project/slhck/ffmpeg-debug-qp/branch/master)

Authors: Werner Robitza, Steve Göring, Pierre Lebreton, Nathan Trevivian

`ffmpeg-debug-qp` is based on ffmpeg and prints QP values of a video input on a per-frame, per-macroblock basis to STDERR.

The tool comes with an additional Python parser to help interpret the output.

**Contents:**

- [Requirements](#requirements)
    - [Linux](#linux)
    - [Windows](#windows)
    - [macOS](#macos)
- [Building](#building)
    - [Building under Linux and macOS](#building-under-linux-and-macos)
    - [Building under Windows](#building-under-windows)
- [Usage](#usage)
    - [Direct Usage](#direct-usage)
    - [Python Usage](#python-usage)
- [Acknowledgement](#acknowledgement)
- [License](#license)

# Requirements

- Python 3.6 or higher

## Linux

For building:

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

For example on Ubuntu:

    sudo apt -qq update && \
    sudo apt install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev build-essential pkg-config

## Building under Windows

For building:

- Visual Studio >= 2015 with C/C++ compiler installed with 64 bit support
- Depending libraries (FFmpeg) are provided along the project, therefore no extra libraries are needed.

## macOS

For building:

- [Homebrew](https://brew.sh/)

Then:

    brew install ffmpeg pkg-config

# Building

In order to use this tool, you need to build the `ffmpeg_debug_qp` binary.

For Windows, you can use the pre-built binary for the master branch, which can be found here: https://ci.appveyor.com/api/projects/slhck/ffmpeg-debug-qp/artifacts/build.zip). Also download the DLL files from `build/dll.zip` and unzip them.


## Building under Linux and macOS

Simply run the command:

```
make
```

The binary will be created under `ffmpeg_debug_qp` in the same folder.

You can add it to your `$PATH`, e.g. by copying it to `/usr/local/bin`:

```
sudo cp ./ffmpeg_debug_qp /usr/local/bin/
```

This way, you can call it from anywhere on your system.

## Building under Windows

- Open the solution file `ffmpeg-debug-qp.sln` which can be found in `build\ffmpeg-debug-qp\`
- Make sure to compile in release mode (See the dropdown on the top menu bar. This is not necessary per-se, but beneficial for speed at runtime)
- Build the tool with `Ctrl-Shift-B`
- The binary will be available in `build\bin\`, required DLL files can be found in the 7zip archive which can be found in `build\bin.7z`
- Copy DLL and binary to the root of the folder `ffmpeg-debug-qp` so depending scripts can find the binary.

# Usage

Run this tool on any of the supported file types:

- MPEG-2
- MPEG-4 Part 2
- H.264 / MPEG-4 Part 10 (AVC)

Supported formats:

- MPEG-4 Part 14
- H.264 Annex B bytestreams

## Direct Usage

Simply call the binary with the path to a file:

```
./ffmpeg_debug_qp test/test.mp4
[h264 @ 0x7fa9c780d200] nal_unit_type: 5(IDR), nal_ref_idc: 3
[h264 @ 0x7fa9c780d200] Format yuv420p chosen by get_format().
[h264 @ 0x7fa9c780d200] Reinit context to 320x192, pix_fmt: yuv420p
[h264 @ 0x7fa9c780d200] New frame, type: I
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
[h264 @ 0x7fa9c780d200] 1111111111111111111111111111111111111111
```

You will see the QP values for each macroblock of every frame. Each pair of two numbers is a QP value, hence, in the above example, the QP values are `11`, `11` and so on.

## Python Usage

You can run the supplied Python tool that helps you parse the results from `ffmpeg_debug_qp`.

First, build the binary and add it to your `$PATH`.

You can run the library directly via `python3 -m ffmpeg_debug_qp_parser`, or install it with `pip`:

```
pip3 install --user ffmpeg_debug_qp_parser
```

The tool options are as follows:

```
usage: ffmpeg_debug_qp_parser [-h] [-f] [-of OUTPUT_FORMAT] [-p PATH_TO_TOOL] [-l | -k]
                              [-m | -a]
                              video|logfile output

Parse QP values from ffmpeg-debug-qp

positional arguments:
  video|logfile         Video file to generate output for, or existing logfile
  output                Output file

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Overwrite output
  -of OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        Output format, one of: ld-json (default), json or csv
  -p PATH_TO_TOOL, --path-to-tool PATH_TO_TOOL
                        Path to ffmpeg-debug-qp (defaults to /usr/local/bin/)
  -l, --use-logfile     Use precalculated logfile instead of the video
  -k, --keep-logfile    Don't remove the temporary logfile 'video.debug'
  -m, --include-macroblock-data
                        Include macroblock-level data, such as: type,
                        interlaced and segmentation
  -a, --compute-averages-only
                        Only compute the frame-average QPs
```


### Python Example

To run a basic example:

```
ffmpeg_debug_qp_parser input.mp4 output_file.json -m -of json
```

This reads the file `input.mp4` and produces a JSON file `output_file.json`, with a list of frames and each of their macroblocks in the format:

```
  [
      {
          "frameType": "I",
          "frameSize": 7787,
          "qpAvg": 26.87280701754386,
          "qpValues": [
              {
                  "qp": 25,
                  "type": "i",
                  "segmentation": "",
                  "interlaced": ""
              },
              {
                  "qp": 26,
                  "type": "i",
                  "segmentation": "",
                  "interlaced": ""
              }, ...
```

The frame and macroblock types are as per ffmpeg debug information. The same goes for segmentation and interlaced values.

For example outputs, see:

* Line-delimited JSON
  * [Averages only](examples/example-avgs.ldjson)
  * [Macroblock data](examples/example-mbdata.ldjson)
* JSON
  * [Averages only](examples/example-avgs.json)
  * [Macroblock data](examples/example-mbdata.json)
* CSV
  * [Averages only](examples/example-avgs.csv)
  * [Macroblock data](examples/example-mbdata.csv)

# Acknowledgement

This code is based on:

- the code from [Fredrik Pihl](https://gist.github.com/figgis/ea9ac513cdd99a10abf1)
- which is adapted from the code example `demuxing_decoding.c` by Stefano Sabatini

See also [this thread](https://ffmpeg.org/pipermail/libav-user/2015-May/008122.html) on the libav-user mailing list.

Test video part of Big Buck Bunny (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org

# License

MIT License

Copyright (c) 2016-2021 Werner Robitza, Steve Göring, Fredrik Pihl, Stefano Sabatini, Nathan Trevivian

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

FFmpeg libraries are licensed under the GNU Lesser General Public License, version 2.1.
