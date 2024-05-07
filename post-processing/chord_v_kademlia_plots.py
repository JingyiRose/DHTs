import matplotlib.pyplot as plt
import numpy as np
import sys,os
import os.path
import statistics


def read_chord_output_file(filename):
    with open(filename) as f:
        hops = [int(line.split("=")[-1]) for line in f]
    f.close()
    return hops

def get_average_hops(filename):
    hops = read_chord_output_file(filename)
    return statistics.mean(hops)


def make_plot(xs_labels, chord_hops, kademlia_hops, filename=None):
    # ax = plt.gca()
    # ax.set_ylim([1, 4])
    default_x_ticks = range(len(xs_labels))
    if chord_hops:
        plt.errorbar(default_x_ticks, chord_hops, linestyle='None', marker='o', color='b', label="Chord's average #hops")
    if kademlia_hops:
        plt.errorbar(default_x_ticks, kademlia_hops, linestyle='None', marker='o', color='r', label="Kademlia's average #hops")
    plt.xticks(default_x_ticks, xs_labels)
    plt.margins(0.2)
    plt.legend()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()

def plot_eval1():
    xs_labels = ["#nodes=20", "#nodes=50", "#nodes=100"]
    filename = "eval1.png" 
    dir = os.path.dirname(os.getcwd()+"/DHTs")
 
    chord_n20 = get_average_hops(dir + "/Evaluation/output_chord/reply_n20.txt")
    chord_n50 = get_average_hops(dir + "/Evaluation/output_chord/reply_n50.txt")
    chord_n100 = get_average_hops(dir + "/Evaluation/output_chord/reply_n100.txt")
    chord_hops = [chord_n20, chord_n50, chord_n100]

    kademlia_n20 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation1/reply_n20.txt")
    kademlia_n50 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation1/reply_n50.txt")
    kademlia_n100 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation1/reply_n100.txt")
    kademlia_hops = [kademlia_n20, kademlia_n50, kademlia_n100]

    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)

   
def plot_eval2():
    xs_labels = ["p_insert=0.05", "p_insert=0.10", "p_insert=0.25", "p_insert=0.50"] 
    filename = "eval2.png" 
    dir = os.path.dirname(os.getcwd()+"/DHTs")
 
    chord_p005 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_insert_005.txt")
    chord_p010 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_insert_010.txt")
    chord_p025 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_insert_025.txt")
    chord_p050 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_insert_050.txt")
    chord_hops = [chord_p005, chord_p010, chord_p025, chord_p050]

    kademlia_p005 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation2/reply_p_insert_005.txt")
    kademlia_p010 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation2/reply_p_insert_010.txt")
    kademlia_p025 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation2/reply_p_insert_025.txt")
    kademlia_p050 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation2/reply_p_insert_050.txt")
    kademlia_hops = [kademlia_p005, kademlia_p010, kademlia_p025, kademlia_p050]

    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)
   

def plot_eval3():
    xs_labels = ["p_nodejoin=0.002", "p_nodejoin=0.01", "p_nodejoin=0.02"]
    filename = "eval3.png"
    dir = os.path.dirname(os.getcwd()+"/DHTs") 

    chord_p0002 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_nodejoin_002.txt")
    chord_p01 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_nodejoin_01.txt")
    chord_p02 = get_average_hops(dir + "/Evaluation/output_chord/reply_p_nodejoin_02.txt")
    chord_hops = [chord_p0002, chord_p01, chord_p02]

    kademlia_p0002 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation3/reply_p_nodejoin_002.txt")
    kademlia_p01 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation3/reply_p_nodejoin_01.txt")
    kademlia_p02 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation3/reply_p_nodejoin_02.txt")
    kademlia_hops = [kademlia_p0002, kademlia_p01, kademlia_p02]

    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)


