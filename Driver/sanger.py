import sys
import numpy as np
from tqdm import tqdm

def choose_oligos(pool_size, stop):
    return np.random.choice(a= pool_size, size= stop, replace= False)

def sequence(np_pool, stop):
    pbar = tqdm(total= stop, desc= "Sequenced oligos")
    
    sequence_data = []
    picked = choose_oligos(np_pool.size, stop)
    for seq in picked:
        sequence_data.append(np_pool[seq])
        pbar.update()
    pbar.close()
    return np.array(sequence_data)
    
def calc_stop(num, per, size):
    if num is None:
        return int(per * size)
    else:
        return num
    
