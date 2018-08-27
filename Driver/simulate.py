import argparse
from synthesis import synthesize, set_mutation_rate
from PCR import amplify, set_error_rate 
from negbin import sequence, prepare_list 
import sys

HEADER = 'packet'

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="File with oligos to synthesize", required=True)
    parser.add_argument("--pcr_cycles", help="Number of PCR cycles", default = 10, type = int)
    parser.add_argument("--worst_case", help="Use the highest error rates", default = False, action="store_true")
    parser.add_argument("--no_synth", help= "Use ACGT nucleotides only", default = False, action="store_true")
    parser.add_argument("--avg_cov", help="Average oligo coverage when sequencing", default = 10, type= int) 
    parser.add_argument("--size_para", help="Size parameter for sequencing coverage", default = 2, type= int) 
    parser.add_argument("--errorN", help= "Every error replaces the nucleotide with N", default = False, action="store_true")
    parser.add_argument("--copies", help= "Number of copies of oligos to synthesize", default = 1, type = int)
    parser.add_argument("--output", help="File with sequenced oligos", required=True)
    args = parser.parse_args()

    return(args)

def read_oligo_list(file_name):
    
    try:
        f = open(file_name, 'r')
    except:
        logging.error("%s file not found", file_name)
        sys.exit(0)

    oligo_list = []
    count = 0

    for oligo in f:

        if HEADER in oligo:     #Reading the header for the oligo, so skip
            continue

        oligo_list.append(oligo.rstrip("\n"))
        count += 1

    f.close()

    return oligo_list, count

def write_data(output, chosen_oligos):
   
    out = open(output, 'w')

    for oligo in chosen_oligos:
        out.write(oligo + "\n")
    out.close()

def set_rates(worst_case, no_synth, errorN):
    set_mutation_rate(worst_case, no_synth, errorN)
    set_error_rate(worst_case, no_synth, errorN)

def main():

    args = read_args()
    set_rates(args.worst_case, args.no_synth, args.errorN)
    oligo_list, count = read_oligo_list(args.file_in) 

    oligo_list = prepare_list(oligo_list, args.avg_cov, args.size_para, count, args.copies)
    
    pool = synthesize(oligo_list)
    
    np_pool = amplify(pool, args.pcr_cycles)

    chosen_oligos = sequence(np_pool, count, args.avg_cov)
    
    write_data(args.output, chosen_oligos)
    
main()

    

        
        
