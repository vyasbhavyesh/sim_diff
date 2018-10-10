# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:32:08 2018

@author: bhavyas
"""
import diff_cli as cli
import diff_repr
import diff_summary

def single_compare(pre, post, unimportant_cols, primary_key, tolerance, dest_path):   
    col_diff, col_orphan_pre, col_orphan_post, pre, post = cli.orphan_cols(pre, post)
    pre, post = cli.hande_unimportant(pre, post, unimportant_cols)
    
    pre = pre.set_index(primary_key)
    post = post.set_index(primary_key)
    
    
    row_diff, row_orphan_pre, row_orphan_post, pre, post = cli.orphan_rows(pre, post, dest_path)
    
    pre = pre.sort_index()
    post = post.sort_index()
    
    diff_data = []
    
    diff_data = [[col,i,pre[col].iloc[i],post[col].iloc[i]] for col in pre.columns for i in range(len(pre[col])) if pre[col].iloc[i] != post[col].iloc[i]]
    diff_data = cli.drop_tolerance(diff_data, tolerance)
    
    
    
    diff_repr.diff_repr(diff_data, pre.columns, pre, post, dest_path)
    
    diff_summary.get_diff_summary(diff_data, col_diff, col_orphan_pre, col_orphan_post, row_diff, row_orphan_pre, row_orphan_post, dest_path)