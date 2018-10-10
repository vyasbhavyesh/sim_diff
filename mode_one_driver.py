# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:24:41 2018

@author: bhavyas
"""
import diff_cli as cli
import single_compare

def mode_one():
    print("Choose file type\n 1- CSV\n 2- Excel")
    file_type = int(input())
    
    if file_type == 1:
        pre_file, post_file = cli.get_file_names()
        pre, post = cli.read_csv_input(pre_file, post_file)
    elif file_type == 2:
        pre_file, post_file = cli.get_file_names()
        pre, post = cli.read_xls_input(pre_file, post_file)
    
    cols = list(pre.columns)
    
    primary_key = cli.get_pri_key(cols)
    unimportant_cols = cli.get_drop_cols(cols)
    tolerance = cli.get_tolerance()
    dest_path = cli.get_report_dest()
    
    single_compare.single_compare(pre, post, unimportant_cols, primary_key, tolerance, dest_path)

