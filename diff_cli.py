# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 16:50:09 2018

@author: bhavyas
"""
import pandas as pd

def get_file_names():
    print("Pre/Source File Path :")
    pre_file = input()
    print("Post/Target File Path :")
    post_file = input()
    
    return pre_file,post_file


def get_pri_key(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + cols[i])
    print("\nSelect col no. for primary keys :")
    primary_key_no = list(map(int, input().strip().split()))
    primary_key = [cols[i] for i in primary_key_no]
    return primary_key


def get_drop_cols(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + cols[i])
    print("\nSelect col no. of unimportent columns :")
    col_no = list(map(int, input().strip().split()))
    drop_cols = [cols[i] for i in col_no]
    return drop_cols


def get_tolerance():
    print("Give tolerance for decimal comparission :")
    tolerance = int(input())
    
    if tolerance:
        return tolerance
    else:
        return False


def read_csv_input(pre_path, post_path):
    df_pre = pd.read_csv(pre_path, low_memory = False)
    df_post = pd.read_csv(post_path, low_memory = False)
    
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
    
def orphan_cols(df_pre, df_post):
    if df_pre.colums == df_post.columns:
        return True, True, True
    else:
        is_pre_orphan = False
        is_post_orphan = False
        
        df_pre_cols = set(df_pre.colums)
        df_post_cols = set(df_post.columns)
        
        orphan_cols_pre = df_pre_cols - df_post_cols
        orphan_cols_post = df_post_cols - df_pre_cols
        
        if orphan_cols_pre:
            df_pre = df_pre.drop(list(orphan_cols_pre),axis =1)
            is_pre_orphan = True
        if orphan_cols_post:
            df_post = df_post.drop(list(orphan_cols_post),axis =1)
            is_post_orphan = True
        
        return False, is_pre_orphan, is_post_orphan


def orphan_rows(df_pre, df_post):
    pre_rows = set(df_pre.index.copy())
    post_rows = set(df_post.index.copy())
    
    
    orphan_rows_pre = pre_rows - post_rows
    orphan_rows_post = post_rows - pre_rows
    #need more attention and testing
    same_rows = list(pre_rows - orphan_rows_pre)
    
    if not orphan_rows_pre and not orphan_rows_post:
        return True, True, True
    else:
        is_pre_orphan = False
        is_post_orphan = False
        
        if orphan_rows_pre:
            is_pre_orphan = True
            df_orphan_rows_pre = df_pre.drop(same_rows)
            df_orphan_rows_pre.to_csv('orphan_rows_pre.csv')
            df_pre = df_pre.drop(list(orphan_rows_pre))
        if orphan_rows_post:
            is_post_orphan = True
            df_orphan_rows_post = df_post.drop(same_rows)
            df_orphan_rows_post.to_csv('orphan_rows_post.csv')
            df_post = df_post.drop(list(orphan_rows_post))
    return False, is_pre_orphan, is_post_orphan


        
        