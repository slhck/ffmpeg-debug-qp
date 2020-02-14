#!/usr/bin/env python3
#
# Author: Werner Robitza
# Modifier: Nathan Trevivian
# 
# Parses output from ffmpeg-debug-qp script.
# Writes per-frame QP values in JSON or CSV format.

import os
import re
import sys
import json
import subprocess
import tempfile

PATH = "/usr/local/bin/";

def set_path(path):
    PATH = path

def print_stderr(msg):
    print(msg, file=sys.stderr)


def average(x):
    if not isinstance(x, list):
        print_stderr("Cannot use average() on non-list!")
        sys.exit(1)
    if not x:
        return []
    return sum(x) / len(x)

def generate_log(video_filename, force=False):
    # TODO: Turn this into a tempfile?
    output_filename = video_filename + ".debug"
    if not os.path.exists(output_filename) or force:
        result = subprocess.check_call([PATH + 'ffmpeg_debug_qp '+ video_filename + ' 2> ' + output_filename], stderr=subprocess.STDOUT, shell=True)
        if result != 0:
            raise
    return output_filename

def parse_file(input_file):
    with open(input_file) if input_file != "-" else sys.stdin as f:
        frame_index = -1
        first_frame_found = False
        has_current_frame_data = False

        frame_type = None
        frame_size = None
        frame_qp_values = []

        for line in f:
            line = line.strip()
            # skip all non-relevant lines
            if "[h264" not in line and "[mpeg2video" not in line and "pkt_size" not in line:
                continue

            # skip irrelevant other lines
            if "nal_unit_type" in line or "Reinit context" in line or "Skipping" in line:
                continue

            # start a new frame
            if "New frame" in line:
                if has_current_frame_data:
                    # yield the current frame
                    yield {
                        "frameType": frame_type,
                        "frameSize": frame_size,
                        "qpAvg": average([x['qp'] for x in frame_qp_values]),
                        "qpValues": frame_qp_values
                    }

                first_frame_found = True

                frame_type = line[-1]
                if frame_type not in ["I", "P", "B"]:
                    print_stderr("Wrong frame type parsed: " + str(frame_type) + "\n Offending LINE : " + line)
                    # instead of exiting overcome the error with an unkown type
                    #  sys.exit(1)
                    frame_type = "?"
                frame_index += 1
                # initialize empty for the moment
                frame_qp_values = []
                frame_size = 0
                has_current_frame_data = True
                continue

            if not first_frame_found:
                # continue parsing
                continue

            if ("[h264" in line or "[mpeg2video" in line) and "pkt_size" not in line:
                if set(line.split("] ")[1]) - set(" 0123456789") != set():
                    # this line contains something that is not a qp value
                    continue
                # Now we have a line with qp values.
                # Strip the first part off the string, e.g.
                #   [h264 @ 0x7f9fb4806e00] 25i  26i  25i  30i  25I  25i  25i  25i  28i  26i  25I  26i  28i  32i  25i  25I  25i  25i  28i  26i  
                # becomes:
                #   25i  26i  25i  30i  25I  25i  25i  25i  28i  26i  25I  26i  28i  32i  25i  25I  25i  25i  28i  26i  
                raw_values = re.sub(r'\[[\w\s@]+\]\s', '', line)
                # remove the leading space in case of single digit qp values
                line_qp_values = [{"qp": int(x.group(1)), "type": x.group(2), "segmentation": x.group(3), "interlaced": x.group(4)} for x in re.finditer("([0-9]{1,})([PAiIdDgGS><X]{1})([ +-|?]{1})([ =]{1})", raw_values)]

                frame_qp_values.extend(line_qp_values)
                continue
            if "pkt_size" in line:
                frame_size = int(re.findall(r'\d+', line)[0])

        # yield last frame
        if has_current_frame_data:
            yield {
                "frameType": frame_type,
                "frameSize": frame_size,
                "qpAvg": average([x['qp'] for x in frame_qp_values]),
                "qpValues": frame_qp_values
            }


def print_data_header():
    return "frame_type,frame_size,qp_values"


def format_data(data, data_format="json"):
    if data_format == "json":
        return(json.dumps(data))
    elif data_format == "csv":
        ret = []
        for _, v in data.items():
            if isinstance(v, list) and len(v) == 1:
                ret.append(str(v[0]))
            else:
                ret.append(str(v))
        return ",".join(ret)
    else:
        raise RuntimeError("Wrong format, use json or csv!")


def extract_qp_data(video, output, force=False, csv=False):
    target_format = "json" if not csv else "csv"

    if video != "-" and not os.path.isfile(video):
        raise "No such video file: " + video

    # Generate the debug file
    debug_file = generate_log(video, force)

    if os.path.isfile(output) and not force:
        raise "Output " + output + " already exists; use force=True to overwrite"

    with open(output, 'w'):
        pass
    with open(output, "a") as of:
        of.truncate()
        if target_format == "csv":
            of.write(print_data_header() + "\n")
        if target_format == "json":
            of.write("[")
        idx = 0
        for data in parse_file(debug_file):
            if idx > 0 and target_format == "json":
                of.write(",")
            of.write(format_data(data, target_format) + "\n")
            idx += 1
        if target_format == "json":
            of.write("]")

    # Delete the debug file
    os.remove(debug_file)