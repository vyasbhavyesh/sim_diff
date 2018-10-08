# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:51:08 2018

@author: bhavyas
driver sim diff
"""
import diff_cli as cli
import diff_repr
import diff_summary

print("Choose file type\n 1- CSV\n 2- Excel")
file_type = int(input())

if file_type == 1:
    pre_file, post_file = cli.get_file_names()
    pre, post = cli.read_csv_input(pre_file, post_file)
elif file_type == 2:
    pre_file, post_file = cli.get_file_names()
    pre, post = cli.read_xls_input(pre_file, post_file)

col_diff, col_orphan_pre, col_orphan_post, pre, post = cli.orphan_cols(pre, post)

cols = list(pre.columns)

primary_key = cli.get_pri_key(cols)
unimportant_cols = cli.get_drop_cols(cols)
tolerance = cli.get_tolerance()

pre, post = cli.hande_unimportant(pre, post, unimportant_cols)

pre = pre.set_index(primary_key)
post = post.set_index(primary_key)

row_diff, row_orphan_pre, row_orphan_post, pre, post = cli.orphan_rows(pre, post)

pre = pre.sort_index()
post = post.sort_index()

diff_data = []

diff_data = [[col,i,pre[col].iloc[i],post[col].iloc[i]] for col in pre.columns for i in range(len(pre[col])) if pre[col].iloc[i] != post[col].iloc[i]]

diff_repr.diff_repr(diff_data, pre.columns, pre, post)

diff_summary.get_diff_summary(diff_data, col_diff, col_orphan_pre, col_orphan_post, row_diff, row_orphan_pre, row_orphan_post)