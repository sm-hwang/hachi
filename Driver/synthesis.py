import numpy as np
from tqdm import tqdm

MUTATION_CHANCE = 1.0/500
DELETION = 0
INSERTION = 1

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

def synthesize(oligo_list):

    pbar = tqdm(total= len(oligo_list), desc= "Synthesized oligos")
    
    pool = []

    for oligo in oligo_list:
        
        mutated = np.random.randint(int(MUTATION_CHANCE ** -1), size= len(oligo))    #generating list of integers between 0 - (1/MUTATION_CHANCE).
                                                                                     #length of list is equal to length of oligo in nt.
        synth_dna = [None] * len(oligo)
        
        for i, chance in enumerate(mutated):            
            if chance == 0:                             #If mutated[i] == 0, then it is mutated 
                synth_dna[i] = mutate(oligo[i])
            else:
                synth_dna[i] = oligo[i]

        pool.append("".join(synth_dna))

        pbar.update()
    pbar.close()
    return pool
        

