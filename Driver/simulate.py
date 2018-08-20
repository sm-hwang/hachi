import argparse
from synthesis import synthesize
from PCR import amplify 
from sanger import sequence, calc_stop
import sys

HEADER = 'packet'

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="File with oligos to synthesize", required=True)
    parser.add_argument("--pcr_cycles", help="Number of PCR cycles", default = 10, type = int)
    parser.add_argument("--worst_case", help="Use the highest error rates", default = False, action="store_true")
    parser.add_argument("--no_synth", help= "Use ACGT nucleotides only", default = False, action="store_true")
    parser.add_argument("--num_seq", help="Number of oligos to sequence in the PCR pool", type = int)
    parser.add_argument("--percent_seq", help="% of oligos to sequence in the PCR pool", type = float)
    parser.add_argument("--output", help="File with sequenced oligos", required=True)
    args = parser.parse_args()

    return(args)

def get_oligo_list(file_name):
    
    try:
        f = open(file_name, 'r')
    except:
        logging.error("%s file not found", file_name)
        sys.exit(0)

    oligo_list = []

    for oligo in f:

        if HEADER in oligo:     #Reading the header for the oligo, so skip
            continue

        oligo_list.append(oligo.rstrip("\n"))

    f.close()

    return oligo_list

def write_data(output, chosen_oligos):
   
    out = open(output, 'w')

    for oligo in chosen_oligos:
        out.write(oligo + "\n")
    out.close()

def set_rates(worst_case, no_synth):
    set_mutation_rate(worst_case, no_synth)
    set_error_rate(worst_case, no_synth)

def main():

    args = read_args()
    set_rates(args.worst_case, args.no_synth)
    oligo_list = get_oligo_list(args.file_in) 

    pool = synthesize(oligo_list)

    np_pool = amplify(pool, args.pcr_cycles)

    stop = calc_stop(args.num_seq, args.percent_seq, np_pool.size) 
    chosen_oligos = sequence(np_pool, stop)
    
    write_data(args.output, chosen_oligos)
    
main()

    

        
        
