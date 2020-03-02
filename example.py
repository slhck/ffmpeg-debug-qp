import argparse
import parse_qp_output

def main():
    parser = argparse.ArgumentParser(description="Parse QP values from ffmpeg-debug-qp")
    parser.add_argument("video", type=str, help="Video file to generate output for")
    parser.add_argument("-o", "--output", help="Output file (defaults to LD-JSON)")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
    parser.add_argument("-of", "--output-format", default="ld-json", help="Output format, one of: ld-json (default), json or csv")
    parser.add_argument("-p", "--path-to-tool", required=False, default="./", help="Path to ffmpeg-debug-qp")
    parser.add_argument("-m", "--include-macroblock-data", action="store_true", help="Include macroblock-level data")

    args = vars(parser.parse_args())
    parse_qp_output.set_path(args["path_to_tool"])
    if parse_qp_output.extract_qp_data(args["video"], args["output"], macroblock_data=args["include_macroblock_data"], force=args["force"], output_format=args["output_format"]):
        print("Success!")
    
if __name__ == '__main__':
    main()
