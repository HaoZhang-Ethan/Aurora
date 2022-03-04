'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-28 07:10:41
LastEditTime: 2022-01-02 06:04:35
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/main.py
'''
from multiprocessing import Condition
import read_circuit
import read_activate
import simulator
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
    command = "cp /home/embed2/Aurora-main/vtr-verilog-to-routing-8.0.0/build/ODIN_II/odin_II " + path
    os.system(command)
    command = "./odin_II " + "-b " + cur_circuit + ".odin.blif" + " -g 100 -U1"
    os.system(command)
    


                    

for cur_circuit in circuit_name:
    print("Process for " + cur_circuit)
    Path_of_circuit = Benchmark_path + "/" + cur_circuit + ".v/common/"
    Path_of_circuit_net = Path_of_circuit  + cur_circuit + ".net"
    Path_of_circuit_act = Path_of_circuit + "output_activity"
    Path_of_circuit_pin_act = Path_of_circuit  + cur_circuit + "_BRAMPin.txt"
    Path_of_circuit_place = Path_of_circuit + cur_circuit + ".place"
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
        # if my_exists(Path_of_circuit_pin_act) is True: # For some cricuits, Init_Gen_ACT() fail to run.
        #     read_activate.Parse4PinACT(Path_of_circuit_pin_act, Handle_BRAMS)
        #     print("---------Parse4ACT OK---------")
        # simulator.Init_Sim_BRAM(Handle_BRAMS,Path_of_circuit_place)
        Lifetime,Swap_num = simulator.Sim_BRAM(Handle_BRAMS)
        # Lifetime,Swap_num = simulator.Sim_BRAM_FIFO(Handle_BRAMS)
        # Lifetime,Swap_num = simulator.Sim_BRAM_Non(Handle_BRAMS)
        print("Lifetime = " + str(Lifetime) + "\t","Swap_num = " + str(Swap_num) + "\n")
        print("\n")

pass