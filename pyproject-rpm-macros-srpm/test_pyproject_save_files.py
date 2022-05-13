import pytest
import yaml

from pathlib import Path
from pprint import pprint

from pyproject_preprocess_record import parse_record, read_record, save_parsed_record

from pyproject_save_files import argparser, generate_file_list, BuildrootPath
from pyproject_save_files import main as save_files_main

DIR = Path(__file__).parent
BINDIR = BuildrootPath("/usr/bin")
DATADIR = BuildrootPath("/usr/share")
SITELIB = BuildrootPath("/usr/lib/python3.7/site-packages")
SITEARCH = BuildrootPath("/usr/lib64/python3.7/site-packages")

yaml_file = DIR / "pyproject_save_files_test_data.yaml"
yaml_data = yaml.safe_load(yaml_file.read_text())
EXPECTED_DICT = yaml_data["classified"]
EXPECTED_FILES = yaml_data["dumped"]
TEST_RECORDS = yaml_data["records"]
TEST_METADATAS = yaml_data["metadata"]


@pytest.fixture
def tldr_root(tmp_path):
    prepare_pyproject_record(tmp_path, package="tldr")
    return tmp_path


@pytest.fixture
def pyproject_record(tmp_path):
    return tmp_path / "pyproject-record"


def prepare_pyproject_record(tmp_path, package=None, content=None):
    """
    Creates RECORD from test data and then uses
    functions from pyproject_process_record to convert
    it to pyproject-record file which is then
    further processed by functions from pyproject_save_files.
    """
    record_file = tmp_path / "RECORD"
    pyproject_record = tmp_path / "pyproject-record"

    if package is not None:
        # Get test data and write dist-info/RECORD file
        record_path = BuildrootPath(TEST_RECORDS[package]["path"])
        record_file.write_text(TEST_RECORDS[package]["content"])
        if package in TEST_METADATAS:
            metadata_path = BuildrootPath(TEST_METADATAS[package]["path"]).to_real(tmp_path)
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(TEST_METADATAS[package]["content"])
        # Parse RECORD file
        parsed_record = parse_record(record_path, read_record(record_file))
        # Save JSON content to pyproject-record
        save_parsed_record(record_path, parsed_record, pyproject_record)
    elif content is not None:
        save_parsed_record(*content, output_file=pyproject_record)


@pytest.fixture
def output(tmp_path):
    return tmp_path / "pyproject_files"


def test_parse_record_tldr():
    record_path = BuildrootPath(TEST_RECORDS["tldr"]["path"])
    record_content = read_record(DIR / "test_RECORD")
    output = list(parse_record(record_path, record_content))
    pprint(output)
    expected = [
        str(BINDIR / "__pycache__/tldr.cpython-37.pyc"),
        str(BINDIR / "tldr"),
        str(BINDIR / "tldr.py"),
        str(SITELIB / "__pycache__/tldr.cpython-37.pyc"),
        str(SITELIB / "tldr-0.5.dist-info/INSTALLER"),
        str(SITELIB / "tldr-0.5.dist-info/LICENSE"),
        str(SITELIB / "tldr-0.5.dist-info/METADATA"),
        str(SITELIB / "tldr-0.5.dist-info/RECORD"),
        str(SITELIB / "tldr-0.5.dist-info/WHEEL"),
        str(SITELIB / "tldr-0.5.dist-info/top_level.txt"),
        str(SITELIB / "tldr.py"),
    ]
    assert output == expected


def test_parse_record_tensorflow():
    long = "tensorflow_core/include/tensorflow/core/common_runtime/base_collective_executor.h"
    record_path = SITEARCH / "tensorflow-2.1.0.dist-info/RECORD"
    record_content = [
        ["../../../bin/toco_from_protos", "sha256=hello", "289"],
        [f"../../../lib/python3.7/site-packages/{long}", "sha256=darkness", "1024"],
        ["tensorflow-2.1.0.dist-info/METADATA", "sha256=friend", "2859"],
    ]
    output = list(parse_record(record_path, record_content))
    pprint(output)
    expected = [
        str(BINDIR / "toco_from_protos"),
        str(SITELIB / long),
        str(SITEARCH / "tensorflow-2.1.0.dist-info/METADATA"),
    ]
    assert output == expected


