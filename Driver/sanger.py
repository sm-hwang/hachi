import numpy as np
from tqdm import tqdm

def choose_oligos(pool_size, stop):
    #returns np.array of size "stop" of numbers between and pool_size - 1
    #Every number in the array is unique
    return np.random.choice(a= pool_size, size= stop, replace= False)

def sequence(np_pool, stop):
    pbar = tqdm(total= stop, desc= "Sequenced oligos")
    
    sequence_data = [None] * stop
    picked = choose_oligos(np_pool.size, stop)
    for i,seq in enumerate(picked):
        sequence_data[i] = np_pool[seq]
        pbar.update()
    pbar.close()
    
    return np.array(sequence_data)
    
def calc_stop(num, per, size):
    if num is None:
        return int(per * size)
    else:
        return num
    
