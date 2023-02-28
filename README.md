# `ffmpeg_debug_qp`

# ⚠️ DEPRECATED — This tool is deprecated and no longer maintained.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Build status](https://ci.appveyor.com/api/projects/status/u4w9c6bas9bblbqw/branch/master?svg=true)](https://ci.appveyor.com/project/slhck/ffmpeg-debug-qp/branch/master)

Authors: Werner Robitza, Steve Göring, Pierre Lebreton, Nathan Trevivian

`ffmpeg-debug-qp` is based on ffmpeg and prints QP values of a video input on a per-frame, per-macroblock basis to STDERR.

The tool comes with an additional Python parser to help interpret the output.

> **⚠️ Note:** This tool relies upon a “hack” to get the QP values. It is not guaranteed to work with all videos. It also does not work with ffmpeg 5.x or above. Use with caution.

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
- [Acknowledgements](#acknowledgements)
- [Contributors](#contributors)
- [License](#license)

## Requirements

- Python 3.8 or higher
- ffmpeg v4 libraries (⚠️ ffmpeg v5 or higher API is not supported)

### Linux

For building:

- libavdevice, libavformat, libavfilter, libavcodec, libswresample, libswscale, libavutil
- C compiler

For example on Ubuntu:

    sudo apt -qq update && \
    sudo apt install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev build-essential pkg-config

### Windows

For building:

- Visual Studio >= 2015 with C/C++ compiler installed with 64 bit support
- Depending libraries (FFmpeg) are provided along the project, therefore no extra libraries are needed.

### macOS

For building:

- [Homebrew](https://brew.sh/)

Then:

    brew install ffmpeg@4 pkg-config
    export PKG_CONFIG_PATH="/opt/homebrew/opt/ffmpeg@4/lib/pkgconfig

## Building

In order to use this tool, you need to build the `ffmpeg_debug_qp` binary.

For Windows, you can use the pre-built binary for the master branch, which can be found here: https://ci.appveyor.com/api/projects/slhck/ffmpeg-debug-qp/artifacts/build.zip). Also download the DLL files from `build/dll.zip` and unzip them.


### Building under Linux and macOS

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

### Building under Windows

- Open the solution file `ffmpeg-debug-qp.sln` which can be found in `build\ffmpeg-debug-qp\`
- Make sure to compile in release mode (See the dropdown on the top menu bar. This is not necessary per-se, but beneficial for speed at runtime)
- Build the tool with `Ctrl-Shift-B`
- The binary will be available in `build\bin\`, required DLL files can be found in the 7zip archive which can be found in `build\bin.7z`
- Copy DLL and binary to the root of the folder `ffmpeg-debug-qp` so depending scripts can find the binary.

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

### Python Usage

You can run the supplied Python tool that helps you parse the results from `ffmpeg_debug_qp`.

First, build the binary and add it to your `$PATH`.

You can run the library directly via `python3 -m ffmpeg_debug_qp_parser`, or install it with `pip` after downloading this repo:

```bash
pip3 install --user .
```

**Note:** Previous versions installed a `ffmpeg_debug_qp_parser` executable. To harmonize it with other tools, now the executable is called `ffmpeg-debug-qp-parser`. Please ensure you remove the old executable (e.g. run `which ffmpeg_debug_qp_parser` and remove the file).

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

Copyright (c) 2016-2023 Werner Robitza, Steve Göring, Fredrik Pihl, Stefano Sabatini, Nathan Trevivian

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
