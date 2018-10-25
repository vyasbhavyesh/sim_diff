#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:11:10 2018

@author: babavyas
"""
import pandas as pd

class sim_diff:
    def __init__(self,pre_path,post_path,primary_key,unimportant_cols,tolerance,dest):
        self.pre_file = pre_path
        self.post_file = post_path
        self.pre = pd.read_csv(self.pre_file, low_memory = False)
        self.post = pd.read_csv(self.post_file, low_memory = False)
        self.primary_key = primary_key
        self.unimportant_cols = unimportant_cols
        self.tolerance = tolerance
        self.dest = dest
        self.diff_data = []
        self.final = pd.DataFrame()
    
    def _handle_unimportant(self):
        self.pre = self.pre.fillna(0)
        self.post = self.post.fillna(0)
        self.pre = self.pre.drop(self.unimportant_cols,axis =1)
        self.post = self.post.drop(self.unimportant_cols,axis =1)
        # orphan col logic
    def _orphan_col(self):     
        if list(self.pre.columns) == list(self.post.columns):
            pass
        else:
            self.pre_cols = set(self.pre.columns)
            self.post_cols = set(self.post.columns)
            
            orphan_cols_pre = self.pre_cols - self.post_cols
            #print("Orphan columns in pre file:")
            #print(orphan_cols_pre)
            orphan_cols_post = self.post_cols - self.pre_cols
            #print("Orphan columns in post file:")
            #print(orphan_cols_post)
            
            if orphan_cols_pre:
                self.pre = self.pre.drop(list(orphan_cols_pre),axis =1)
                #is_pre_orphan = True
            if orphan_cols_post:
                self.post = self.post.drop(list(orphan_cols_post),axis =1)
                
    def _orphan_row(self):
        # orphan row logic
        pre_rows = set(self.pre.index.copy())
        post_rows = set(self.post.index.copy())
        
        df_orphan_rows_pre = pd.DataFrame()
        df_orphan_rows_post = pd.DataFrame()
        orphan_rows_pre = pre_rows-post_rows
        orphan_rows_post = post_rows-pre_rows
        print(orphan_rows_post,orphan_rows_pre)
        #need more attention and testing
        same_rows = list(pre_rows - orphan_rows_pre)
        if not orphan_rows_pre and not orphan_rows_post:
            pass
        else:
            is_pre_orphan = False
            is_post_orphan = False
            if orphan_rows_pre:
                is_pre_orphan = True
                df_orphan_rows_pre = self.pre.drop(same_rows)
                df_orphan_rows_pre.to_csv(self.dest + 'orphan_rows_pre.csv')
                print('Oprhan Row in pre written')
                self.pre = self.pre.drop(list(orphan_rows_pre))
            if orphan_rows_post:
                is_post_orphan = True
                df_orphan_rows_post = self.post.drop(same_rows)
                df_orphan_rows_post.to_csv(self.dest + 'orphan_rows_post.csv')
                print('Oprhan Row in post written')
                self.post = self.post.drop(list(orphan_rows_post))
    
    
    def _sort_index(self):
        self._handle_unimportant()
        self._orphan_col()
        self.pre = self.pre.set_index(self.primary_key)
        self.post = self.post.set_index(self.primary_key)
        self._orphan_row()
        self.pre = self.pre.sort_index()
        self.post = self.post.sort_index()
    
    def drop_tolerance(self):
        l = len(self.diff_data)
        for item in self.diff_data:
            if type(item[2]) == float:
                if abs(item[2] - item[3]) < self.tolerance:
                    self.diff_data.remove(item)
            if not l == len(self.diff_data):
                self.drop_tolerance()
    
    
    def _get_diff(self):
        print('in diff data method')
        self.diff_data = [[col,i,self.pre[col].iloc[i],self.post[col].iloc[i]] for col in self.pre.columns for i in range(len(self.pre[col])) if self.pre[col].iloc[i] != self.post[col].iloc[i]]
        self.drop_tolerance()
    
    
    def _diff_repr(self):
        self.diff = pd.DataFrame(self.diff_data,columns = ['column','row','pre_value','post_value'])
        diff_cols = [col for col in self.pre.columns if col in set(self.diff['column'])]
        same_cols = [col for col in self.pre.columns if col not in set(self.diff['column'])]

        diff_cols_z = [['PRE_' +c ,'POST_' +c] for c in diff_cols]
        diff_cols = [d for u in diff_cols_z for d in u]

        same_cols = [['PRE_' +c ,'POST_' +c] for c in same_cols]
        same_cols = [d for u in same_cols for d in u]

        #all_cols = diff_cols + same_cols
        self.final_diff = pd.DataFrame(columns = diff_cols ,index = self.pre.index.copy())
        self.final_same = pd.DataFrame(columns = same_cols ,index = self.pre.index.copy())

        
        for col in self.final_diff.columns:
            if  'POST' in col:
                self.final_diff[col] = self.post[col.replace('POST_','')]
        for col in self.final_diff.columns:
             if 'PRE' in col:
                self.final_diff[col] = self.pre[col.replace('PRE_','')]
    
        self.final_diff['unique'] = range(1, len(self.final.index)+1)
        self.final_diff = self.final_same.set_index('unique', append=True)
        
        for col in self.final_same.columns:
            if  'POST' in col:
                self.final_same[col] = self.post[col.replace('POST_','')]
        for col in self.final_same.columns:
             if 'PRE' in col:
                self.final[col] = self.pre[col.replace('PRE_','')]
    
        self.final_same['unique'] = range(1, len(self.final.index)+1)
        self.final_same = self.final_same.set_index('unique', append=True)
        
    
    def _summary(self):
        pass

        
        