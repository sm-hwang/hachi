

import argparse
import logging
import random
import sys

#Can be optimzed using numpy
#Check if the specified oligo_size does not match the oligo in the input file
#Add progress bars using tqdm
#Substitution can't be the same base it started out with

MUTATION_CHANCE = 1/500
HEADER = 'packet'
DELETION = 0
INSERTION = 1
A = 0 
C = 1
G = 2
T = 3
P = 4
Z = 5

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="file with oligos to synthesize", required=True)
    parser.add_argument("--oligo_size", help="Size of the oligos in nt", required=True)
    parser.add_argument("--output", help="File with synthesized oligos", required=True)

    args = parser.parse_args()

    return(args)

    
def mutate(base):
    chance = random.randrange(0,3)
    if chance == DELETION:
        nt = ""
    elif chance == INSERTION:
        insert_nt = random.randrange(0,6)
        if insert_nt == A:
            nt = base + 'A'
        elif insert_nt == C:
            nt = base + 'C'
        elif insert_nt == G:
            nt = base + 'G'
        elif insert_nt == T:
            nt = base + 'T'
        elif insert_nt == P:
            nt = base + 'P'
        else:
            nt = base + 'Z'
    else: #Substitution
        sub_nt = random.randrange(0,6)
        if sub_nt == A:
            nt = 'A'
        elif sub_nt == C:
            nt = 'C'
        elif sub_nt == G:
            nt = 'G'
        elif sub_nt == T:
            nt = 'T'
        elif sub_nt == P:
            nt = 'P'
        else:
            nt = 'Z'
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

        mutated = [random.randrange(0, int(MUTATION_CHANCE ** -1)) for i in range(arg.oligo_size)] #generating list of random integers between 0 - (1/MUTATION_CHANCE).

        synth_dna = []

        for i, chance in enumerate(mutated):
            if chance == 0:                             #If mutated[i] == 0, then it is mutated 
                synth_dna.append(mutate(oligo[i]))
            else:
                synth_dna.append(oligo[i])

        out.write("".join(synth_dna))
        
    f.close()
        
        
main()
