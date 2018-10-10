# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:13:16 2018

@author: bhavyas
"""
import diff_cli as cli

pre_files, post_files = cli.get_folder_paths()

if not pre_files == post_files:
    extra_pre = set(pre_files) - set(post_files)
    extra_post = set(post_files) - set(pre_files)
    
    pre_files = set(pre_files) - extra_post
    post_files = set(post_files) - extra_post



for file in pre_files:
    pre_file = file
    post_file = file

    