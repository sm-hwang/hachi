import numpy as np
from tqdm import tqdm

#Genome wide sequencing error rate reported as 0.0034
ERRORS_PER_TT = 34 #Errors per ten thousand
TT = 10000

def negbin_cov(avg_cov, size_para, count, copies):
    prob = size_para / float(size_para + avg_cov)
    sample = np.random.negative_binomial(size_para, prob, count)
    dropout = 0
    
    for num in range(count):
        sample[num] = sample[num] * copies
        if sample[num] == 0:
            dropout += 1
    print "{0:.2f}".format(dropout * 100/ float(count)) + "% dropout" #(Munsu)
    
    return sample

def prepare_list(oligo_list, avg_cov, size_para, count, copies):

    sample = negbin_cov(avg_cov, size_para, count, copies)

    synth_list = []
    
    for each in range(count):
        for cov in range(sample[each]):
            synth_list.append(oligo_list[each])

    return np.array(synth_list)

        
def choose_oligos(pool_size, stop):
    #returns np.array of size "stop" of numbers between 0 and pool_size - 1
    #Every number in the array is unique
    return np.random.choice(a= pool_size, size= stop, replace= False)


def sequence(np_pool, count, avg_cov):

    stop = int(count * avg_cov)
    error = np.random.randint(TT, size= stop)
    
    pbar = tqdm(total= stop, desc= "Sequenced oligos")
    
    sequence_data = [None] * stop
    picked = choose_oligos(np_pool.size, stop)
    for i,seq in enumerate(picked):
        if error[i] < ERRORS_PER_TT:
            #Induce a general error 
            sequence_data[i] = np_pool[seq] + 'N'
        else:
            sequence_data[i] = np_pool[seq]
        pbar.update()
    pbar.close()
    return np.array(sequence_data)


    
    
