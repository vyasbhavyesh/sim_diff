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
        self.post = pd.read_csv(self.post_file, low_memorty = False)
        self.primary_key = primary_key
        self.unimportant_cols = unimportant_cols
        self.tolerance = tolerance
        self.dest = dest
    
    
    def _handle_unimportant(self):
        self.pre = self.pre.fillna(0)
        self.post = self.post.fillna(0)
        self.pre = self.pre.drop(self.unimportant_cols,axis =1)
        self.post = self.post.drop(self.unimportant_cols,axis =1)
        
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
    
    
    def _get_diff(self):
        pass
    
    
    def _diff_repr(self):
        pass
    
    
    def _summary(self):
        pass