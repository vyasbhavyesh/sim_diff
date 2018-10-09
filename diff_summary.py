# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 18:39:45 2018

@author: bhavyas
"""
from collections import Counter

def get_diff_summary(diff_data, col_diff, col_orphan_pre, col_orphan_post, row_diff, row_orphan_pre, row_orphan_post, dest_path ):
    no_of_diffs = len(diff_data)
    diff_cols = Counter([col_name[0] for col_name in diff_data])
    no_of_diff_cols = len(diff_cols)
    summary = 'Summary of Comparision\n'+ '\n'
    summary += 'Total number of different elements: '+ str(no_of_diffs) + '\n' + '\n'
    summary += 'Total number of columns having differences: '+ str(no_of_diff_cols) + '\n' + '\n'
    summary += 'Orphan Rows: '+ str(row_diff) + '\n' + '\n'
    summary += 'Orphan Rows Pre: ' + str(row_orphan_pre[0]) + ' No. of rows- ' + str(len(row_orphan_pre[1])) + '\n'+ '\n'
    summary += 'Orphan Rows Post: ' + str(row_orphan_post[0]) + ' No. of rows- ' + str(len(row_orphan_post[1])) + '\n'+ '\n'
    summary += 'Orphan Columns: ' + str(col_diff) + '\n'+ '\n'
    summary += 'Orphan Columns Pre: ' + str(col_orphan_pre[0]) + ' Names- ' + ''.join(col_orphan_pre[1]) + '\n'+ '\n'
    summary += 'Orphan Columns Post: ' + str(col_orphan_post[0]) + ' Names-' + ''.join(col_orphan_post[1]) + '\n'+ '\n'
    summary +='Number of different elements per columns:\n'+ '\n'
    
    for key in diff_cols.keys():
        summary += '\t' + key + '- ' + str(diff_cols[key]) +'\n'
    
    with open(dest_path + 'diff_summary.txt', 'w') as s:
        s.write(summary)