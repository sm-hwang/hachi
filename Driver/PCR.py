import numpy as np
from tqdm import tqdm 

def set_error_rate(worst_case, no_synth, errorN):
    global mistake_per, synth_error, gen_error
    if worst_case:
        mistake_per = 5000
    else:
        mistake_per = 100000
    if no_synth:
        synth_error = 0
    else:
        synth_error = 0.002
    gen_error = False
    if errorN:
        gen_error = True

def amplify(pool, num_cycle):

    within_prob = int(synth_error * mistake_per)
    pbar = tqdm(total= num_cycle, desc= "PCR rounds completed")

    pool = np.array(pool)
    
    for cycle in range(num_cycle):
        clone = []
        for oligo in pool:
            mistake = np.random.randint(mistake_per, size= len(oligo))
            
            pcr_oligo = [None] * len(oligo)
            for nt in range(len(oligo)):
                if mistake[nt] < within_prob:
                    pcr_oligo[nt] = loss_or_gain(oligo[nt])                  
                elif mistake[nt] == within_prob:
                    pcr_oligo[nt] = transition(oligo[nt])
                else:
                    pcr_oligo[nt] = oligo[nt]
            clone.append(''.join(pcr_oligo))
        pool = np.append(pool, clone)

        pbar.update()
    pbar.close()
    
    return pool

def transition(base):
    if gen_error:
        return 'N'
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
    if gen_error:
        return 'N'
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
        
