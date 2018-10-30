# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:13:16 2018

@author: bhavyas
"""
import diff_cli as cli
import os
import single_compare
import pandas as pd

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
    
    
    pfolio_data = {'Portfolio': [],
                   'Match/Mismatch Columns': [],
                   'Mismatch Columns Count':[],
                   'Orphan Rows': [],
                   'PRE_Oprhan Count':[],
                   'POST_Oprhan Count':[]
                }
    
    diff_data_collated = {'Portfolio':[],
                          'Column Name':[],
                          'Number of differences':[],
                          'Sample deal num':[]
                    }
    
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
        
        print("Working on file:"+ str(pre_file.stem))
                    
        diff_data, row_diff, row_orphan_pre, row_orphan_post \
        = single_compare.single_compare(pre, post, unimportant_cols, \
                                        primary_key, tolerance, dest_path_i)
        diff_data_formated = {}
        for row in diff_data:
            if row[0] not in diff_data_formated.keys():
                diff_data_formated[row[0]] = [row[1]]
            else:
                diff_data_formated[row[0]].append(row[1])
        
        
        if diff_data:
            pfolio_data['Portfolio'].append(pre_file.stem)
            pfolio_data['Match/Mismatch Columns'].append('Mismatch')
            pfolio_data['Mismatch Columns Count'].append(len(diff_data_formated.keys()))
            pfolio_data['Orphan Rows'].append(row_diff)
            pfolio_data['PRE_Oprhan Count'].append(row_orphan_pre[1])
            pfolio_data['POST_Oprhan Count'].append(row_orphan_post[1])
        elif diff_data and not row_diff:
            pfolio_data['Portfolio'].append(pre_file.stem)
            pfolio_data['Match/Mismatch Columns'].append('Match')
            pfolio_data['Mismatch Columns Count'].append(len(diff_data_formated.keys()))
            pfolio_data['Orphan Rows'].append(row_diff)
            pfolio_data['PRE_Oprhan Count'].append(row_orphan_post[1])
            pfolio_data['POST_Oprhan Count'].append(row_orphan_post[1])
        elif not diff_data and row_diff:
            pfolio_data['Portfolio'].append(pre_file.stem)
            pfolio_data['Match/Mismatch Columns'].append('Match')
            pfolio_data['Mismatch Columns Count'].append(0)
            pfolio_data['Orphan Rows'].append(row_diff)
            pfolio_data['PRE_Oprhan Count'].append(row_orphan_pre[1])
            pfolio_data['POST_Oprhan Count'].append(row_orphan_post[1])
        elif not diff_data and not row_diff:
            pfolio_data['Portfolio'].append(pre_file.stem)
            pfolio_data['Match/Mismatch Columns'].append('Match')
            pfolio_data['Mismatch Columns Count'].append(0)
            pfolio_data['Orphan Rows'].append(row_diff)
            pfolio_data['PRE_Oprhan Count'].append(row_orphan_post[1])
            pfolio_data['POST_Oprhan Count'].append(row_orphan_post[1])
            
        if diff_data_formated:
            for col in diff_data_formated.keys():
                diff_data_collated['Portfolio'].append(pre_file.stem)
                diff_data_collated['Column Name'].append(col)
                diff_data_collated['Number of differences'].append(len(diff_data_formated[col]))
                diff_data_collated['Sample deal num'].append(pre['deal_num'].iloc[diff_data_formated[col][0]])
        
        
        print("Report generated for file:"+ str(pre_file.stem))
        
    df1 = pd.DataFrame().from_dict(pfolio_data)
    df2 = pd.DataFrame().from_dict(diff_data_collated)
    
    df1 = df1.sort_values(['Match/Mismatch Columns'])
    
    writer = pd.ExcelWriter(dest_path + pre_file.parent.name + '.xlsx')
    df1.to_excel(writer,'Folder Details', index = False)
    df2.to_excel(writer,'Portfolio Details', index = False)
    writer.save()

    
    
    
    
    
    
    

    