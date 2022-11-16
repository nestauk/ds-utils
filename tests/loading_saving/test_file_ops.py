import shutil
import os
from pathlib import Path
import sys
import pytest
from nesta_ds_utils.loading_saving import file_ops


@pytest.fixture
def test_output_path():
    """Generates pathlib.Path to dump intermediate test data.

    Yields:
        Output path to dump intermetiate test data.
    """
    test_output_path = file_ops._convert_str_to_pathlib_path("tests/temp/")
    file_ops.make_path_if_not_exist(test_output_path)
    yield test_output_path
    shutil.rmtree("tests/temp/")


def test_convert_str_to_pathlib_path(test_output_path: Path):
    """Tests that file_ops method convert_str_to_pathlib_path.
        returns type patlib.Path.

    Args:
        test_output_path (pathlib.Path): output path to dump intermetiate test data
    """
    assert isinstance(test_output_path, Path)


def test_path_exists(test_output_path: Path):
    """Tests that the path generated by file_ops method
        make_path_if_not_exist exists.

    Args:
        test_output_path (pathlib.Path): Output path to dump intermetiate test data.
    """
    assert test_output_path.exists()


def test_extract_zip_to_output_path(test_output_path: Path):
    """Tests that the file_ops method extractall dumped a
        text file to an output path and that text file could be read.

    Args:
        test_output_path (pathlib.Path): Output path to dump intermetiate test data.
    """
    file_ops.extractall(
        "tests/artifacts/dummy_zip.zip", test_output_path, delete_zip=False
    )

    with open("tests/temp/dummy_text_in_zip.txt", "r") as f:
        text = f.read()
        assert text == "'Hello World'"


def test_extract_zip_no_output_path():
    """Tests that the file_ops method extractall dumped a
    text file to the directory of the zip file.
    """
    file_ops.extractall("tests/artifacts/dummy_zip.zip", delete_zip=False)

    with open("tests/artifacts/dummy_text_in_zip.txt", "r") as f:
        text = f.read()
        assert text == "'Hello World'"

    os.remove("tests/artifacts/dummy_text_in_zip.txt")


def test_zip_not_deleted():
    """Tests that the zip file was not deleted when extractall
    was called without a delete_zip flag.
    """
    assert file_ops._convert_str_to_pathlib_path(
        "tests/artifacts/dummy_zip.zip"
    ).exists()
