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
import itertools
import uuid


class SerializableGenerator(list):
    """Generator that is serializable by JSON
    https://stackoverflow.com/a/46841935/435093
    """

    def __init__(self, iterable):
        tmp_body = iter(iterable)
        try:
            self._head = iter([next(tmp_body)])
            self.append(tmp_body)
        except StopIteration:
            self._head = []

    def __iter__(self):
        return itertools.chain(self._head, *self[:1])


OUTPUT_FORMATS = ["ld-json", "json", "csv"]


def run_command(cmd, dry_run=False, verbose=False):
    """
    Run a command directly
    """
    if dry_run or verbose:
        print_stderr("[cmd] " + " ".join(cmd))
        if dry_run:
            return None, None

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        print_stderr("[error] running command: {}".format(" ".join(cmd)))
        print_stderr(stderr.decode("utf-8"))
        sys.exit(1)


def print_stderr(msg):
    print(msg, file=sys.stderr)


def average(x):
    if not isinstance(x, list):
        print_stderr("Cannot use average() on non-list!")
        sys.exit(1)
    if not x:
        return []
    return sum(x) / len(x)


def generate_logfile(
    video_filename, force=False, include_macroblock_data=False, custom_path=None
):
    ff = os.path.join(custom_path, "ffmpeg_debug_qp")
    if not os.path.isfile(ff):
        print_stderr("Could not find executable at " + str(ff))
        sys.exit(1)

    # TODO: Turn this into a tempfile?
    if video_filename == "-":
        # Using PIPE input
        output_filename = "video." + uuid.uuid4().hex + ".debug"
        video_filename = "pipe:"
    else:
        output_filename = video_filename + ".debug"
    if not os.path.exists(output_filename) or force:
        args = [ff, video_filename]
        if include_macroblock_data:
            args.append("-m")

        with open(output_filename, "w") as outfile:
            result = subprocess.check_call(
                args, stdout=outfile, stderr=subprocess.STDOUT
            )
        if result != 0:
            raise RuntimeError("Error running ffmpeg_debug_qp")
    return output_filename


def parse_logfile(input_file, compute_averages_only, include_macroblock_data):
    if not input_file.endswith(".debug"):
        print_stderr(
            "You attempted to parse a logfile, but supplied a video file name as input"
        )
        sys.exit(1)

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
            if (
                "[h264" not in line
                and "[mpeg2video" not in line
                and "pkt_size" not in line
            ):
                continue

            # skip irrelevant other lines
            if (
                "nal_unit_type" in line
                or "Reinit context" in line
                or "Skipping" in line
            ):
                continue

            # start a new frame
            if "New frame" in line:
                if has_current_frame_data:
                    # yield the current frame
                    frame_data = {"frameType": frame_type, "frameSize": frame_size}

                    if include_macroblock_data:
                        frame_data["qpAvg"] = average(
                            [x["qp"] for x in frame_qp_values]
                        )
                        frame_data["qpValues"] = frame_qp_values
                    else:
                        frame_data["qpAvg"] = average(frame_qp_values)

                    if not compute_averages_only:
                        frame_data["qpValues"] = frame_qp_values

                    yield frame_data
                first_frame_found = True

                frame_type = line[-1]
                if frame_type not in ["I", "P", "B"]:
                    print_stderr(
                        "Wrong frame type parsed: "
                        + str(frame_type)
                        + "\n Offending LINE : "
                        + line
                    )
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
                if (
                    set(line.split("] ")[1]) - set(" 0123456789PAiIdDgGS><X+-|?=")
                    != set()
                ):
                    # this line contains something that is not a qp value
                    continue

                # Now we have a line with qp values.
                # Strip the first part off the string, e.g.
                #   [h264 @ 0x7f9fb4806e00] 25i  26i  25i  30i  25I  25i  25i  25i  28i  26i  25I  26i  28i  32i  25i  25I  25i  25i  28i  26i
                # becomes:
                #   25i  26i  25i  30i  25I  25i  25i  25i  28i  26i  25I  26i  28i  32i  25i  25I  25i  25i  28i  26i
                #   [h264 @ 0x7fadf2008000] 1111111111111111111111111111111111111111
                # OR
                # becomes:
                #   1111111111111111111111111111111111111111
                # Note:
                # Single digit qp values are padded with a leading space e.g.:
                # [h264 @ 0x7fadf2008000]  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                raw_values = re.sub(r"\[[\w\s@]+\]\s", "", line)
                if include_macroblock_data:
                    # remove the leading space in case of single digit qp values
                    line_qp_values = [
                        {
                            "qp": int(x.group(1)),
                            "type": x.group(2),
                            "segmentation": x.group(3).strip(),
                            "interlaced": x.group(4).strip(),
                        }
                        for x in re.finditer(
                            "([0-9]{1,})([PAiIdDgGS><X]{1})([ +-|?]{1})([ =]{1})",
                            raw_values,
                        )
                    ]
                    frame_qp_values.extend(line_qp_values)
                else:
                    # remove the leading space in case of single digit qp values
                    line_qp_values = [
                        int(raw_values[i : i + 2].lstrip())
                        for i in range(0, len(raw_values), 2)
                    ]
                    frame_qp_values.extend(line_qp_values)
                continue
            if "pkt_size" in line:
                frame_size = int(re.findall(r'\d+', line[line.rfind("pkt_size"):])[0])

        # yield last frame
        if has_current_frame_data:
            frame_data = {"frameType": frame_type, "frameSize": frame_size}

            if include_macroblock_data:
                frame_data["qpAvg"] = average([x["qp"] for x in frame_qp_values])
                frame_data["qpValues"] = frame_qp_values
            else:
                frame_data["qpAvg"] = average(frame_qp_values)

            if not compute_averages_only:
                frame_data["qpValues"] = frame_qp_values
            yield frame_data


