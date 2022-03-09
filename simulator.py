'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 04:08:23
LastEditTime: 2022-03-09 04:07:39
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/type.py
'''

import random
import math
import type


def Init_Sim_BRAM(Handle_BRAMS,Path_of_circuit_place):
    for tmp_i in Handle_BRAMS.Dict:
        # print(Handle_BRAMS.Dict[tmp_i])
        with open(Path_of_circuit_place, "r") as Circuit_place:
            All_Line = Circuit_place.readlines()
        for tmp_line in All_Line:
            if tmp_line.find(Handle_BRAMS.Dict[tmp_i].Name) != -1:
                print(tmp_line)
                tmp_arr = tmp_line.split()
                Handle_BRAMS.Dict[tmp_i].Pos_x = tmp_arr[1]
                Handle_BRAMS.Dict[tmp_i].Pos_y = tmp_arr[2]


def Create_input(Signal_Probability):
    if random.randint(0,100) < float(Signal_Probability) * 100:
        return 1
    else:
        return 0

def Get_we_freq(We2_freq_list):
    if isinstance(We2_freq_list,list):
        return We2_freq_list[0]
    else:
        return 0




def Read_Act(Handle_BRAMS):
    for tmp_i in Handle_BRAMS.Dict:
        # single port BRAM
        if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") != -1:
            for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                tmp_input = []
                tmp_write_enable = []
                for tmp_ in range(0,5000):
                    tmp_input.append(Create_input(Handle_BRAMS.Dict[tmp_i].Add1_freq_list[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][0]))
                    tmp_write_enable.append(Create_input(Get_we_freq(Handle_BRAMS.Dict[tmp_i].We1_freq)))
                if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                    Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input
                    Handle_BRAMS.Dict[tmp_i].We1_input = tmp_write_enable
                else:
                    if tmp_j >= Handle_BRAMS.Dict[tmp_i].Num_add_1:
                        Handle_BRAMS.Dict[tmp_i].Add_1_input["tmp_pin"+str(tmp_j)] = [0]*5000
                    else:
                        Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input
        else: # dual port BRAM
            for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                tmp_input_1 = []
                tmp_input_2 = []
                tmp_write_enable_we1 = []
                tmp_write_enable_we2 = []
                for tmp_ in range(0,5000):
                    tmp_input_1.append(Create_input(Handle_BRAMS.Dict[tmp_i].Add1_freq_list[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][0]))
                    tmp_input_2.append(Create_input(Handle_BRAMS.Dict[tmp_i].Add2_freq_list[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][0]))
                    tmp_write_enable_we1.append(Create_input(Get_we_freq(Handle_BRAMS.Dict[tmp_i].We1_freq)))
                    tmp_write_enable_we2.append(Create_input(Get_we_freq(Handle_BRAMS.Dict[tmp_i].We2_freq)))
                    Handle_BRAMS.Dict[tmp_i].We1_input = tmp_write_enable_we1
                    Handle_BRAMS.Dict[tmp_i].We2_input = tmp_write_enable_we2
                if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                    Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input_1
                    Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]] = tmp_input_2
                else: # Assume that the number of Port_1 is same as Port_2
                    if tmp_j >= Handle_BRAMS.Dict[tmp_i].Num_add_1:
                        Handle_BRAMS.Dict[tmp_i].Add_1_input["tmp_pin"+str(tmp_j)] = [0]*5000
                        Handle_BRAMS.Dict[tmp_i].Add_2_input["tmp_pin"+str(tmp_j)] = [0]*5000
                    else:
                        Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input_1
                        Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]] = tmp_input_2


def Select_SLC_strategy(BRAM,num_select):
    index_of_slc = 0
    for tmp_i in BRAM.SLC_State:
        if tmp_i == 0:
            return index_of_slc 
        index_of_slc += 1
    # choose strategy  by frequency
    tmp_dict = dict()
    for tmp_i in range(0,type.swap_region):
        if BRAM.MLC_State[tmp_i] == 1:
            if BRAM.Freq_counter[tmp_i] >= BRAM.Freq_Threshold[tmp_i]:
                tmp_dict[tmp_i] = BRAM.Freq_counter[tmp_i]
    sorted_dict = sorted(tmp_dict.items(), key=lambda x: x[1])
    index_list = []
    freq_list = []
    for tmp_j in range(0,num_select):
        index_list.append(sorted_dict[tmp_j][0])
        freq_list.append(sorted_dict[tmp_j][1])
    return index_list,freq_list


def Set_SLC_Sel_state(BRAM,Choose_SLC,state):
    BRAM.SLC_State[Choose_SLC] = state
def Set_MLC_Sel_state(BRAM,Choose_MLC,state):
    BRAM.MLC_State[Choose_MLC] = state

def Select_MLC_strategy(BRAM,num_select):
    tmp_dict = dict()
    for tmp_i in range(0,type.num_region):
        if BRAM.MLC_State[tmp_i] == 1:
            if BRAM.Freq_counter[tmp_i] >= BRAM.Freq_Threshold[tmp_i]:
                tmp_dict[tmp_i] = BRAM.Freq_counter[tmp_i]
    sorted_dict = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
    index_list = []
    freq_list = []
    for tmp_j in range(0,num_select):
        index_list.append(sorted_dict[tmp_j][0])
        freq_list.append(sorted_dict[tmp_j][1])
    return index_list,freq_list




def Condition_Remaping(BRAM):
    # TODO: coding    
    # MLC condition
    # BRAM.Counter[tmp_j] > BRAM.Threshold[tmp_j]:
    # TODO: conding
    # SLC condition
    return 0 



def Sim_BRAM(Handle_BRAMS):
    Write_Counter = 0
    Swap_counter = 0
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                    tmp_str = ""
                    for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                        # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                        tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                    Sel_write = int(tmp_str,2)
                    if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                        num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                        Handle_BRAMS.Dict[tmp_i].Counter[num_current_slc] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[num_current_slc] > Handle_BRAMS.Dict[tmp_i].Up_limit[num_current_slc]:
                            return Write_Counter, Swap_counter
                    else:
                        Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Up_limit[Sel_write]:
                            return Write_Counter, Swap_counter
                # dual port
                if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") == -1:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_str = ""
                        for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                            if Handle_BRAMS.Dict[tmp_i].Num_add_2 > int(math.log2(type.num_region)):
                                tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        Sel_write = int(tmp_str,2)
                        if Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                            num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                            Handle_BRAMS.Dict[tmp_i].Counter[num_current_slc] += 1
                        else:
                            Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                            # if Handle_BRAMS.Dict[tmp_i].Current_sel != -1:
                            #     Handle_BRAMS.Dict[tmp_i].Freq_counter[Sel_write] += 1 

            for tmp_i in Handle_BRAMS.Dict:
                for tmp_j in range(0,type.num_region):
                    if Handle_BRAMS.Dict[tmp_i].Counter[tmp_j] > Handle_BRAMS.Dict[tmp_i].Threshold[tmp_j]:
                        Handle_BRAMS.Dict[tmp_i].Condition_counter[tmp_j] += 1
                        # select strategy
                        # Condition for Prioritization
                        if Handle_BRAMS.Dict[tmp_i].Condition_counter[tmp_j] == 1:
                            # TODO: I forget the function of the operation
                            # write due to swap
                            # Handle_BRAMS.Dict[tmp_i].Counter[Handle_BRAMS.Dict[tmp_i].Current_sel] += 1
                            if Condition_Remaping(Handle_BRAMS.Dict[tmp_i]):    
                                # which MLC is selected
                                slc_index_list, slc_freq_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i],2)
                                # which SLC is selected
                                mlc_index_list, mlc_freq_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],2)
                                # Remapping
                                # TODO: Remapping
                            if Handle_BRAMS.Dict[tmp_i].SLC_State[Choose_SLC] == 1:
                                last_value = Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC]
                                Handle_BRAMS.Dict[tmp_i].Counter[last_value] += 1   # write back
                                del Handle_BRAMS.Dict[tmp_i].Sel_Dict[last_value]   # del relationship
                                Set_SLC_Sel_state(Handle_BRAMS.Dict[tmp_i],Choose_SLC,0)   # reset flag
                                Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC] = -1     # reset flag
                            Set_SLC_Sel_state(Handle_BRAMS.Dict[tmp_i],Choose_SLC,1)
                            Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC] = tmp_j
                            Handle_BRAMS.Dict[tmp_i].Sel_Dict[tmp_j] = Choose_SLC
                            # write due to swap
                            Handle_BRAMS.Dict[tmp_i].Counter[type.num_region + Choose_SLC] += 1

                            Swap_counter += 1
                            Handle_BRAMS.Dict[tmp_i].Freq_counter = [0]*(type.num_region+type.swap_region)
                        elif Handle_BRAMS.Dict[tmp_i].Condition_counter[tmp_j] > 1 and max(Handle_BRAMS.Dict[tmp_i].Freq_counter) > Handle_BRAMS.Dict[tmp_i].Freq_Threshold[Handle_BRAMS.Dict[tmp_i].Freq_counter.index(max(Handle_BRAMS.Dict[tmp_i].Freq_counter))]:
                            # TODO: I forget the function of the operation
                            # write due to swap
                            # Handle_BRAMS.Dict[tmp_i].Counter[Handle_BRAMS.Dict[tmp_i].Current_sel] += 1

                            Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i])
                            tmp_j = Handle_BRAMS.Dict[tmp_i].Freq_counter.index(max(Handle_BRAMS.Dict[tmp_i].Freq_counter))
                            # Handle_BRAMS.Dict[tmp_i].Current_sel = tmp_j
                            Choose_SLC = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                            Set_SLC_Sel_state(Handle_BRAMS.Dict[tmp_i],Choose_SLC,1)
                            Set_MLC_Sel_state(Handle_BRAMS.Dict[tmp_i],Choose_SLC,1)
                            if Handle_BRAMS.Dict[tmp_i].SLC_State[Choose_SLC] == 1:
                                last_value = Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC]
                                Handle_BRAMS.Dict[tmp_i].Counter[last_value] += 1   # write back
                                del Handle_BRAMS.Dict[tmp_i].Sel_Dict[last_value]   # del relationship
                                Set_SLC_Sel_state(Handle_BRAMS.Dict[tmp_i],Choose_SLC,0)   # reset flag
                                Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC] = -1     # reset flag
                            Handle_BRAMS.Dict[tmp_i].Swap_Dict[Choose_SLC] = tmp_j
                            Handle_BRAMS.Dict[tmp_i].Sel_Dict[tmp_j] = Choose_SLC
                            # write due to swap
                            Handle_BRAMS.Dict[tmp_i].Counter[type.num_region + Choose_SLC] += 1
                            Swap_counter += 1
                            Handle_BRAMS.Dict[tmp_i].Freq_counter = [0]*(type.num_region+type.swap_region)  # map the current region to the swap region
    
                    

def Sim_BRAM_FIFO(Handle_BRAMS):
    Write_Counter = 0
    Swap_counter = 0
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                    tmp_str = ""
                    for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                        # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                        tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                    Sel_write = int(tmp_str,2)
                    if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
                        Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[8] > Handle_BRAMS.Dict[tmp_i].Up_limit[8]:
                            return Write_Counter, Swap_counter
                    else:
                        Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Threshold[Sel_write]:
                            # 
                            Handle_BRAMS.Dict[tmp_i].Counter[Handle_BRAMS.Dict[tmp_i].Current_sel] += 1
                            #
                            Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                            
                            
                            Handle_BRAMS.Dict[tmp_i].Current_sel = Sel_write
                            Swap_counter += 1
                        if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Up_limit[Sel_write]:
                            return Write_Counter, Swap_counter
                if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") == -1:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_str = ""
                        for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                            if Handle_BRAMS.Dict[tmp_i].Num_add_2 > int(math.log2(type.num_region)):
                                tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        Sel_write = int(tmp_str,2)
                        if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
                            Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                        else:
                            Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                            if Handle_BRAMS.Dict[tmp_i].Current_sel != -1:
                                Handle_BRAMS.Dict[tmp_i].Freq_counter[Sel_write] += 1 



def Sim_BRAM_Non(Handle_BRAMS):
    Write_Counter = 0
    Swap_counter = 0    
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                    tmp_str = ""
                    for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                        # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                        tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                    Sel_write = int(tmp_str,2)
                    if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
                        Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[8] > Handle_BRAMS.Dict[tmp_i].Up_limit[8]:
                            return Write_Counter,Swap_counter
                    else:
                        Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                        # Wear Out
                        if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Up_limit[Sel_write]:
                            return Write_Counter,Swap_counter
                if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") == -1:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_str = ""
                        for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
                            if Handle_BRAMS.Dict[tmp_i].Num_add_2 > int(math.log2(type.num_region)):
                                tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        Sel_write = int(tmp_str,2)
                        if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
                            Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                        else:
                            Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
                            if Handle_BRAMS.Dict[tmp_i].Current_sel != -1:
                                Handle_BRAMS.Dict[tmp_i].Freq_counter[Sel_write] += 1 
