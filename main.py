'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-28 07:10:41
LastEditTime: 2021-12-30 08:54:40
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/main.py
'''
import read_circuit
import read_activate
import type
import os

Benchmark_path = "/home/zhlab/Aurora/Benchmark"

circuit_name = [tmp.replace(".v", "") for tmp in os.listdir(Benchmark_path)]



def my_exists(path):
    if path.find(".net") != -1:
        if os.path.exists(path):
            return True
        else:
            print("ERROR: " + path + " IS NOT EXIST;")
            return False
    elif path.find(".odin.blif") != -1:
        if os.path.exists(path):
            return True
        else:
            print("ERROR: " + path + " IS NOT EXIST;")
            return False
    elif path.find("output_activity") != -1:
        if os.path.exists(path):
            return True
        else:
            print("ERROR: " + path + " IS NOT EXIST;")
            return False
        
def Init_Gen_ACT(path, cur_circuit):
    os.chdir(path)
    # print(os.getcwd())
    command = "cp /home/zhlab/Aurora/vtr-verilog-to-routing-8.0.0/build/ODIN_II/odin_II " + path
    os.system(command)
    command = "./odin_II " + "-b " + cur_circuit + ".odin.blif" + " -g 100 -U1"
    os.system(command)
    

    
for cur_circuit in circuit_name:
    print("Process for " + cur_circuit)
    Path_of_circuit = Benchmark_path + "/" + cur_circuit + ".v/common/"
    Path_of_circuit_net = Path_of_circuit  + cur_circuit + ".net"
    Path_of_circuit_act = Path_of_circuit + "output_activity"
    if my_exists(Path_of_circuit_net):
        Handle_BRAMS = type.BRAMS()
        read_circuit.Parse4BRAMINF(Path_of_circuit_net, Handle_BRAMS)
        print("---------Parse4BRAMINF OK---------")
        if my_exists(Path_of_circuit_act) is False:
            Init_Gen_ACT(Path_of_circuit, cur_circuit)
            print("---------Gen_ACT OK---------")
        if my_exists(Path_of_circuit_act) is True: # For some cricuits, Init_Gen_ACT() fail to run.
            read_activate.Parse4ACT(Path_of_circuit_act, Handle_BRAMS)
            print("---------Parse4ACT OK---------")
        print("\n")

pass