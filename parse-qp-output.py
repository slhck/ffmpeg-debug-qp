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

def parse_file(input_file):
  all_frame_data = []
  with open(input_file) as f:
    frame_index = -1
    for line in f.readlines():
      line = line.strip()
      # skip all non-relevant lines
      if "[h264" not in line:
        continue
      # skip irrelevant other lines
      if "nal_unit_type" in line or "Reinit context" in line:
        continue
      # start a new frame
      if "New frame" in line:
        frame_type = line[-1]
        if frame_type not in ["I", "P", "B"]:
          print("Wrong frame type parsed: " + str(frame_type))
          sys.exit(1)
        frame_index += 1
        # print("Frame parsed, type " + frame_type + ", index: " + str(frame_index))
        all_frame_data.append({
          "frameType": frame_type,
          "qpValues": []
        })
        continue
      # Now we have a line with qp values.
      # Strip the first part off the string, e.g.
      #   [h264 @ 0x7fadf2008000] 1111111111111111111111111111111111111111
      # becomes:
      #   1111111111111111111111111111111111111111
      raw_values = re.sub(r'\[[\w\s@]+\]\s', '', line)
      qp_values = [int(raw_values[i:i+2]) for i in range(0, len(raw_values), 2)]
      # print("Adding QP values to frame with index " + str(frame_index))
      all_frame_data[frame_index]["qpValues"].extend(qp_values)

  print(json.dumps(all_frame_data))

def main():

    parser = argparse.ArgumentParser(description='Parse QP values from ffmpeg-debug-qp')
    parser.add_argument('input', type=str, help="Input log file")

    args = vars(parser.parse_args())
    if not os.path.isfile(args['input']):
      print("no such file: " + args['input'])
      sys.exit(1)
    parse_file(args['input'])

if __name__ == '__main__':
  main()