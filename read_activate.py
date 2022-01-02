'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 06:50:08
LastEditTime: 2022-01-02 02:48:04
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/read_activate.py
'''

'''
description: 
param {*}
return {*}
'''


import type



def Parse4ACT(Path_of_circuit, Handle_BRAMS):
    Path_of_circuit = Path_of_circuit
    
    Act_dict = dict()
    with open(Path_of_circuit,"r") as File:
        All_Line = File.readlines()
    for tmp_line in All_Line:
        tmp = tmp_line.split()
        tmp_list = []
        tmp_list.append(tmp[1])
        tmp_list.append(tmp[2])
        tmp_list.append(tmp[3])
        Act_dict[tmp[0]] = tmp_list
        # print(tmp_line)
    for tmp_bram in Handle_BRAMS.Dict:
        if len(Handle_BRAMS.Dict[tmp_bram].Add1) > 0:
            for tmp_add in Handle_BRAMS.Dict[tmp_bram].Add1:
                Handle_BRAMS.Dict[tmp_bram].Add1_freq_list[tmp_add] = Act_dict[tmp_add]
        if len(Handle_BRAMS.Dict[tmp_bram].Add2) > 0:
            for tmp_add in Handle_BRAMS.Dict[tmp_bram].Add2:
                Handle_BRAMS.Dict[tmp_bram].Add2_freq_list[tmp_add] = Act_dict[tmp_add]
        if Handle_BRAMS.Dict[tmp_bram].We1 != "gnd" and Handle_BRAMS.Dict[tmp_bram].We1 != "open":
            Handle_BRAMS.Dict[tmp_bram].We1_freq = Act_dict[Handle_BRAMS.Dict[tmp_bram].We1]
        if Handle_BRAMS.Dict[tmp_bram].We2 != "gnd" and Handle_BRAMS.Dict[tmp_bram].We2 != "open":
            Handle_BRAMS.Dict[tmp_bram].We2_freq = Act_dict[Handle_BRAMS.Dict[tmp_bram].We2]


def Parse4PinACT(Path_of_circuit, Handle_BRAMS):
    Path_of_circuit = Path_of_circuit
    
    Act_dict = dict()
    with open(Path_of_circuit,"r") as File:
        All_Line = File.readlines()