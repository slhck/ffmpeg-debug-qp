import argparse
import parse_qp_output

def main():
    parser = argparse.ArgumentParser(description="Parse QP values from ffmpeg-debug-qp")
    parser.add_argument("video", type=str, help="Video file to generate output for")
    parser.add_argument("-o", "--output", help="Output file (should be LD-JSON)")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
    parser.add_argument("-c", "--csv", action="store_true", help="Write CSV output instead")
    parser.add_argument("-p", "--path-to-tool", required=False, default="./", help="Path to ffmpeg-debug-qp")

    args = vars(parser.parse_args())
    parse_qp_output.set_path(args["path_to_tool"])
    if parse_qp_output.extract_qp_data(args["video"], args["output"], force=args["force"], csv=args["csv"]):
        print("Success!")
    
if __name__ == '__main__':
    main()
