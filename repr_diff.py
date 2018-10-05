# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:23:02 2018

@author: bhavyas
"""
l = []
def drop_tolerance(diff):
    for item in diff_data:
        if abs(item[2] - item[3]) < 0.001:
            l.append(item)
            diff.remove(item)
            
import pandas as pd 

primary_key = ['index_id',
'index_name',
'gpt_id',
'gpt_name',
'gpt_category',
'contract_end_date',
'market_data_type'
]

unimportant = ['extraction_id']

diff_data = []

df1 = pd.read_csv('dw_index_price_rate_values_Pre_test.csv', low_memory = False)
df2 = pd.read_csv('dw_index_price_rate_values_post_test.csv', low_memory = False)

df1= df1.fillna(0)
df2 = df2.fillna(0)

df1 = df1.set_index(primary_key)
df2 = df2.set_index(primary_key)

df1= df1.sort_index()
df2= df2.sort_index()

pre_cols = df1.columns
post_cols = df2.columns

df1 = df1.drop(unimportant_cols,axis =1)
df2 = df2.drop(unimportant_cols,axis =1)

diff_data = [[col,i,df1[col][i],df2[col][i]] for col in df1.columns for i in range(len(df1[col])) if df1[col][i] != df2[col][i]]
drop_tolerance(diff_data)

df_diff = pd.DataFrame(diff_data,columns = ['column','row','pre_value','post_value'])
diff_cols = [col for col in pre_cols if col in set(df_diff['column'])]
same_cols = [col for col in pre_cols if col not in set(df_diff['column'])]

diff_cols = [['PRE_' +c ,'POST_' +c] for c in diff_cols]
diff_cols = [d for u in diff_cols for d in u]

same_cols = [['PRE_' +c ,'POST_' +c] for c in same_cols]
same_cols = [d for u in same_cols for d in u]

all_cols = diff_cols + same_cols
df_final = pd.DataFrame(columns = all_cols ,index = df1.index.copy())



for i in range(len(df_final)):
    for col in df_final.columns:
        if  'POST' in col:
            df_final[col] = df2[col.replace('POST_','')]
for i in range(len(df_final)):
    for col in df_final.columns:
        if 'PRE' in col:
            df_final[col] = df1[col.replace('PRE_','')]

df_final['unique'] = range(1, len(df_final.index)+1)
df_final = df_final.set_index('unique', append=True)
z =[]
def highlight_cols(s):
    color = 'red'
    z.append(s)
    return 'color: %s' % color 
df_final.style.applymap(highlight_cols, subset=pd.IndexSlice[:, diff_cols]).to_excel('styled.xlsx', engine='openpyxl')



def col_df(df_final):
    color = 'color: red'
    df1 = pd.DataFrame('', index=df_final.index, columns=df_final.columns)
    for cols in z:
        for i in range(len(df_final[cols[0]])):
            if df_final[cols[0]][i] != df_final[cols[1]][i]:
                df1[cols[0]][i] = color
                df1[cols[1]][i] = color
    return df1

df_final.style.apply(col_df, axis=None).to_excel('styled.xlsx', engine='openpyxl')









def drop_rows_diff(df1,df2):
    df1_rows = df1.index.copy()
    df2_rows = df2.index.copy()
    l1 = len(df1)
    l2 = len(df2)
    df1_m_df2 =set(df1_rows) - set(df2_rows)
    df2_m_df1 =set(df2_rows) - set(df1_rows) 
    
    df11 = df1.drop(list(df1_m_df2))
    row_diff_df = df1.drop(df2_rows)
    
    row_diff_df.to_csv('orph_row_pre.csv')


df1.to_csv('df1.csv')
df2.to_csv('df2.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    