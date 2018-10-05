# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:18:30 2018

@author: bhavyas
code to get list of files from folder
"""

from pathlib import Path


def get_folder_files(path):
    source = Path(path)
    files = [files for files in source.iterdir()]
    return files
    