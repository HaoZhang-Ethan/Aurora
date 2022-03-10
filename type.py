'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 04:08:23
LastEditTime: 2022-03-10 08:28:18
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/type.py
'''

import math
from typing import Counter

num_region = 8      # MLC
region_add_bit = int(math.log2(num_region))
swap_region = 3     # SLC

# 32K Bit 512x64
organize_mem_row = 512
organize_mem_col = 64
subblock_row_add_bit = int(math.log2(organize_mem_row/num_region))
subblock_row = int(organize_mem_row/num_region)
subblock_col = organize_mem_col


Lifetime = math.pow(10,5)
Counter_bit = math.ceil(math.log2(Lifetime))
if Counter_bit <=5:
    print("Place increase the lifetime of NVM")
Freq_Acc = 5  # 1--50%  2--25%  3--12.5%   4--6.25%    5--3.125%
Frequency_bit = Counter_bit - Freq_Acc              
Accuracy_bit = 3   # 1--50%  2--25%  3--12.5%   4--6.25%    5--3.125%
Accuracy_bit_Aid =  Counter_bit - Freq_Acc - Accuracy_bit 
Counter_high_bit = Counter_bit - Accuracy_bit_Aid - Accuracy_bit

class BRAM:
    def _init_(self, name, instance, mode, add1, add2, we1, we2, address_bit, data_bit):
        self.Name = name
        self.Instance = instance
        self.Mode = mode
        self.Address_bit = address_bit
        self.Data_bit = data_bit
        self.Add1 = add1
        self.Num_add_1 = len(self.Add1)
        self.Add_1_input = dict()
        self.Add2 = add2
        self.Num_add_2 = len(self.Add2)
        self.Add_2_input = dict()
        self.We1 = we1
        self.We1_input = []
        self.We2 = we2
        self.We2_input = []
        self.Add1_freq_list = dict()
        self.Add2_freq_list = dict()
        self.We1_freq = 0
        self.We2_freq = 0
        self.Add1_act_list = dict()
        self.Add2_act_list = dict()
        self.We1_act_list = 0
        self.We2_act_list = 0
        self.Pos_x = 0
        self.Pos_y = 0
        self.Current_sel = [-1]*swap_region         # 当前谁在SLC区域
        self.Swap_p = [-1]*swap_region              # 当前SLC区域指向谁
        self.MLC_State = [1]*num_region             # 当前MLC状态 0表示未被使用(为SLC模式) 1表示对应编号的subblock是MLC的
        self.SLC_State = [0]*swap_region            # 当前SLC状态 0表示未被使用
        self.Sel_Dict = dict()
        self.Swap_Dict = dict()
        self.Num_subblock = 0
        # self.Lifetime_Counter = [0]*(num_region+swap_region)           # counter of swap region if counter[9]
        # Counter 记录实际寿命 只记录MLC的
        self.Counter_Cell_level = [[0]*subblock_row*subblock_col]*num_region
        
        self.Condition_counter = [0]*(num_region+swap_region) # 满足出发条件后被触发了多少次  TODO: Del
        self.Threshold = [5000]*num_region + [5000000]*swap_region
        self.Up_limit = [5500]*num_region + [5500000]*swap_region
        self.Accuracy_counter = [0]*(num_region+swap_region)
        self.Accuracy_Threshold = [int(math.pow(2,Accuracy_bit))]*num_region + [1000*int(math.pow(2,Accuracy_bit))]*swap_region
        self.Accuracy_Aid_counter = [0]*(num_region+swap_region)
        self.Accuracy_Aid_Threshold = [int(math.pow(2,Accuracy_bit_Aid))]*num_region + [1000*int(math.pow(2,Accuracy_bit_Aid))]*swap_region
        self.Freq_counter = [0]*(num_region+swap_region)             # counter of swap region if counter[9]
        self.Freq_Threshold = [int(math.pow(2,Frequency_bit))]*num_region + [1000*int(math.pow(2,Frequency_bit))]*swap_region
        self.Counter_high = [0]*(num_region+swap_region) # Counter的高位
        self.Counter_high_Threshold = [int(math.pow(2,Counter_high_bit))]*num_region + [1000*int(math.pow(2,Counter_high_bit))]*swap_region 
        # |XXXXXXXXXXXXXXXXXXXXXXXXXXX|XXXXXXXXXXXXXXXXX|XXXXXXXXXXXXXXXXXX|
        # |          high bit      |            frequency bit              |

        # |         high bit          |  accuracy bit   |aid accuracy bit  |



        


class BRAMS:   
    def _init_(self):
        self.Dict = dict()
        self.cycle = 0

