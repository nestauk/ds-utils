from io import BytesIO
from typing import Union
from pathlib import Path
from xmlrpc.client import Boolean
import zipfile
import os
import boto3
from typing import List
S3 = boto3.resource("s3")


def _convert_str_to_pathlib_path(path: Union[Path, str]) -> Path:
    """Converts a path written as a string to pathlib format.

    :param path: file path in string format
    :type path: str or pathlib.path
    :return: path in pathlib format
    :rtype: pathlib.Path
    """
    return Path(path) if type(path) is str else path


def make_path_if_not_exist(path: Union[Path, str]):
    """Check if path exists, if it does not exist then create it.

    :param path: file path 
    :type path: pathlib.Path or str
    """
    path = _convert_str_to_pathlib_path(path)
    if not path.exists():
        path.mkdir(parents=True)


def extractall(
    zip_path: Union[Path, str], 
    out_path: Union[Path, str]=None, 
    delete_zip: Boolean = True):
    """Takes path to zipped file and extracts it to specified output path.
    
    :param zip_path: path to zipped file
    :type zip_path: str or pathlib.Path
    :param out_path: path where contents will be unzipped to
    :type out_path: str or pathlib.Path
    :param delete_zip: option to delete zip file after extracted
    :type delete_zip: Boolean
    """

    if out_path is None:
        out_path = zip_path.rsplit("/", 1)[0]

    make_path_if_not_exist(out_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_path)
    
    if delete_zip is True:
        os.remove(zip_path)


def get_s3_dir_files(bucket_name: str, dir_name: str='') -> List[str]:
    """Get a list of all files in bucket directory.

    Args:
        bucket_name (str): S3 bucket name
        dir_name (str, optional): S3 bucket directory name. Defaults to ''.

    Returns:
        List[str]: List of file names in bucket directory
    """

    my_bucket = S3.Bucket(bucket_name)
    return [
        object_summary.key
        for object_summary in my_bucket.objects.filter(Prefix=dir_name)
    ]