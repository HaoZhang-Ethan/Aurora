'''
Author: HaoZhang-Hoge@SDU
Date: 2021-12-28 07:10:41
LastEditTime: 2021-12-29 08:33:45
LastEditors: Please set LastEditors
Description: 
FilePath: /Aurora/main.py
'''
import read_circuit
import read_activate
import type

Path_of_circuit = "/home/zhlab/VTR-Oreo/vtr_flow/tasks/timing/run001/k6_frac_N10_mem32K_40nm.xml/LU8PEEng.v/common/LU8PEEng.net"
Path_of_act = "/home/zhlab/VTR-Oreo/build/ODIN_II/output_activity"
Handle_BRAMS = type.BRAMS()
read_circuit.Parse4BRAMINF(Path_of_circuit, Handle_BRAMS)
read_activate.Parse4ACT(Path_of_act, Handle_BRAMS)
pass