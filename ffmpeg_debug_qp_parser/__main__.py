#!/usr/bin/env python3

import argparse
from . import parse_qp_output


def main():
    parser = argparse.ArgumentParser(description="Parse QP values from ffmpeg-debug-qp")
    parser.add_argument(
        "video",
        metavar="video|logfile",
        type=str,
        help="Video file to generate output for, or existing logfile",
    )
    parser.add_argument("output", help="Output file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
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
        help="Path to ffmpeg_debug_qp executable (will search in $PATH by default)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--use-logfile",
        action="store_true",
        help="Use precalculated logfile instead of the video",
    )
    group.add_argument(
        "-k",
        "--keep-logfile",
        action="store_true",
        help="Don't remove the temporary logfile 'video.debug'",
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
    parse_qp_output.extract_qp_data(
        args.video,
        args.output,
        compute_averages_only=args.compute_averages_only,
        include_macroblock_data=args.include_macroblock_data,
        force=args.force,
        output_format=args.output_format,
        use_logfile=args.use_logfile,
        keep_logfile=args.keep_logfile,
        custom_path=args.path_to_tool,
    )


if __name__ == "__main__":
    main()
