'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 04:08:23
LastEditTime: 2021-12-29 07:38:00
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/type.py
'''




class BRAM:   
    def _init_(self, name, instance, mode, add1, add2, we1, we2):
        self.Name = name
        self.Instance = instance
        self.Mode = mode
        self.Add1 = add1
        self.Add2 = add2
        self.We1 = we1
        self.We2 = we2
        self.Add1_freq_list = dict()
        self.Add2_freq_list = dict()
        self.We1_freq = 0
        self.We2_freq = 0


class BRAMS:   
    def _init_(self):
        self.Dict = dict()

