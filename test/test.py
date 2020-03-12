import os
import sys
import filecmp
import pytest

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.append(ROOT_PATH)

from ffmpeg_debug_qp_parser import __main__ as main
from ffmpeg_debug_qp_parser.parse_qp_output import run_command


@pytest.fixture
def test_file():
    return os.path.join(TEST_DIR_PATH, "test.mp4")


@pytest.fixture
def output_ldjson():
    f = os.path.join(TEST_DIR_PATH, "out.ldjson")
    yield f
    os.remove(f)


@pytest.fixture
def expected_output_ldjson():
    return os.path.join(TEST_DIR_PATH, "expected_out.ldjson")


@pytest.fixture
def output_csv():
    f = os.path.join(TEST_DIR_PATH, "out.csv")
    yield f
    os.remove(f)


@pytest.fixture
def expected_output_csv():
    return os.path.join(TEST_DIR_PATH, "expected_out.csv")


@pytest.fixture
def output_json():
    f = os.path.join(TEST_DIR_PATH, "out.json")
    yield f
    os.remove(f)


@pytest.fixture
def expected_output_json():
    return os.path.join(TEST_DIR_PATH, "expected_out.json")


@pytest.fixture(scope="session", autouse=True)
def binary():
    os.chdir(ROOT_PATH)
    run_command("make")
    binary = os.path.join(ROOT_PATH, "ffmpeg_debug_qp")
    yield binary
    if os.path.isfile(binary):
        os.remove(binary)


def run_with_opts(opts):
    base_opts = ["python3", "-m", "ffmpeg_debug_qp_parser"]
    base_opts.extend(opts)
    run_command(base_opts)


class TestParser:
    def test_ldjson_output(self, test_file, output_ldjson, expected_output_ldjson):
        """
        Test LDJSON output
        """

        run_with_opts([test_file, output_ldjson, "-p", ROOT_PATH])
        assert os.path.isfile(output_ldjson)
        assert filecmp.cmp(output_ldjson, expected_output_ldjson)

    def test_csv_output(self, test_file, output_csv, expected_output_csv):
        """
        Test CSV output
        """

        run_with_opts([test_file, output_csv, "-of", "csv", "-p", ROOT_PATH])
        assert os.path.isfile(output_csv)
        assert filecmp.cmp(output_csv, expected_output_csv)

    def test_json_output(self, test_file, output_json, expected_output_json):
        """
        Test JSON output
        """

        run_with_opts([test_file, output_json, "-of", "json", "-p", ROOT_PATH])
        assert os.path.isfile(output_json)
        assert filecmp.cmp(output_json, expected_output_json)
