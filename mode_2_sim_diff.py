# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:13:16 2018

@author: bhavyas
"""
import diff_cli as cli
import os
import single_compare

def mode_2():
    
    pre_files, post_files = cli.get_folder_paths()
    pre_names = [files.stem for files in pre_files ]
    post_names = [files.stem for files in post_files ]
    
    extra_pre = set(pre_names) - set(post_names)
    extra_post = set(post_names) - set(pre_names)
    if extra_pre:
        print(extra_pre)
        pre_names = list(set(pre_names) - extra_pre)
    if extra_post:
        print(extra_post)
        post_names =  list(set(post_names) - extra_post)
    
    pre_files = [file for file in pre_files if file.stem in pre_names]
    post_files = [file for file in post_files if file.stem in post_names]
    
    
    pre_files.sort()
    post_files.sort()
    print("Choose file type\n 1- CSV\n 2- Excel")
    file_type = int(input())
    if file_type == 1:
        print("Does File have header?\n Enter 0 for file without header\n 1 for file with header ")
        header_type = int(input())
        
    if file_type == 1 and header_type == 0:
        pre, post = cli.read_csv_input_without_header(pre_files[0], post_files[0])
    
    elif file_type == 1 and header_type == 1 :    
        pre, post = cli.read_csv_input(pre_files[0], post_files[0])
    elif file_type == 2:    
        pre, post = cli.read_xls_input(pre_files[0], post_files[0])    
    
    cols = list(pre.columns)
        
    primary_key = cli.get_pri_key(cols)
    unimportant_cols = cli.get_drop_cols(cols)
    tolerance = cli.get_tolerance()
    dest_path = cli.get_report_dest()
    
    for i  in range(len(pre_files)):
        pre_file = pre_files[i]
        post_file = post_files[i]
        if file_type == 1 and header_type == 0:
            pre, post = cli.read_csv_input_without_header(pre_file, post_file)
        elif file_type == 1 and header_type == 1:
            pre, post = cli.read_csv_input(pre_file, post_file)
        elif file_type == 2:
            pre, post = cli.read_xls_input(pre_file, post_file)
        dest_path_i = dest_path + pre_files[i].stem + '\\'
        os.mkdir(dest_path_i)
        print("Working on file:"+ str(pre_file.stem))
        single_compare.single_compare(pre, post, unimportant_cols, primary_key, tolerance, dest_path_i)
        print("Report generated for file:"+ str(pre_file.stem))
        

    