import numpy as np
from tqdm import tqdm 

LOSS_GAIN_PER = 500 #Loss and gain of P:Z is 0.2% per theoretical PCR cycle

#Deleting pool after being converted to np.array?
def amplify(pool, num_cycle):

    pbar = tqdm(total= num_cycle, desc= "PCR rounds completed")

    np_pool = np.array(pool)
    
    for cycle in range(num_cycle):
        clone = []
        for oligo in np_pool:
            mistake = np.random.randint(LOSS_GAIN_PER, size= len(oligo))
            
            pcr_oligo = [None] * len(oligo)
            for nt in range(len(oligo)):
                if mistake[nt] == 0:
                    pcr_oligo[nt] = loss_or_gain(oligo[nt])                  
                else:
                    pcr_oligo[nt] = oligo[nt]
            clone.append(''.join(pcr_oligo))
        np_pool = np.append(np_pool, clone)

        pbar.update()
    pbar.close()
    
    return np_pool

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
        