def print_data_header():
    return "frame_type,frame_size,qp_avg"


def format_line(data, data_format="ld-json"):
    if data_format == "ld-json":
        return json.dumps(data)
    elif data_format == "csv":
        ret = []
        for _, v in data.items():
            if isinstance(v, list) and len(v) == 1:
                ret.append(str(v[0]))
            elif isinstance(v, list) and len(v) > 1:
                if isinstance(v[0], int):
                    ret.append(",".join([str(x) for x in v]))
                else:
                    ret.append(",".join([str(x["qp"]) for x in v]))
            else:
                ret.append(str(v))
        return ",".join(ret)
    else:
        raise RuntimeError("Wrong format, use ld-json or csv!")


def extract_qp_data(
    video,
    output,
    compute_averages_only=False,
    include_macroblock_data=False,
    force=False,
    output_format="ld-json",
    use_logfile=False,
    keep_logfile=False,
    custom_path=None,
):
    if video != "-" and not os.path.isfile(video):
        raise ValueError("No such video|logfile file: " + video)

    if output_format not in OUTPUT_FORMATS:
        raise ValueError(
            "Invalid output format! Must be one of: " + ", ".join(OUTPUT_FORMATS)
        )

    # Generate the logfile
    logfile = None
    try:
        if os.path.isfile(output) and not force:
            raise RuntimeError(
                "Output " + output + " already exists; use force=True to overwrite"
            )

        if not use_logfile:
            logfile = generate_logfile(
                video,
                force=force,
                include_macroblock_data=include_macroblock_data,
                custom_path=custom_path,
            )
        else:
            logfile = video

        if output_format == "json":
            # dump everything to the file
            with open(output, "w") as of:
                json.dump(
                    SerializableGenerator(
                        parse_logfile(
                            logfile, compute_averages_only, include_macroblock_data
                        )
                    ),
                    of,
                )
                sys.exit(0)
        else:
            with open(output, "w") as of:
                if output_format == "csv":
                    of.write(print_data_header() + "\n")
                for data in parse_logfile(
                    logfile, compute_averages_only, include_macroblock_data
                ):
                    of.write(format_line(data, output_format) + "\n")

    except Exception as e:
        print_stderr("Error generating log: " + str(e))
        sys.exit(1)
    finally:
        # Delete the debug file
        if logfile and not use_logfile and not keep_logfile:
            os.remove(logfile)