def plot_eval4():
    xs_labels = ["no left-bias", "bias=0.80", "bias=0.90", "bias=0.90", "bias=0.99"]
    filename = "eval4.png" 
    dir = os.path.dirname(os.getcwd()+"/DHTs")
 
    chord_no_bias = get_average_hops(dir + "/Evaluation/output_chord/reply_n50.txt")
    chord_b80 = get_average_hops(dir + "/Evaluation/output_chord/reply_b80.txt")
    chord_b90 = get_average_hops(dir + "/Evaluation/output_chord/reply_b90.txt")
    chord_b95 = get_average_hops(dir + "/Evaluation/output_chord/reply_b95.txt")
    chord_b99 = get_average_hops(dir + "/Evaluation/output_chord/reply_b99.txt")
    chord_hops = [chord_no_bias, chord_b80, chord_b90, chord_b95, chord_b99]

    kademlia_no_bias = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation1/reply_n50.txt")
    kademlia_b80 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation4/reply_b80.txt")
    kademlia_b90 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation4/reply_b90.txt")
    kademlia_b95 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation4/reply_b95.txt")
    kademlia_b99 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation4/reply_b99.txt")
    kademlia_hops = [kademlia_no_bias, kademlia_b80, kademlia_b90, kademlia_b95, kademlia_b99]
    
    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)

   

def plot_eval5():
    xs_labels = ["no left-bias", "bias=0.80", "bias=0.90", "bias=0.90", "bias=0.99"]
    filename = "eval5.png"
    dir = os.path.dirname(os.getcwd()+"/DHTs") 

    chord_no_bias = get_average_hops(dir + "/Evaluation/output_chord/reply_p_insert_050.txt")
    chord_b80 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_b80.txt")
    chord_b90 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_b90.txt")
    chord_b95 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_b95.txt")
    chord_b99 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_b99.txt")
    chord_hops = [chord_no_bias, chord_b80, chord_b90, chord_b95, chord_b99]

    kademlia_no_bias = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation2/reply_p_insert_050.txt")
    kademlia_b80 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation5/reply_lookup_insert_b80.txt")
    kademlia_b90 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation5/reply_lookup_insert_b90.txt")
    kademlia_b95 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation5/reply_lookup_insert_b95.txt")
    kademlia_b99 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation5/reply_lookup_insert_b99.txt")
    kademlia_hops = [kademlia_no_bias, kademlia_b80, kademlia_b90, kademlia_b95, kademlia_b99]
    
    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)

   


def plot_eval6(): 
    xs_labels = ["no left-bias", "bias=0.80", "bias=0.90", "bias=0.90", "bias=0.99"]
    filename = "eval6.png"
    dir = os.path.dirname(os.getcwd()+"/DHTs")

    chord_no_bias = get_average_hops(dir + "/Evaluation/output_chord/reply_p_nodejoin_01.txt")
    chord_b80 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_nodejoin_b80.txt")
    chord_b90 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_nodejoin_b90.txt")
    chord_b95 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_nodejoin_b95.txt")
    chord_b99 = get_average_hops(dir + "/Evaluation/output_chord/reply_lookup_insert_nodejoin_b99.txt")
    chord_hops = [chord_no_bias, chord_b80, chord_b90, chord_b95, chord_b99]

    kademlia_no_bias = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation3/reply_p_nodejoin_01.txt")
    kademlia_b80 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation6/reply_lookup_insert_nodejoin_b80.txt")
    kademlia_b90 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation6/reply_lookup_insert_nodejoin_b90.txt")
    kademlia_b95 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation6/reply_lookup_insert_nodejoin_b95.txt")
    kademlia_b99 = get_average_hops(dir + "/Evaluation/output_kademlia/Evaluation6/reply_lookup_insert_nodejoin_b99.txt")
    kademlia_hops = [kademlia_no_bias, kademlia_b80, kademlia_b90, kademlia_b95, kademlia_b99]
    
    make_plot(xs_labels, chord_hops, kademlia_hops, filename=filename)




if __name__ == "__main__":
    os.chdir("/Users/jingyiliu/Desktop/DHTs" )
    plot_eval1()
    plot_eval2()
    plot_eval3()
    plot_eval4()
    plot_eval5()
    plot_eval6()
