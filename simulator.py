'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-29 04:08:23
LastEditTime: 2022-03-26 10:24:27
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/type.py
'''


import random
import math
import type
import os





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
    if Handle_BRAMS.has_act_file == 1:
        return 1
    for tmp_i in Handle_BRAMS.Dict:
        # single port BRAM
        if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") != -1:
            for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
                tmp_input = []
                tmp_write_enable = []
                for tmp_ in range(0,5000):
                    tmp_input.append(Create_input(Handle_BRAMS.Dict[tmp_i].Add1_freq_list[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][0]))
                    tmp_write_enable.append(Create_input(Get_we_freq(Handle_BRAMS.Dict[tmp_i].We1_freq)))
                # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input
                Handle_BRAMS.Dict[tmp_i].We1_input = tmp_write_enable
                # else:
                #     if tmp_j >= Handle_BRAMS.Dict[tmp_i].Num_add_1:
                #         Handle_BRAMS.Dict[tmp_i].Add_1_input["tmp_pin"+str(tmp_j)] = [0]*5000
                #     else:
                #         Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input
        else: # dual port BRAM
            for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
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
                # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
                Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input_1
                Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]] = tmp_input_2
                # else: # Assume that the number of Port_1 is same as Port_2
                #     if tmp_j >= Handle_BRAMS.Dict[tmp_i].Num_add_1:
                #         Handle_BRAMS.Dict[tmp_i].Add_1_input["tmp_pin"+str(tmp_j)] = [0]*5000
                #         Handle_BRAMS.Dict[tmp_i].Add_2_input["tmp_pin"+str(tmp_j)] = [0]*5000
                #     else:
                #         Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]] = tmp_input_1
                #         Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]] = tmp_input_2


def Calculate_Wear(Counter_high,Accuracy_counter):
    Counter_high_base = Counter_high * int(math.pow(2,type.address_bit - type.Counter_high_bit))
    Accuracy_counter_offset = Accuracy_counter * int(math.pow(2,type.address_bit - type.Counter_high_bit - type.Accuracy_bit_Aid))
    Wear = (Counter_high_base + Accuracy_counter_offset)
    return Wear


def Select_SLC_strategy(BRAM):
    # index_of_slc = 0
    # for tmp_i in range(0,type.swap_region):
    #     if BRAM.SLC_State[tmp_i] == 0:
    #         tmp_dict[index_of_slc] = 0 
    #     index_of_slc += 1
    # choose strategy  by frequency
    tmp_dict = dict()
    for tmp_i in range(0,type.swap_region):
        if BRAM.SLC_State[tmp_i] == 1:
            tmp_dict[tmp_i] = BRAM.Freq_counter[tmp_i]/(1-(Calculate_Wear(BRAM.Counter_high[BRAM.Swap_Dict[tmp_i]],BRAM.Accuracy_counter[BRAM.Swap_Dict[tmp_i]])/type.MLC_Lifetime))
        else:
            tmp_dict[tmp_i] = 0
    sorted_dict = sorted(tmp_dict.items(), key=lambda x: x[1])
    index_list = []
    cost_list = []
    for tmp_j in range(0,len(sorted_dict)):
        index_list.append(sorted_dict[tmp_j][0])
        cost_list.append(sorted_dict[tmp_j][1])
    return index_list,cost_list


def Select_SLC_strategy_FIFO(BRAM):
    tmp_dict = dict()
    for tmp_i in range(0,type.swap_region):
        if BRAM.SLC_State[tmp_i] == 1:
            tmp_dict[tmp_i] = BRAM.Priority[tmp_i]
        else:
            tmp_dict[tmp_i] = -1
    sorted_dict = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
    index_list = []
    cost_list = []
    for tmp_j in range(0,len(sorted_dict)):
        index_list.append(sorted_dict[tmp_j][0])
        cost_list.append(sorted_dict[tmp_j][1])
    return index_list,cost_list


def Set_SLC_Sel_state(BRAM,Choose_SLC,state):
    BRAM.SLC_State[Choose_SLC] = state
def Set_MLC_Sel_state(BRAM,Choose_MLC,state):
    BRAM.MLC_State[Choose_MLC] = state

def Select_MLC_strategy(BRAM,Threshold):
    Max_freq = max(BRAM.Freq_counter[0:type.num_region])
    T_select = Threshold*Max_freq
    tmp_dict = dict()
    for tmp_i in range(0,type.num_region):
        if BRAM.MLC_State[tmp_i] == 1:
            if BRAM.Freq_counter[tmp_i] >= T_select:
                tmp_dict[tmp_i] = BRAM.Freq_counter[tmp_i]/(1-(Calculate_Wear(BRAM.Counter_high[tmp_i],BRAM.Accuracy_counter[tmp_i])/type.MLC_Lifetime))
    sorted_dict = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
    index_list = []
    cost_list = []
    
    for tmp_j in range(0,len(sorted_dict)):
        index_list.append(sorted_dict[tmp_j][0])
        cost_list.append(sorted_dict[tmp_j][1])
    
    return index_list,cost_list

def BRAM_counter(BRAM, index):
    BRAM.Freq_counter[index] += 1*BRAM.amp
    BRAM.Accuracy_Aid_counter[index] += 1*BRAM.amp
    if BRAM.Accuracy_Aid_counter[index] >= BRAM.Accuracy_Aid_Threshold[index]:
        BRAM.Accuracy_counter[index] += 1
        BRAM.Accuracy_Aid_counter[index] = 0
        if BRAM.Accuracy_counter[index] >= BRAM.Accuracy_Threshold[index]:
           BRAM.Accuracy_counter[index] = 0
           BRAM.Counter_high[index] += 1
           if BRAM.Counter_high[index] >= BRAM.Counter_high_Threshold[index]:
                BRAM.Counter_high[index] -= 1
    if BRAM.Freq_counter[index] > BRAM.Freq_Threshold[index]:
        return True
    return False


def Remaping(BRAM, SLC_index_list, SLC_cost_list, MLC_index_list, MLC_cost_list):
    remapping_num = 0
    min_len = min(len(SLC_index_list),len(MLC_index_list))
    if (min_len >= 1):
        BRAM.Freq_counter = [0 for i in range (type.num_region+type.swap_region)]
    for tmp_i in range(0,min_len):
        if SLC_cost_list[tmp_i] < MLC_cost_list[tmp_i]:
            remapping_num += 1
            if BRAM.SLC_State[SLC_index_list[tmp_i]] == 1: # if the SLC is used
                last_value = BRAM.Swap_Dict[SLC_index_list[tmp_i]]
                Set_MLC_Sel_state(BRAM, last_value, 1)
                BRAM_counter(BRAM,last_value) # write back
                del BRAM.Sel_Dict[last_value]   # del relationship
                Set_SLC_Sel_state(BRAM,SLC_index_list[tmp_i],0)   # reset flag
                BRAM.Swap_Dict[SLC_index_list[tmp_i]] = -1     # reset flag
            Set_SLC_Sel_state(BRAM, SLC_index_list[tmp_i], 1)
            Set_MLC_Sel_state(BRAM, MLC_index_list[tmp_i], 0)
            BRAM.Swap_Dict[SLC_index_list[tmp_i]] = MLC_index_list[tmp_i]
            BRAM.Sel_Dict[MLC_index_list[tmp_i]] = SLC_index_list[tmp_i]
            # write due to swap
            BRAM_counter(BRAM,type.num_region + SLC_index_list[tmp_i]) # write back
    return remapping_num



def FIFO_Priority_update(BRAM,SLC_id):
    BRAM.Priority[SLC_id] += 1
    if BRAM.Priority[SLC_id] >= BRAM.Priority_Threshold[SLC_id]:
        BRAM.Priority[SLC_id] = 0
    
    

def Remaping_FIFO(BRAM, SLC_index_list, SLC_cost_list, MLC_index_list, MLC_cost_list):
    remapping_num = 0
    BRAM.Freq_counter = [0 for i in range (type.num_region+type.swap_region)]
    FIFO_Priority_update(BRAM,SLC_index_list)
    remapping_num += 1
    if BRAM.SLC_State[SLC_index_list] == 1: # if the SLC is used
        last_value = BRAM.Swap_Dict[SLC_index_list]
        Set_MLC_Sel_state(BRAM, last_value, 1)
        BRAM_counter(BRAM,last_value) # write back
        del BRAM.Sel_Dict[last_value]   # del relationship
        Set_SLC_Sel_state(BRAM,SLC_index_list,0)   # reset flag
        BRAM.Swap_Dict[SLC_index_list] = -1     # reset flag
    Set_SLC_Sel_state(BRAM, SLC_index_list, 1)
    Set_MLC_Sel_state(BRAM, MLC_index_list, 0)
    BRAM.Swap_Dict[SLC_index_list] = MLC_index_list
    BRAM.Sel_Dict[MLC_index_list] = SLC_index_list
    # write due to swap
    BRAM_counter(BRAM,type.num_region + SLC_index_list) # write back
    return remapping_num



def Memory_write(BRAM, Address):
    Port_Add_bit = len(Address)
    # format the address
    if BRAM.Address_bit == Port_Add_bit:
        pass
    else:
        for tmp_i in range(0, BRAM.Address_bit-Port_Add_bit):
            Address += "0"    # connect the gnd
    
    # find subblock
    subblock_address = Address[0:type.region_add_bit]
    tmp_id = subblock_id = int(subblock_address,2)
    
    if tmp_id in BRAM.Sel_Dict:
        subblock_id = type.num_region + BRAM.Sel_Dict[tmp_id]
        
    
    
    # find memory cell
    # Row
    Intra_subblock_address_row = Address[type.region_add_bit:type.region_add_bit+type.subblock_row_add_bit]
    Row_str = ""
    for tmp_i in range(0,len(Intra_subblock_address_row)):
        Row_str += Intra_subblock_address_row[tmp_i]
    if Row_str == "":
        Row_str += "0"
    # Col
    # base+offset
    Intra_subblock_address_col = Address[type.region_add_bit+type.subblock_row_add_bit:]
    Col_base_str = ""
    for tmp_i in range(0,len(Intra_subblock_address_col)):
        Col_base_str += Intra_subblock_address_col[tmp_i]
    if Col_base_str == "":
        Col_base_str += "0"
    Base = int(Col_base_str,2)
    Offset = int(BRAM.Data_bit)


    # Update_Write
    for tmp_i in range(0,Offset):
        BRAM.Counter_Cell_level[subblock_id][Base][tmp_i] += 1
        if subblock_id >= type.num_region and BRAM.Counter_Cell_level[subblock_id][Base][tmp_i] > type.SLC_Lifetime:
            print(" Wear Out     SLC     Region:"+str(subblock_id) + "\n")
            return True # wear out
        elif subblock_id < type.num_region and BRAM.Counter_Cell_level[subblock_id][Base][tmp_i] > type.MLC_Lifetime:
            print(" Wear Out     MLC     Region:"+str(subblock_id) + "\n")
            return True # wear out
    return False



def Sim_BRAM(Handle_BRAMS):
    Write_Counter = 0
    Remapping_Counter = 0
    Trigger_Counter = 0
    FPGA_Wear_Flag = False
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                # Port 1
                if len(Handle_BRAMS.Dict[tmp_i].We1_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))]
                        Sel_write = int(tmp_add_freq,2)
                        if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                            num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                                slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                        else:
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                                slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                # Port 2
                if len(Handle_BRAMS.Dict[tmp_i].We2_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add2)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add2),int(math.log2(type.num_region)))]
                        Sel_write = int(tmp_add_freq,2)
                        if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                            num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                                slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                        else:
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                                slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)


                  
                  

def Baseline(Handle_BRAMS):
    Write_Counter = 0
    Remapping_Counter = 0
    Trigger_Counter = 0
    FPGA_Wear_Flag = False
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                # Port 1
                if len(Handle_BRAMS.Dict[tmp_i].We1_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        # tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))]
                        # Sel_write = int(tmp_add_freq,2)
                        # if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                        #     num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                        #     Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                        #     if Remapping_flag == True:
                        #         Trigger_Counter += 1
                        #         mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                        #         slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                        #         Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                        # else:
                        #     Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                        #     if Remapping_flag == True:
                        #         Trigger_Counter += 1
                        #         mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                        #         slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                        #         Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                # Port 2
                if len(Handle_BRAMS.Dict[tmp_i].We2_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add2)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        # tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add2),int(math.log2(type.num_region)))]
                        # Sel_write = int(tmp_add_freq,2)
                        # if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                        #     num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                        #     Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                        #     if Remapping_flag == True:
                        #         Trigger_Counter += 1
                        #         mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                        #         slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                        #         Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
                        # else:
                        #     Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                        #     if Remapping_flag == True:
                        #         Trigger_Counter += 1
                        #         mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                        #         slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
                        #         Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)

                  
                  

def Sim_BRAM_FIFO(Handle_BRAMS):
    Write_Counter = 0
    Remapping_Counter = 0
    Trigger_Counter = 0
    FPGA_Wear_Flag = False
    while(1):
        Read_Act(Handle_BRAMS)
        for tmp_k in range(0,5000):
            Write_Counter += 1
            for tmp_i in Handle_BRAMS.Dict:
                # Port 1
                if len(Handle_BRAMS.Dict[tmp_i].We1_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))]
                        Sel_write = int(tmp_add_freq,2)
                        if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                            num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],1)
                                slc_index_list, slc_cost_list = Select_SLC_strategy_FIFO(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping_FIFO(Handle_BRAMS.Dict[tmp_i],slc_index_list[0], slc_cost_list[0], mlc_index_list[0], mlc_cost_list[0])
                        else:
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],1)
                                slc_index_list, slc_cost_list = Select_SLC_strategy_FIFO(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping_FIFO(Handle_BRAMS.Dict[tmp_i],slc_index_list[0], slc_cost_list[0], mlc_index_list[0], mlc_cost_list[0])
                # Port 2
                if len(Handle_BRAMS.Dict[tmp_i].We2_input) != 0:
                    if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
                        tmp_address = ""
                        for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add2)):
                            tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
                        FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
                        if FPGA_Wear_Flag == True:
                            return Write_Counter, Remapping_Counter, Trigger_Counter
                        tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add2),int(math.log2(type.num_region)))]
                        Sel_write = int(tmp_add_freq,2)
                        if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
                            num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],1)
                                slc_index_list, slc_cost_list = Select_SLC_strategy_FIFO(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping_FIFO(Handle_BRAMS.Dict[tmp_i],slc_index_list[0], slc_cost_list[0], mlc_index_list[0], mlc_cost_list[0])
                        else:
                            Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
                            if Remapping_flag == True:
                                Trigger_Counter += 1
                                mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
                                slc_index_list, slc_cost_list = Select_SLC_strategy_FIFO(Handle_BRAMS.Dict[tmp_i])
                                Remapping_Counter += Remaping_FIFO(Handle_BRAMS.Dict[tmp_i],slc_index_list[0], slc_cost_list[0], mlc_index_list[0], mlc_cost_list[0])


             
             
             
# def Sim_BRAM_FIFO(Handle_BRAMS):
#     Write_Counter = 0
#     Remapping_Counter = 0
#     Trigger_Counter = 0
#     FPGA_Wear_Flag = False
#     while(1):
#         Read_Act(Handle_BRAMS)
#         for tmp_k in range(0,5000):
#             Write_Counter += 1
#             for tmp_i in Handle_BRAMS.Dict:
#                 # Port 1
#                 if len(Handle_BRAMS.Dict[tmp_i].We1_input) != 0:
#                     if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
#                         tmp_address = ""
#                         for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add1)):
#                             tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
#                         FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
#                         if FPGA_Wear_Flag == True:
#                             return Write_Counter, Remapping_Counter, Trigger_Counter
#                         tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))]
#                         Sel_write = int(tmp_add_freq,2)
#                         if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
#                             num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
#                             Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
#                             if Remapping_flag == True:
#                                 Trigger_Counter += 1
#                                 mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
#                                 slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
#                                 Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
#                         else:
#                             Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
#                             if Remapping_flag == True:
#                                 Trigger_Counter += 1
#                                 mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
#                                 slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
#                                 Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
#                 # Port 2
#                 if len(Handle_BRAMS.Dict[tmp_i].We2_input) != 0:
#                     if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
#                         tmp_address = ""
#                         for tmp_j in range(0,len(Handle_BRAMS.Dict[tmp_i].Add2)):
#                             tmp_address += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
#                         FPGA_Wear_Flag = Memory_write(Handle_BRAMS.Dict[tmp_i],tmp_address)
#                         if FPGA_Wear_Flag == True:
#                             return Write_Counter, Remapping_Counter, Trigger_Counter
#                         tmp_add_freq = tmp_address[0:min(len(Handle_BRAMS.Dict[tmp_i].Add2),int(math.log2(type.num_region)))]
#                         Sel_write = int(tmp_add_freq,2)
#                         if  Sel_write in Handle_BRAMS.Dict[tmp_i].Sel_Dict:
#                             num_current_slc = type.num_region + Handle_BRAMS.Dict[tmp_i].Sel_Dict[Sel_write]
#                             Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],num_current_slc)
#                             if Remapping_flag == True:
#                                 Trigger_Counter += 1
#                                 mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
#                                 slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
#                                 Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
#                         else:
#                             Remapping_flag = BRAM_counter(Handle_BRAMS.Dict[tmp_i],Sel_write)
#                             if Remapping_flag == True:
#                                 Trigger_Counter += 1
#                                 mlc_index_list, mlc_cost_list = Select_MLC_strategy(Handle_BRAMS.Dict[tmp_i],0.75)
#                                 slc_index_list, slc_cost_list = Select_SLC_strategy(Handle_BRAMS.Dict[tmp_i])
#                                 Remapping_Counter += Remaping(Handle_BRAMS.Dict[tmp_i],slc_index_list, slc_cost_list, mlc_index_list, mlc_cost_list)
       

# def Sim_BRAM_FIFO(Handle_BRAMS):
#     Write_Counter = 0
#     Remapping_Counter = 0
#     while(1):
#         Read_Act(Handle_BRAMS)
#         for tmp_k in range(0,5000):
#             Write_Counter += 1
#             for tmp_i in Handle_BRAMS.Dict:
#                 if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
#                     tmp_str = ""
#                     for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
#                         # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
#                         tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
#                     Sel_write = int(tmp_str,2)
#                     if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
#                         Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
#                         # Wear Out
#                         if Handle_BRAMS.Dict[tmp_i].Counter[8] > Handle_BRAMS.Dict[tmp_i].Up_limit[8]:
#                             return Write_Counter, Remapping_Counter
#                     else:
#                         Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
#                         # Wear Out
#                         if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Threshold[Sel_write]:
#                             # 
#                             Handle_BRAMS.Dict[tmp_i].Counter[Handle_BRAMS.Dict[tmp_i].Current_sel] += 1
#                             #
#                             Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
                            
                            
#                             Handle_BRAMS.Dict[tmp_i].Current_sel = Sel_write
#                             Remapping_Counter += 1
#                         if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Up_limit[Sel_write]:
#                             return Write_Counter, Remapping_Counter
#                 if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") == -1:
#                     if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
#                         tmp_str = ""
#                         for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
#                             if Handle_BRAMS.Dict[tmp_i].Num_add_2 > int(math.log2(type.num_region)):
#                                 tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
#                         Sel_write = int(tmp_str,2)
#                         if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
#                             Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
#                         else:
#                             Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
#                             if Handle_BRAMS.Dict[tmp_i].Current_sel != -1:
#                                 Handle_BRAMS.Dict[tmp_i].Freq_counter[Sel_write] += 1 



# def Sim_BRAM_Non(Handle_BRAMS):
#     Write_Counter = 0
#     Remapping_Counter = 0    
#     while(1):
#         Read_Act(Handle_BRAMS)
#         for tmp_k in range(0,5000):
#             Write_Counter += 1
#             for tmp_i in Handle_BRAMS.Dict:
#                 if Handle_BRAMS.Dict[tmp_i].We1_input[tmp_k] == 1:
#                     tmp_str = ""
#                     for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
#                         # if Handle_BRAMS.Dict[tmp_i].Num_add_1 > int(math.log2(type.num_region)):
#                         tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_1_input[Handle_BRAMS.Dict[tmp_i].Add1[tmp_j]][tmp_k])
#                     Sel_write = int(tmp_str,2)
#                     if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
#                         Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
#                         # Wear Out
#                         if Handle_BRAMS.Dict[tmp_i].Counter[8] > Handle_BRAMS.Dict[tmp_i].Up_limit[8]:
#                             return Write_Counter,Remapping_Counter
#                     else:
#                         Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
#                         # Wear Out
#                         if Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] > Handle_BRAMS.Dict[tmp_i].Up_limit[Sel_write]:
#                             return Write_Counter,Remapping_Counter
#                 if Handle_BRAMS.Dict[tmp_i].Mode.find("sp") == -1:
#                     if Handle_BRAMS.Dict[tmp_i].We2_input[tmp_k] == 1:
#                         tmp_str = ""
#                         for tmp_j in range(0,min(len(Handle_BRAMS.Dict[tmp_i].Add1),int(math.log2(type.num_region)))):
#                             if Handle_BRAMS.Dict[tmp_i].Num_add_2 > int(math.log2(type.num_region)):
#                                 tmp_str += str(Handle_BRAMS.Dict[tmp_i].Add_2_input[Handle_BRAMS.Dict[tmp_i].Add2[tmp_j]][tmp_k])
#                         Sel_write = int(tmp_str,2)
#                         if Sel_write == Handle_BRAMS.Dict[tmp_i].Current_sel:
#                             Handle_BRAMS.Dict[tmp_i].Counter[8] += 1
#                         else:
#                             Handle_BRAMS.Dict[tmp_i].Counter[Sel_write] += 1
#                             if Handle_BRAMS.Dict[tmp_i].Current_sel != -1:
#                                 Handle_BRAMS.Dict[tmp_i].Freq_counter[Sel_write] += 1 
