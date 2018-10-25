# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:04:58 2018

@author: bhavyas
"""
import diff_cli as cli
import pandas as pd
import sim_diff_2
import multiprocessing

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

print("Files extra in pre folder = " + str(extra_pre))
print("Files extra in post folder = " + str(extra_post))

pre_files.sort()
post_files.sort()

print("Choose file type\n 1- CSV\n 2- Excel")
file_type = int(input())
if file_type == 1:
    print("Does File have header?\n Enter 0 for file without header\n 1 for file with header ")
    header_type = int(input())
    
if file_type == 1 and header_type == 0:
    pre = pd.read_csv(pre_files[0],nrows=2,header=None)

elif file_type == 1 and header_type == 1 :    
    pre = pd.read_csv(pre_files[0],nrows=2)
elif file_type == 2:    
    pre = pd.read_excel(pre_files[0])

cols = list(pre.columns)
    
primary_key = cli.get_pri_key(cols)
unimportant_cols = cli.get_drop_cols(cols)
tolerance = cli.get_tolerance()
dest_path = cli.get_report_dest()

static_info = {'pre':'',
               'post':'',
               'primary':primary_key,
               'unimportant':unimportant_cols,
               'dest':dest_path,
               'tolerance':tolerance}

info_list = []
for i in range(len(pre_files)):
    static_info['pre'] = pre_files[i]
    static_info['post'] = post_files[i]
    info_list.append(static_info)



def test(info):
    print(info)
    
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)              # start 4 worker processes

    result = pool.apply_async(test, (10,))   # evaluate "f(10)" asynchronously in a single process

    result = pool.map_async(test, info_list)


