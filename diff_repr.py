# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 17:24:22 2018

@author: bhavyas
"""
import pandas as pd
import time as t

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
    t1 = t.time()
    df_diff = pd.DataFrame(diff_data,columns = ['column','row','pre_value','post_value'])
    diff_cols = [col for col in cols if col in set(df_diff['column'])]
    same_cols = [col for col in cols if col not in set(df_diff['column'])]

    diff_cols_z = [['PRE_' +c ,'POST_' +c] for c in diff_cols]
    diff_cols = [d for u in diff_cols_z for d in u]

    same_cols = [['PRE_' +c ,'POST_' +c] for c in same_cols]
    same_cols = [d for u in same_cols for d in u]

    
    final_diff = pd.DataFrame(columns = diff_cols ,index = df_pre.index.copy())
    final_same = pd.DataFrame(columns = same_cols ,index = df_pre.index.copy())
    
    t2 = t.time()
    print('final df time' + str((t2-t1)/60))

    t1 = t.time()
    for col in final_diff.columns:
        if  'POST' in col:
            final_diff[col] = df_post[col.replace('POST_','')]
    for col in final_diff.columns:
        if 'PRE' in col:
            final_diff[col] = df_pre[col.replace('PRE_','')]

    #final_diff['unique'] = range(1, len(final_diff.index)+1)
   # final_diff = final_same.set_index('unique', append=True)
    final_diff.to_csv(dest_path+'different.csv')
    
    for col in final_same.columns:
        if  'POST' in col:
            final_same[col] = df_post[col.replace('POST_','')]
    for col in final_same.columns:
         if 'PRE' in col:
            final_same[col] = df_pre[col.replace('PRE_','')]

    #final_same['unique'] = range(1, len(final_same.index)+1)
   # final_same = final_same.set_index('unique', append=True)
    final_same.to_csv(dest_path+'same.csv')
    t2 = t.time()
    print( 'final copy and write time' + str((t2-t1)/60))
    
    