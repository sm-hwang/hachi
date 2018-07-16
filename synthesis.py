import argparse
import logging
import random
import sys
import numpy as np

MUTATION_CHANCE = 1/500
HEADER = 'packet'
DELETION = 0
INSERTION = 1

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="file with oligos to synthesize", required=True)
    parser.add_argument("--oligo_size", help="Size of the oligos in nt", required=True)
    parser.add_argument("--output", help="File with synthesized oligos", required=True)

    args = parser.parse_args()

    return(args)

    
def mutate(base):
    chance = np.random.randint(0,3)
    nt_list = ['A','C','G','T','P','Z']
    if chance == DELETION:
        nt = ""
    elif chance == INSERTION:
        nt = base + np.random.choice(nt_list)
    else: #Substitution
        nt_list.remove(base)
        nt = np.random.choice(nt_list)
    return nt


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

    for oligo in f:
        
        if HEADER in oligo: #Reading the header for the oligo
            continue
        
        oligo.rstrip("\n")
        
        mutated = np.random.randint(int(MUTATION_CHANCE ** -1), size= len(oligo)) #generating list of random integers between 0 - (1/MUTATION_CHANCE). Length of list is equal to oligo size in nt.

        synth_dna = []

        for i, chance in enumerate(mutated):            #np.ndenumerate() for numpy
            if chance == 0:                             #If mutated[i] == 0, then it is mutated 
                synth_dna.append(mutate(oligo[i]))
            else:
                synth_dna.append(oligo[i])

        out.write("".join(synth_dna))
        
    f.close()
    out.close()
          
main()
