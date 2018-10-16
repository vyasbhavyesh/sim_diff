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
    f =[]
    for i in range(len(pre_files)):
        if pre_files[i].stem == post_files[i].stem:
            f.append(True)
        else:
            f.append(False)
    
    if not all(f):
        extra_pre = set(pre_files) - set(post_files)
        extra_post = set(post_files) - set(pre_files)
        
        pre_files = list(set(pre_files) - extra_pre)
        post_files =  list(set(post_files) - extra_post)
    
    
    pre_files.sort()
    post_files.sort()
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
    
    for i  in range(len(pre_files)):
        pre_file = pre_files[i]
        post_file = post_files[i]
        if file_type == 1:
            pre, post = cli.read_csv_input(pre_file, post_file)
        elif file_type == 2:
            pre, post = cli.read_xls_input(pre_file, post_file)
        dest_path_i = dest_path + pre_files[i].stem + '\\'
        os.mkdir(dest_path_i)
        
        single_compare.single_compare(pre, post, unimportant_cols, primary_key, tolerance, dest_path_i)
        
        

    