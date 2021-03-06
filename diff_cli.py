# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 16:50:09 2018

@author: bhavyas
"""
import pandas as pd
import os
import path_files

def get_file_names():
    print("Pre/Source File Path :")
    pre_file = input()
    print("Post/Target File Path :")
    post_file = input()
    
    return pre_file,post_file


def get_pri_key(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + str(cols[i]))
    print("\nSelect col no. for primary keys :")
    primary_key_no = list(map(int, input().strip().split()))
    primary_key = [cols[i] for i in primary_key_no]
    return primary_key


def get_drop_cols(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + str(cols[i]))
    print("\nSelect col no. of unimportent columns :")
    col_no = list(map(int, input().strip().split()))
    drop_cols = [cols[i] for i in col_no]
    return drop_cols


def get_tolerance():
    print("Give tolerance for decimal comparission :")
    tolerance = float(input())
    
    if tolerance:
        return tolerance
    else:
        return False


def read_csv_input(pre_path, post_path):
    df_pre = pd.read_csv(pre_path, low_memory = False)
    df_post = pd.read_csv(post_path, low_memory = False)
    
    return df_pre, df_post

def read_csv_input_without_header(pre_path, post_path):
    df_pre = pd.read_csv(pre_path, low_memory = False, header= None)
    col_pre = [str(i) for i in df_pre.columns]
    df_pre.columns = col_pre
    df_post = pd.read_csv(post_path, low_memory = False, header= None)
    col_post = [str(i) for i in df_post.columns]
    df_post.columns = col_post
    return df_pre, df_post

def read_xls_input(pre_path, post_path):
    df_pre = pd.read_excel(pre_path, low_memory = False)
    df_post = pd.read_excel(post_path, low_memory = False)
    
    return df_pre, df_post

def hande_unimportant(df_pre, df_post, unimportant_cols):
    df_pre = df_pre.fillna(0)
    df_post = df_post.fillna(0)
    
    df_pre = df_pre.drop(unimportant_cols,axis =1)
    df_post = df_post.drop(unimportant_cols,axis =1)
    
    return df_pre, df_post
    
def orphan_cols(df_pre, df_post):
    if list(df_pre.columns) == list(df_post.columns):
        return False, [False, False],[False, False],df_pre,df_post
    else:
        is_pre_orphan = False
        is_post_orphan = False
        
        df_pre_cols = set(df_pre.columns)
        df_post_cols = set(df_post.columns)
        
        orphan_cols_pre = df_pre_cols - df_post_cols
        print("Orphan columns in pre file:")
        print(orphan_cols_pre)
        orphan_cols_post = df_post_cols - df_pre_cols
        print("Orphan columns in post file:")
        print(orphan_cols_post)
        
        if orphan_cols_pre:
            df_pre = df_pre.drop(list(orphan_cols_pre),axis =1)
            is_pre_orphan = True
        if orphan_cols_post:
            df_post = df_post.drop(list(orphan_cols_post),axis =1)
            is_post_orphan = True
        
        return True, [is_pre_orphan, orphan_cols_pre], [is_post_orphan, orphan_cols_post], df_pre, df_post


def orphan_rows(df_pre, df_post, dest_path):
    pre_rows = set(df_pre.index.copy())
    post_rows = set(df_post.index.copy())
    
    df_orphan_rows_pre = pd.DataFrame()
    df_orphan_rows_post = pd.DataFrame()
    
    orphan_rows_pre = pre_rows-post_rows
    orphan_rows_post = post_rows-pre_rows
    #need more attention and testing
    same_rows = list(pre_rows - orphan_rows_pre)
    
    if not orphan_rows_pre and not orphan_rows_post:
        return False, [False, False],[False, False],df_pre,df_post
    else:
        os.mkdir(dest_path)
        is_pre_orphan = False
        is_post_orphan = False
        
        
        
        if orphan_rows_pre:
            is_pre_orphan = True
            df_orphan_rows_pre = df_pre.drop(same_rows)
            df_orphan_rows_pre.to_csv(dest_path + 'orphan_rows_pre.csv')
            print('Oprhan Row in pre written')
            df_pre = df_pre.drop(list(orphan_rows_pre))
        if orphan_rows_post:
            is_post_orphan = True
            df_orphan_rows_post = df_post.drop(same_rows)
            df_orphan_rows_post.to_csv(dest_path + 'orphan_rows_post.csv')
            print('Oprhan Row in post written')
            df_post = df_post.drop(list(orphan_rows_post))
    return True, [is_pre_orphan, len(df_orphan_rows_pre)], [is_post_orphan, len(df_orphan_rows_post)], df_pre, df_post

def drop_tolerance(diff_data, tolerance):
    l = len(diff_data)
    for item in diff_data:
        if type(item[2]) == float:
            if abs(item[2] - item[3]) < tolerance:
                diff_data.remove(item)
    if not l == len(diff_data):
        drop_tolerance(diff_data)
    
    return diff_data

def get_report_dest():
    print("Enter the destination for report: ")
    dest_path = input()
    os.mkdir(dest_path + '\\'+ 'report')
    
    return dest_path + '\\report\\'

def get_folder_paths():
    print('Enter path of pre folder')
    pre_path = input()
    pre_files = path_files.get_folder_files(pre_path)
    print('Enter path of post folder')
    post_path = input()
    post_files = path_files.get_folder_files(post_path)

    return pre_files, post_files