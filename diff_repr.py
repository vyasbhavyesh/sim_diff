# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 17:24:22 2018

@author: bhavyas
"""
import pandas as pd


def col_df(df_final, z = []):
    color = 'color: red'
    df1 = pd.DataFrame('', index=df_final.index, columns=df_final.columns)
    for cols in z:
        for i in range(len(df_final[cols[0]])):
            if df_final[cols[0]][i] != df_final[cols[1]][i]:
                df1[cols[0]][i] = color
                df1[cols[1]][i] = color
    return df1


def diff_repr(diff_data, cols, df_pre, df_post, dest_path):
    df_diff = pd.DataFrame(diff_data,columns = ['column','row','pre_value','post_value'])
    diff_cols = [col for col in cols if col in set(df_diff['column'])]
    same_cols = [col for col in cols if col not in set(df_diff['column'])]

    diff_cols_z = [['PRE_' +c ,'POST_' +c] for c in diff_cols]
    diff_cols = [d for u in diff_cols_z for d in u]

    same_cols = [['PRE_' +c ,'POST_' +c] for c in same_cols]
    same_cols = [d for u in same_cols for d in u]

    all_cols = diff_cols + same_cols
    df_final = pd.DataFrame(columns = all_cols ,index = df_pre.index.copy())



    for i in range(len(df_final)):
        for col in df_final.columns:
            if  'POST' in col:
                df_final[col] = df_post[col.replace('POST_','')]
    for i in range(len(df_final)):
        for col in df_final.columns:
            if 'PRE' in col:
                df_final[col] = df_pre[col.replace('PRE_','')]
    
    df_final['unique'] = range(1, len(df_final.index)+1)
    df_final = df_final.set_index('unique', append=True)

    df_final.style.apply(col_df, z = diff_cols_z, axis=None).to_excel(dest_path + 'diff_report.xlsx', engine='openpyxl')