'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 04:08:23
LastEditTime: 2022-03-04 08:52:41
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/type.py
'''

num_region = 8   # 


class BRAM:   
    def _init_(self, name, instance, mode, add1, add2, we1, we2):
        self.Name = name
        self.Instance = instance
        self.Mode = mode
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
        self.Current_sel = -1
        self.Swap_p = -1 
        self.Num_subblock = 0
        self.Counter = [0]*9           # counter of swap region if counter[9]
        self.Condition_counter = [0]*9
        self.Threshold = [5000,5000,5000,5000,5000,5000,5000,5000,5000000]
        self.Up_limit = [5500,5500,5500,5500,5500,5500,5500,5500,5500000]
        self.Freq_counter = [0]*9           # counter of swap region if counter[9]
        self.Freq_Threshold = [275,275,275,275,275,275,275,275,2000000]
        


class BRAMS:   
    def _init_(self):
        self.Dict = dict()
        self.cycle = 0

