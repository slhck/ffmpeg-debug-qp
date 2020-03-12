#!/usr/bin/env python3

import argparse
import parse_qp_output


def main():
    parser = argparse.ArgumentParser(description="Parse QP values from ffmpeg-debug-qp")
    parser.add_argument("video", metavar='video|datalog', type=str, help="Video file to generate output for")
    parser.add_argument("output", help="Output file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
    parser.add_argument(
        "-d",
        "--use-data-log-file",
        action="store_true",
        help="Use precalculated data-log file instead of the video",
    )
    parser.add_argument(
        "-of",
        "--output-format",
        default="ld-json",
        help="Output format, one of: ld-json (default), json or csv",
    )
    parser.add_argument(
        "-p",
        "--path-to-tool",
        required=False,
        default="/usr/local/bin/",
        help="Path to ffmpeg-debug-qp (defaults to /usr/local/bin/)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        "--include-macroblock-data",
        action="store_true",
        help="Include macroblock-level data, such as: type, interlaced and segmentation",
    )
    group.add_argument(
        "-a",
        "--compute-averages-only",
        action="store_true",
        help="Only compute the frame-average QPs",
    )

    args = parser.parse_args()
    parse_qp_output.set_path(args.path_to_tool)
    if parse_qp_output.extract_qp_data(
        args.video,
        args.output,
        compute_averages_only=args.compute_averages_only,
        macroblock_data=args.include_macroblock_data,
        force=args.force,
        output_format=args.output_format,
        logfile=args.use_data_log_file,
    ):
        print("Data extracted to: {0}".format(args["output"]))


if __name__ == "__main__":
    main()
