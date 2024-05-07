import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from Framework.controller_v2 import *

from Chord.chord6 import *




def eval_chord(folder_name, label):
    start_filename =  os.getcwd() + "/{}/init_{}.txt".format(folder_name, label)
    normal_ops_filename =  os.getcwd() + "/{}/normal_ops_{}.txt".format(folder_name, label)
    rep_filename = os.getcwd() + "/output_chord/reply_{}.txt".format(label)
    L = 12
    dht = Chord6(L)
    controller = ControllerV2(start_filename, normal_ops_filename, dht, rep_filename, makenode_sleep=0)
    controller.execute()
    # test_hard(start_filename, normal_ops_filename, rep_filename, m = L)


if __name__ == "__main__":
    # folder_name = "Evaluation1"
    # label = "n100"
    # eval_chord(folder_name, label)

    # folder_name = "Evaluation2"
    # label = "p_insert_050"
    # eval_chord(folder_name, label)

    # folder_name = "Evaluation3"
    # label = "p_nodejoin_01"
    # eval_chord(folder_name, label)

    # folder_name = "Evaluation6"
    # label = "lookup_insert_nodejoin_b80"
    # eval_chord(folder_name, label)
    
    pass
    

    
