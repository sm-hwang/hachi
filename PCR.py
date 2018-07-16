import sys
import argparse
import numpy as np

LOSS_GAIN_PER = 500 #Loss and gain of P:Z is 0.2% per theoretical PCR cycle

#implementation of dropouts?

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="File with synthesized oligos", required=True)
    parser.add_argument("--pcr_cycles", help="Number of PCR cycles", default = 10, type = int)
    parser.add_argument("--output", help="File with simulated oligos", required=True)
    args = parser.parse_args()

    return(args)

def loss_or_gain(base):
    synthetic = ['P', 'Z']
    if base in synthetic:
        return loss(base)
    else:
        return gain(base)
    
def gain(base):
    nt = base
    if base == 'C':
        nt = 'Z'
    return nt

def loss(base):
    if base == 'Z':
        return np.random.choice(['T', 'C'], p = [0.05,0.95])
    else:
        return np.random.choice(['A', 'G'], p = [0.7,0.3])
        

def main():

    args = read_args()

    try:
        f = open(args.file_in, 'r')
    except:
        print("%s file not found", args.file_in)
        sys.exit(0)

    if (args.output == '-'):
        out = sys.stdout
    else:
        out = open(args.output, 'w')
    
    pool = []

    #Unnecessary with driver program
    for oligo in f:
        pool.append(oligo)
    pool = np.array(pool)

    f.close()

    for i in range(args.pcr_cycles):
        clone = []
        for oligo in pool:

            oligo.rstrip("\n")
            
            mistake = np.random.randint(LOSS_GAIN_PER, size = len(oligo))

            pcr_oligo = ""
            for i in range(len(oligo)):
                if mistake[i] == 0:
                    pcr_oligo += loss_or_gain(oligo[i])
                else:
                    pcr_oligo += oligo[i]
            clone.append(pcr_oligo)
        pool = np.append(pool, clone)

    for oligo in pool:
        out.write(oligo)
    out.close()
    
main()
