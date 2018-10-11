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


print("Choose file type\n 1- CSV\n 2- Excel")
file_type = int(input())

if file_type == 1:    
    pre, post = cli.read_csv_input(pre_files[0], post_files[0])
elif file_type == 2:    
    pre, post = cli.read_xls_input(pre_files[0], post_files[0])    

cols = list(pre.columns)
    
primary_key = cli.get_pri_key(cols)
unimportant_cols = cli.get_drop_cols(cols)
tolerance = cli.get_tolerance()
dest_path = cli.get_report_dest()

for file in pre_files:
    pre_file = file
    post_file = file
    
    
    