import numpy as np
from tqdm import tqdm

DELETION = 0
INSERTION = 1

def set_mutation_rate(worst_case, no_synth):
    global mutation_per, nt_list
    if worst_case:
        mutation_per = 500
    else:
        mutation_per = 750
    if no_synth:
        nt_list = ['A','C','G','T']
    else:
        nt_list = ['A','C','G','T','P','Z']

def mutate(base):
    chance = np.random.randint(0,3) #Each type of mistakes are equiprobable
    if chance == DELETION:
        nt = ""
    elif chance == INSERTION:
        nt = base + np.random.choice(nt_list)
    else: #Substitution
        nt_choices = list(nt_list)
        nt_choices.remove(base)
        nt = np.random.choice(nt_choices)
    return nt

def synthesize(oligo_list):

    pbar = tqdm(total= len(oligo_list), desc= "Synthesized oligos")
    
    pool = []

    for oligo in oligo_list:
        
        mutated = np.random.randint(mutation_per, size= len(oligo))    #generating list of integers between 0 - mutation_per.
                                                                                     #length of list is equal to length of oligo in nt.
        synth_dna = [None] * len(oligo)
        
        for nt, chance in enumerate(mutated):            
            if chance == 0:                             #If mutated[i] == 0, then it is mutated 
                synth_dna[nt] = mutate(oligo[nt])
            else:
                synth_dna[nt] = oligo[nt]
        pool.append("".join(synth_dna))

        pbar.update()
    pbar.close()
    
    return pool
        

