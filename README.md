# `ffmpeg_debug_qp`

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Authors: Werner Robitza, Steve Göring, Pierre Lebreton, Nathan Trevivian, Valerio Triolo

`ffmpeg-debug-qp` is based on ffmpeg and prints QP values of a video input on a per-frame, per-macroblock basis to STDERR.

The tool comes with an additional Python parser to help interpret the output.

**Contents:**

- [Download](#download)
- [Building from Source](#building-from-source)
  - [Requirements](#requirements)
  - [Building](#building)
  - [Installation](#installation)
- [Usage](#usage)
  - [Direct Usage](#direct-usage)
  - [Python Usage](#python-usage)
- [Developers: Static Build](#developers-static-build)
- [Acknowledgements](#acknowledgements)
- [Contributors](#contributors)
- [License](#license)

## Download

Pre-built static binaries are available for Linux and macOS (both x86_64 and ARM64):

**[Download the latest release](https://github.com/slhck/ffmpeg-debug-qp/releases/latest)**

These binaries have FFmpeg statically linked and require no additional dependencies.

## Building from Source

If you prefer to build from source, follow the instructions below.

### Requirements

- Python 3.9 or higher
- ffmpeg 8.x or higher libraries

### Linux

For building:

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

For example on Ubuntu:

    sudo apt -qq update && \
    sudo apt install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev build-essential pkg-config

### macOS

For building:

- [Homebrew](https://brew.sh/)

Then:

    brew install ffmpeg pkg-config

### Building

In order to use this tool, you need to build the `ffmpeg_debug_qp` binary.

If you have FFmpeg libraries installed on your system, simply run:

```bash
make
```

The binary will be created under `ffmpeg_debug_qp` in the same folder.

### Installation

You can add the binary to your `$PATH`, e.g. by copying it to `/usr/local/bin`:

```bash
sudo cp ./ffmpeg_debug_qp /usr/local/bin/
# or for static build:
sudo cp ./build/ffmpeg_debug_qp /usr/local/bin/
```

This way, you can call it from anywhere on your system.

## Usage

Run this tool on any of the supported file types:

- MPEG-2
- MPEG-4 Part 2
- H.264 / MPEG-4 Part 10 (AVC)

Supported formats:

- MPEG-4 Part 14
- H.264 Annex B bytestreams

### Direct Usage

Simply call the binary with the path to a file:

```console
./ffmpeg_debug_qp test/test.mp4
[h264 @ 0x124f043b0] New frame, type: I
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] << frame_type: I; pkt_size: 213 >>
[h264 @ 0x124f043b0] New frame, type: P
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
[h264 @ 0x124f043b0] 1111111111111111111111111111111111111111
```

You will see the QP values for each macroblock of every frame. Each pair of two numbers is a QP value, hence, in the above example, the QP values are `11`, `11` and so on.

### Python Usage

You can run the supplied Python tool that helps you parse the results from `ffmpeg_debug_qp`.

First, build the binary and add it to your `$PATH`.

Then, from the project directory, run via [uv](https://docs.astral.sh/uv/):

```bash
uv run ffmpeg-debug-qp-parser --help
```

Or install locally with pip:

```bash
pip install .
ffmpeg-debug-qp-parser --help
```

The tool options are as follows:

```
usage: ffmpeg-debug-qp-parser [-h] [-f] [-of OUTPUT_FORMAT] [-p PATH_TO_TOOL] [-l | -k]
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
                        Path to ffmpeg_debug_qp executable (will search in $PATH by default)
  -l, --use-logfile     Use precalculated logfile instead of the video
  -k, --keep-logfile    Don't remove the temporary logfile 'video.debug'
  -m, --include-macroblock-data
                        Include macroblock-level data, such as: type, interlaced and segmentation
  -a, --compute-averages-only
                        Only compute the frame-average QPs
```


#### Python Example

To run a basic example:

```
ffmpeg-debug-qp-parser input.mp4 output_file.json -m -of json
```

This reads the file `input.mp4` and produces a JSON file `output_file.json`, with a list of frames and each of their macroblocks in the format:

```json
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

## Developers: Static Build

To build a portable binary with FFmpeg statically linked, use CMake:

```bash
# Download and build minimal FFmpeg (first time only)
./util/build-ffmpeg.sh --download

# Build ffmpeg_debug_qp
cmake -B build -DUSE_VENDORED_FFMPEG=ON
cmake --build build
```

The binary will be created at `build/ffmpeg_debug_qp`. This binary only depends on system libraries and can be distributed without requiring FFmpeg to be installed.

To rebuild FFmpeg (e.g., after changes):

```bash
./util/build-ffmpeg.sh --clean    # Clean and reconfigure
./util/build-ffmpeg.sh            # Just rebuild
```

This is what is used inside GitHub Actions to provide prebuilt binaries for Linux and macOS.

## Acknowledgements

This code is based on:

- the code from [Fredrik Pihl](https://gist.github.com/figgis/ea9ac513cdd99a10abf1)
- which is adapted from the code example `demuxing_decoding.c` by Stefano Sabatini

See also [this thread](https://ffmpeg.org/pipermail/libav-user/2015-May/008122.html) on the libav-user mailing list.

Test video part of Big Buck Bunny (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://slhck.info/"><img src="https://avatars.githubusercontent.com/u/582444?v=4?s=100" width="100px;" alt="Werner Robitza"/><br /><sub><b>Werner Robitza</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=slhck" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ndtreviv"><img src="https://avatars.githubusercontent.com/u/1530653?v=4?s=100" width="100px;" alt="Nathan Trevivian"/><br /><sub><b>Nathan Trevivian</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=ndtreviv" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lars18th"><img src="https://avatars.githubusercontent.com/u/9989964?v=4?s=100" width="100px;" alt="Lars The"/><br /><sub><b>Lars The</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=lars18th" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/plebreton"><img src="https://avatars.githubusercontent.com/u/19344718?v=4?s=100" width="100px;" alt="plebreton"/><br /><sub><b>plebreton</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=plebreton" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/winking324"><img src="https://avatars.githubusercontent.com/u/7922054?v=4?s=100" width="100px;" alt="winking324"/><br /><sub><b>winking324</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=winking324" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://stg7.github.io/"><img src="https://avatars.githubusercontent.com/u/9373295?v=4?s=100" width="100px;" alt="Steve Göring"/><br /><sub><b>Steve Göring</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=stg7" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/valeriot30"><img src="https://avatars.githubusercontent.com/u/30567406?v=4?s=100" width="100px;" alt="Valerio Triolo"/><br /><sub><b>Valerio Triolo</b></sub></a><br /><a href="https://github.com/slhck/ffmpeg-debug-qp/commits?author=valeriot30" title="Code">💻</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

MIT License

Copyright (c) 2016-2025 Werner Robitza, Steve Göring, Fredrik Pihl, Stefano Sabatini, Nathan Trevivian, Valerio Triolo

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
