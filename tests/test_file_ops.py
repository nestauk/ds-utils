import unittest
import zipfile
import shutil
from pathlib import Path
import sys
sys.path.insert(1, "../nesta_ds_utils/")
import file_ops


class TestFileOps(unittest.TestCase):
    """Unittest class associated with nesta_io methods
    
    To run all tests: python -m unittest test_file_ops.TestFileOps

    To run specific tests: python -m unittest test_file_ops.TestFileOps.[test_method]
    (ex: python -m unittest test_file_ops.TestFileOps.test_zip_extraction)
    
    """
    def setUp(self):
        self.outPath = file_ops._convert_str_to_pathlib_path("temp/zipContents")
        self.zipPath = file_ops._convert_str_to_pathlib_path("artifacts/dummy_zip.zip")
        file_ops.make_path_if_not_exist(self.outPath)
        file_ops.extractall("artifacts/dummy_zip.zip", self.outPath, delete_zip = False)
        file_ops.extractall("artifacts/dummy_zip.zip", delete_zip = False)
        
    def test_convert_str_to_pathlib_path(self):
        """tests that file_ops method convert_str_to_pathlib_path returns type patlib.Path
        """
        self.assertIsInstance(self.outPath,Path)
    
    def test_path_exists(self):
        """tests that the path generated by file_ops method make_path_if_not_exist exists
        """
        self.assertTrue(self.outPath.exists())
    
    def test_zip_extraction_with_outpath(self):
        """tests that the file_ops method extractall dumped a text file to an output path and that text file could be read
        """
        with open("temp/zipContents/dummy_text_in_zip.txt", "r") as f:
            text = f.read()
            self.assertEqual(text, "'Hello World'")
    
    def test_zip_extraction_no_outpath(self):
        """tests that the file_ops method extractall dumped a text file to the directory of the zip file
        """
        with open("artifacts/dummy_text_in_zip.txt", "r") as f:
            text = f.read()
            self.assertEqual(text, "'Hello World'")
    
    def test_zip_not_deleted(self):
        """tests that the zip file was not deleted when extractall was called without a delete_zip flag
        """
        self.assertTrue(self.zipPath.exists())
    
    def tearDown(self):
        shutil.rmtree("temp/")


if __name__ == "__main__":
    unittest.main()