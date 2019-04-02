#!/usr/bin/env python3
#
# Author: Werner Robitza
#
# Parses output from ffmpeg-debug-qp script.
# Writes per-frame QP values in JSON format.

import os
import re
import argparse
import sys
import json


def print_stderr(msg):
    print(msg, file=sys.stderr)


def average(x):
    if not isinstance(x, list):
        print_stderr("Cannot use average() on non-list!")
        sys.exit(1)
    if not x:
        return []
    return sum(x) / len(x)


def parse_file(input_file, use_average=False):
    with open(input_file) as f:
        frame_index = -1
        first_frame_found = False
        has_current_frame_data = False

        frame_type = None
        frame_size = None
        frame_qp_values = []

        for line in f:
            line = line.strip()
            # skip all non-relevant lines
            if "[h264" not in line and "pkt_size" not in line:
                continue

            # skip irrelevant other lines
            if "nal_unit_type" in line or "Reinit context" in line:
                continue

            # start a new frame
            if "New frame" in line:
                if has_current_frame_data:
                    # yield the current frame
                    yield {
                        "frameType": frame_type,
                        "frameSize": frame_size,
                        "qpValues": frame_qp_values if not use_average else [average(frame_qp_values)]
                    }

                first_frame_found = True

                frame_type = line[-1]
                if frame_type not in ["I", "P", "B"]:
                    print_stderr("Wrong frame type parsed: " + str(frame_type))
                    sys.exit(1)
                frame_index += 1
                # initialize empty for the moment
                frame_qp_values = []
                frame_size = 0
                has_current_frame_data = True
                continue

            if not first_frame_found:
                # continue parsing
                continue

            if "[h264" in line and "pkt_size" not in line:
                if set(line.split("] ")[1]) - set(" 0123456789") != set():
                    # this line contains something that is not a qp value
                    continue
                # Now we have a line with qp values.
                # Strip the first part off the string, e.g.
                #   [h264 @ 0x7fadf2008000] 1111111111111111111111111111111111111111
                # becomes:
                #   1111111111111111111111111111111111111111
                # Note: 
                # Single digit qp values are padded with a leading space e.g.:
                # [h264 @ 0x7fadf2008000]  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                raw_values = re.sub(r'\[[\w\s@]+\]\s', '', line)
                # remove the leading space in case of single digit qp values
                line_qp_values = [int(raw_values[i:i + 2].lstrip())
                             for i in range(0, len(raw_values), 2)]
                # print_stderr("Adding QP values to frame with index " + str(frame_index))
                frame_qp_values.extend(line_qp_values)
                continue
            if "pkt_size" in line:
                frame_size = int(re.findall(r'\d+', line)[0])

        # yield last frame
        if has_current_frame_data:
            yield {
                "frameType": frame_type,
                "frameSize": frame_size,
                "qpValues": frame_qp_values if not use_average else [average(frame_qp_values)]
            }


def main():

    parser = argparse.ArgumentParser(
        description="Parse QP values from ffmpeg-debug-qp")
    parser.add_argument("input", type=str, help="Input log file")
    parser.add_argument("-o", "--output", help="Output LD-JSON file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
    parser.add_argument("-a", "--average", action="store_true", help="Calculate only average QP (efficiency)")

    args = vars(parser.parse_args())
    if not os.path.isfile(args["input"]):
        print_stderr("no such file: " + args["input"])
        sys.exit(1)

    if args["output"]:
        if os.path.isfile(args["output"]) and not args["force"]:
            print_stderr("output " + args["output"] + " already exists; use -f/--force to overwrite")
            sys.exit(1)

        with open(args["output"], 'w'):
            pass
        with open(args["output"], "a") as of:
            of.truncate()
            for data in parse_file(args["input"], args["average"]):
                of.write(json.dumps(data) + "\n")
    else:
        for data in parse_file(args["input"], args["average"]):
            print(json.dumps(data))


if __name__ == '__main__':
    main()
