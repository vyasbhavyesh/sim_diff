# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 13:58:06 2018

@author: bhavyas

Data Structure - Tries
_insert
_find
"""
class Node:
    def __init__(self):
        self.child = [None]*26
        self.isEnd = None

class Tries:
    def __init__(self):
        self.root = Node()
        
    def charToIndex(self,char):
        return ord(char) - ord('a')
    
    def insert(self,string):
        temp = self.root 
        length = len(string) 
        for level in range(length): 
            index = self.charToIndex(string[level]) 
  
            if not temp.child[index]: 
                temp.child[index] = Node() 
            temp = temp.child[index] 
        temp.isEnd = True
        
    def search(self, key): 
        temp = self.root 
        length = len(key) 
        for level in range(length): 
            index = self.charToIndex(key[level]) 
            if not temp.child[index]: 
                return False
            temp = temp.child[index] 
  
        return temp != None and temp.isEnd
    
    
    

