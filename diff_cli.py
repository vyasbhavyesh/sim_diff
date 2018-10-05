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

pre, post = get_file_names()

def get_pri_key(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + cols[i])
    print("\nSelect col no. for primary keys :")
    primary_key_no = list(map(int, input().strip().split()))
    primary_key = [cols[i] for i in primary_key_no]
    return primary_key

df2 = pd.read_csv('dw_index_price_rate_values_post_test.csv', low_memory = False)


def get_drop_cols(cols):
    for i in range(len(cols)):
        print(str(i) + '- ' + cols[i])
    print("\nSelect col no. of unimportent columns :")
    col_no = list(map(int, input().strip().split()))
    drop_cols = [cols[i] for i in col_no]
    return drop_cols
