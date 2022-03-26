'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-28 07:10:41
LastEditTime: 2022-03-26 07:47:32
LastEditors: Please set LastEditors
Description: Read the logical BRAM instance
FilePath: /Aurora/read_circuit.py
'''

# To get BRAM's infomation easily, I will parse the .net file rathen than .v or .blif file. 
# To be honest, parse the .v is a wiser choose. But I do not understand the mechanism of verilog high-level synthesis.

import os
import xml.etree.ElementTree as ET
import type
import math


# <port name="addr1">top^mesgRF_rWrPtr~8_FF_NODE top^mesgRF_rWrPtr~9_FF_NODE open open open open open</port>
# For some address port, the "open" means invaild input pin. I will remove it when I count the pin's information.			
Replace_key_word_0 = "open"
Replace_key_word_1 = "gnd"
Replace_key_word_2 = "vcc"


'''
description:  
param {Circuit_path}
return {BRAMS()}
'''
def Parse4BRAMINF(Path_of_circuit, Handle_BRAMS):
    Path_of_circuit = Path_of_circuit;
    Path_of_BRAMPin = Path_of_circuit[:Path_of_circuit.rfind("/")+1] + Path_of_circuit[Path_of_circuit.rfind("/")+1:Path_of_circuit.rfind(".")] +"_BRAMPin.txt"

    Writer_Set = set();

    '''
    description: Find the vaild pin of BRAM
    '''
    dom = ET.parse(Path_of_circuit);
    root = dom.getroot();
    # print(root) 
    level_1 = root.findall("block")

    Handle_BRAMS = Handle_BRAMS
    Handle_BRAMS._init_()

    for child_node_l_1 in level_1:
        # find node with type is memory.  
        if child_node_l_1.attrib.get("instance").find("memory[") != -1:
            Name = child_node_l_1.attrib.get("name")
            Instance = child_node_l_1.attrib.get("instance")
            Mode = child_node_l_1.attrib.get("mode")
            # It can parse dual and single bram. 
            level_2 = child_node_l_1.find("inputs");
            level_3 = level_2.findall("port");
            # level_3 port_0:addr1 port_1:addr2     port_2:data     port_3:we1   port_4:we2 
            Addr1_List = level_3[0].text.replace(Replace_key_word_0,"").replace(Replace_key_word_1,"").replace(Replace_key_word_2,"").split();
            Addr2_List = level_3[1].text.replace(Replace_key_word_0,"").replace(Replace_key_word_1,"").replace(Replace_key_word_2,"").split();
            We1 = level_3[3].text.replace(" ", "");
            We2 = level_3[4].text.replace(" ", "");
            if (We1 != "gnd") and (We1 != "open") and (len(Addr1_List) != 0) :
                # Writer.write(We1+"\n");
                Writer_Set.add(We1)
                for tmp in Addr1_List:
                    Writer_Set.add(tmp)
                    # Writer.write(tmp+"\n");
            if (We2 != "gnd") and (We2 != "open") and (len(Addr2_List) != 0):
                # Writer.write(We2+"\n");
                Writer_Set.add(We2)
                for tmp in Addr2_List:
                    Writer_Set.add(tmp)
                    # Writer.write(tmp+"\n");
            Handle_BRAMS.Dict[Instance] = type.BRAM()
            Mode_list = Mode.replace("x"," ").replace("_"," ").split()
            Real_add_bit = int(math.log2(int(Mode_list[1])))
            Real_data_bit = int(Mode_list[2])
            Handle_BRAMS.Dict[Instance]._init_(name = Name, instance = Instance, mode = Mode, add1 = Addr1_List, add2 = Addr2_List, we1 = We1, we2 = We2, address_bit = Real_add_bit, data_bit = Real_data_bit)

    '''
    description: Save the vaild pin of BRAM 
    '''
    Writer = open(Path_of_BRAMPin,"w");
    for tmp in Writer_Set:
        Writer.write(tmp+"\n");
    Writer.close()

    return Handle_BRAMS