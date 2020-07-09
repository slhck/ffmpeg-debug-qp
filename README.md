# `ffmpeg_debug_qp`

[![Build status](https://ci.appveyor.com/api/projects/status/u4w9c6bas9bblbqw/branch/master?svg=true)](https://ci.appveyor.com/project/slhck/ffmpeg-debug-qp/branch/master)

Authors: Werner Robitza, Steve Göring, Pierre Lebreton, Nathan Trevivian

Synopsis: Prints QP values of input sequence on a per-frame, per-macroblock basis to STDERR.

- [Requirements](requirements)
    - [UNIX](unix)
    - [Windows](windows)
    - [macOS](macos)
    - [Supported scenarios](supported_scenarios)
- [Building](building)
    - [Building under UNIX/macOS](building_under_unix_and_macos)
    - [Building under Windows](windows)
- [Usage](usage)
- [Acknowledgement](acknowledgement)
- [License](license)

# Requirements

You need Python 3 and the `ffmpeg_debug_qp` binary, which you have to build yourself.

For Windows, you can use the pre-built binary for the master branch, which can be found here: https://ci.appveyor.com/api/projects/slhck/ffmpeg-debug-qp/artifacts/build.zip). Also download the DLL files from `build/dll.zip` and unzip them.

## UNIX

For building:

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

For example on Ubuntu:

    sudo apt update && apt install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev build-essential pkg-config

## Windows

For building:

- Visual Studio >= 2015 with C/C++ compiler installed with 64 bit support
- Depending libraries (FFmpeg) are provided along the project, therefore no extra libraries are needed.

## macOS

For building:

- [Homebrew](https://brew.sh/)

Then:

    brew install ffmpeg pkg-config

# Supported scenarios

Supported input:

- MPEG-2
- MPEG-4 Part 2
- H.264 / MPEG-4 Part 10 (AVC)

Supported formats:

- MPEG-4 Part 14
- H.264 Annex B bytestreams

# Building

## Building under UNIX and macOS

Simply run the command:

```
make
```

## Building under Windows

- Open the solution file "ffmpeg-debug-qp.sln" which can be found in `build\ffmpeg-debug-qp\`
- Make sure to compile in release mode (See the dropdown on the top menu bar. This is not necessary per-se, but beneficial for speed at runtime)
- Build the tool ctrl+shift+B
- The binary will be available in `build\bin\`, required DLL files can be found in the 7zip archive which can be found in `build\bin.7z`
- Copy DLL and binary to the root of the folder `ffmpeg-debug-qp` so depending scripts such as `parse-qp-output.py` can find the binary.

# Usage

The main tool is a python library that first calls to ffmpeg-debug-qp and then parses and outputs the results.

You can run the library directly via `python3 -m ffmpeg_debug_qp_parser`, or install it with `pip`:

```
pip3 install --user ffmpeg_debug_qp_parser
```

The tool options are as follows:

```
usage: __main__.py [-h] [-f] [-of OUTPUT_FORMAT] [-p PATH_TO_TOOL] [-l | -k]
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


## Example

To run a basic example:

    ffmpeg_debug_qp_parser input.mp4 output_file.json -m -of json

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

The frame and macroblock types are as per ffmpeg debug information. Same goes for segmentation and interlaced values.

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

Copyright (c) 2016-2020 Werner Robitza, Steve Göring, Fredrik Pihl, Stefano Sabatini, Nathan Trevivian

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