def remove_others(expected):
    return [p for p in expected if not (p.startswith(str(BINDIR)) or p.endswith(".pth") or p.rpartition(' ')[-1].startswith(str(DATADIR)))]


@pytest.mark.parametrize("include_auto", (True, False))
@pytest.mark.parametrize("package, glob, expected", EXPECTED_FILES)
def test_generate_file_list(package, glob, expected, include_auto):
    paths_dict = EXPECTED_DICT[package]
    modules_glob = {glob}
    if not include_auto:
        expected = remove_others(expected)
    tested = generate_file_list(paths_dict, modules_glob, include_auto)

    assert tested == expected


def test_generate_file_list_unused_glob():
    paths_dict = EXPECTED_DICT["kerberos"]
    modules_glob = {"kerberos", "unused_glob1", "unused_glob2", "kerb*"}
    with pytest.raises(ValueError) as excinfo:
        generate_file_list(paths_dict, modules_glob, True)

    assert "unused_glob1, unused_glob2" in str(excinfo.value)
    assert "kerb" not in str(excinfo.value)


def default_options(output, mock_root, pyproject_record):
    return [
        "--output",
        str(output),
        "--buildroot",
        str(mock_root),
        "--sitelib",
        str(SITELIB),
        "--sitearch",
        str(SITEARCH),
        "--python-version",
        "3.7",  # test data are for 3.7,
        "--pyproject-record",
        str(pyproject_record)
    ]


@pytest.mark.parametrize("include_auto", (True, False))
@pytest.mark.parametrize("package, glob, expected", EXPECTED_FILES)
def test_cli(tmp_path, package, glob, expected, include_auto, pyproject_record):
    prepare_pyproject_record(tmp_path, package)
    output = tmp_path / "files"
    globs = [glob, "+auto"] if include_auto else [glob]
    cli_args = argparser().parse_args([*default_options(output, tmp_path, pyproject_record), *globs])
    save_files_main(cli_args)

    if not include_auto:
        expected = remove_others(expected)
    tested = output.read_text()
    assert tested == "\n".join(expected) + "\n"


def test_cli_no_pyproject_record(tmp_path, pyproject_record):
    output = tmp_path / "files"
    cli_args = argparser().parse_args([*default_options(output, tmp_path, pyproject_record), "tldr*"])

    with pytest.raises(FileNotFoundError):
        save_files_main(cli_args)


def test_cli_too_many_RECORDS(tldr_root, output, pyproject_record):
    # Two calls to simulate how %pyproject_install process more than one RECORD file
    prepare_pyproject_record(tldr_root,
                             content=("foo/bar/dist-info/RECORD", []))
    prepare_pyproject_record(tldr_root,
                             content=("foo/baz/dist-info/RECORD", []))
    cli_args = argparser().parse_args([*default_options(output, tldr_root, pyproject_record), "tldr*"])

    with pytest.raises(FileExistsError):
        save_files_main(cli_args)


def test_cli_bad_argument(tldr_root, output, pyproject_record):
    cli_args = argparser().parse_args(
        [*default_options(output, tldr_root, pyproject_record), "tldr*", "+foodir"]
    )

    with pytest.raises(ValueError):
        save_files_main(cli_args)


def test_cli_bad_option(tldr_root, output, pyproject_record):
    prepare_pyproject_record(tldr_root.parent, content=("RECORD1", []))
    cli_args = argparser().parse_args(
        [*default_options(output, tldr_root, pyproject_record), "tldr*", "you_cannot_have_this"]
    )

    with pytest.raises(ValueError):
        save_files_main(cli_args)


def test_cli_bad_namespace(tldr_root, output, pyproject_record):
    cli_args = argparser().parse_args(
        [*default_options(output, tldr_root, pyproject_record), "tldr.didntread"]
    )

    with pytest.raises(ValueError):
        save_files_main(cli_args)
