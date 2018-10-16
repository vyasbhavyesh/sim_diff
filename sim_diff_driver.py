# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:51:08 2018

@author: bhavyas
driver sim diff
"""
import time
import mode_one_driver as mode_1
import mode_2_sim_diff as mode_2
print('Select the SIM_DIFF_MODE:\n 1.Single PRE/POST CSV/Excel File\n 2.PRE/POST Folders\n 3.2GB or greater Single PRE/POST CSV\n 4.Database connect and compare')

mode = int(input())

if mode == 1:
    mode_1.mode_one()
elif mode == 2:
    t1 = time.time()
    mode_2.mode_2()
    t2 = time.time()
    
    print(t2-t1)
elif mode == 3:
    print("Under construction")
elif mode == 4:
    print("Under construction")
else:
    print("Worng Input")
