import argparse
import sys
import numpy as np
from tqdm import tqdm


HEADER = 'packet'
SYNTH_ERROR_RATE = 1 / 500.0
PCR_ERROR_RATE = 0.0022
SEQ_ERROR_RATE = 0.0034
PCR_EFFICIENCY = 1.00


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="File with oligos to synthesize", required=True)
    parser.add_argument("--pcr_cycles", help="Number of PCR cycles", default = 10, type= int)
    parser.add_argument("--avg_cov", help="Average oligo coverage when sequencing", default = 10, type= int)
    parser.add_argument("--size_para", help="Size parameter for sequencing coverage", default = 2, type= int)
    parser.add_argument("--copies", help= "Number of copies of oligos to synthesize", default = 1, type= int)
    parser.add_argument("--output", help="File with sequenced oligos", required=True)
    args = parser.parse_args()

    return(args)


def read_oligo_list(file_name):

    try:
        f = open(file_name, 'r')
    except:
        print "%s file not found", file_name
        sys.exit(0)

    oligo_list = []

    for oligo in f:

        if HEADER in oligo:     #Reading the header for the oligo
            continue

        oligo_list.append(oligo.rstrip("\n"))

    f.close()

    len_oligo = len(oligo_list[0])
    pool_size = len(oligo_list)

    return oligo_list, len_oligo, pool_size


def write_data(output, chosen_oligos, seq_mistakes):
    print "file is: " + output
    out = open(output, 'w')
    count = 0
    for oligo in chosen_oligos:
        if oligo != None:
            out.write(oligo + "\n")
    out.close()
    print "Read " + str(seq_mistakes) + " oligos with mistakes in them"


def calcCoverage(avg_cov, size_para, pool_size):
    prob = avg_cov / float(size_para + avg_cov)
    return np.random.negative_binomial(size_para, prob, pool_size)


def negbin_cov(avg_cov, size_para, pool_size):                                         #Does this improve it
    sample = calcCoverage(size_para, prob, pool_size)                    #np.random.negative_binomial(size_para, prob, pool_size)
    return sample


def sampleBinomial(numTrials, successProb, sampleSize):
    return np.random.binomial(numTrials, successProb, sampleSize)


def sampleSynthError(len_oligo, totOligoCount):
    return sampleBinomial(len_oligo, SYNTH_ERROR_RATE, totOligoCount)


def synthesize(len_oligo, sample, copies):
    mistakes = 0
    synth_error = sampleSynthError(len_oligo, sample.size * copies)    #wrapper function for this one of more intuitive name

    num_copy = []
    pbar = tqdm(total= sample.size, desc= "Synthesized oligos")
    for i in xrange(sample.size):
        copy = 0
        offset = copies * i
        for j in xrange(copies):
            if synth_error[offset + j] == 0:
                copy += sample[i]
            else:
                mistakes += sample[i]
        num_copy.append(copy)
        pbar.update()
    pbar.close()
    #Think about pre-initializing the right sized array, this impacts how everything after is done (optimize)
    return num_copy, mistakes


def amplifyMistakes(ow_mistakes):
    return np.count_nonzero(samplePCREfficiency(ow_mistakes))


def samplePCREfficiency(poolSize):
    return np.random.choice([0,1], poolSize, p = [1 - PCR_EFFICIENCY, PCR_EFFICIENCY])


def samplePCRError(len_oligo, numOligo):
    return np.random.binomial(len_oligo, PCR_ERROR_RATE, numOligo)


def amplify(num_pool, num_cycles, ow_mistakes, len_oligo):

    pbar = tqdm(total= num_cycles, desc= "PCR cycles finished")
    for cycle in xrange(num_cycles):
        ow_mistakes += amplifyMistakes(ow_mistakes)
        for i, numOligo in enumerate(num_pool):
            if num == 0:
                continue
            #1 for replicated, 0 for not
            pcr_eff = samplePCREfficiency(numOligo)
            #1 for mistake, 0 for not
            pcr_error = samplePCRError(len_oligo, numOligo)
            new_numOligo = 0
            amp_mistakes = 0
            for j in xrange(numOligo):
                #Redo this section without efficiency
                if pcr_eff[j] == 0 or pcr_error[j] != 0:       #It wasn't replicated, or there is a mistake
                    new_numOligo += 1
                    if pcr_eff[j] != 0:                      #It was replicated, and there was a mistake
                        amp_mistakes += 1
            num_pool[i] = 2 * numOligo - new_numOligo
            ow_mistakes += amp_mistakes
        pbar.update()
    pbar.close()

    return ow_mistakes


def sequence(pool, ow_mistakes, avg_cov, len_oligo, num_pool):
    #pool and num_pool should have the same length
    len_pool = len(pool)
    stop = int(len_pool * avg_cov)
    seq_mistakes = 0
    totOligoInPool = np.sum(num_pool)

    print "Number of mistakes: " + str(ow_mistakes)                     #Is this necessary
    print "Number of correct oligos: " + str(totOligoInPool)           #Is this necessary

    sequence_data = [None] * stop

    #Randomly sequencing, and sampling squence error rate
    picked = np.random.choice(a= ow_mistakes + totOligoInPool, size= stop, replace= False)
    seq_error = np.random.binomial(len_oligo, SEQ_ERROR_RATE, stop)
    picked = np.sort(picked)

    pbar = tqdm(total= picked.size, desc= "Sequenced oligos")

    for i, seq in enumerate(picked):
        if seq_error[i] != 0:
            seq_mistakes += 1
            continue
        if seq > totOligoInPool:
            seq_mistakes += len(picked[i:])
            break
        while seq > upperBound:
            poolIndex += 1
            upperBound += num_pool[poolIndex]
        sequence_data[i] = pool[poolIndex]
        pbar.update()
    pbar.close()

    print "Percent: " + str(float(stop) / totOligoInPool + ow_mistakes))

    return sequence_data, seq_mistakes



def main():
    #Get commandline arguments and parse input
    args = read_args()
    oligo_list, len_oligo, pool_size = read_oligo_list(args.file_in)

    #Calculate sequencing coverage of the oligo pool
    sample = negbin_cov(args.avg_cov, args.size_para, pool_size)
    dropout = sample.size - np.count_nonzero(sample)
    print "{0:.2f}".format(dropout * 100/ float(pool_size)) + "% dropout"

    num_copy, mistakes = synthesize(len_oligo, sample, args.copies)

    mistakes = amplify(num_copy, args.pcr_cycles, mistakes, len_oligo)

    sequence_data, seq_mistakes = sequence(oligo_list, mistakes, args.avg_cov, len_oligo, num_copy)

    write_data(args.output, sequence_data, seq_mistakes)

main()
