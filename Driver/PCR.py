import numpy as np
from tqdm import tqdm 

MISTAKE = 5000

def amplify(pool, num_cycle):

    pbar = tqdm(total= num_cycle, desc= "PCR rounds completed")

    pool = np.array(pool)
    
    for cycle in range(num_cycle):
        clone = []
        for oligo in pool:
            mistake = np.random.randint(MISTAKE, size= len(oligo))
            
            pcr_oligo = [None] * len(oligo)
            for nt in range(len(oligo)):
                if mistake[nt] < 0:
                    pcr_oligo[nt] = loss_or_gain(oligo[nt])                  
                elif mistake[nt] == 10:
                    pcr_oligo[nt] = transition(oligo[nt])
                else:
                    pcr_oligo[nt] = oligo[nt]
            clone.append(''.join(pcr_oligo))
        pool = np.append(pool, clone)

        pbar.update()
    pbar.close()
    
    return pool

def transition(base):
    if base == 'A':
        return 'G'
    elif base == 'C':
        return 'T'
    elif base == 'G':
        return 'A'
    elif base == 'T':
        return 'C'
    else:
        return base
    
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
        
