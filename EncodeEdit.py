"""
Modified from https://github.com/TeamErlich/dna-fountain
"""


#6 Nucleotide

#utils.pyx
intab = "012345"
outtab - "ACGTPZ"

def screen_repeat_dna(dna, max_repeat, gc_dev):

    dna = dna.replace(MAX_Cs, ADD_Z)
    dna = dna.replace(MAX_Gs, ADD_P) 
    if As in dna or Cs in dna or Gs in dna or Ts in dna: 
        return 0
    
    gc = dna.count("1") + dna.count("2")  
    gc = gc/(len(dna)+0.0)

    if (gc < 0.5 - gc_dev) or (gc > 0.5 + gc_dev):
        return 0
    return 1

def prepare(max_repeat):
    #Added Ps, Zs global constants (Munsu)
    global As, Cs, Gs, Ts
    global MAX_Cs, MAX_Gs, ADD_Z, Add_P 
    As = '0' * (max_repeat+1)
    Cs = '1' * (max_repeat+1)
    Gs = '2' * (max_repeat+1)
    Ts = '3' * (max_repeat+1)
    MAX_Cs = '1' * (max_repeat)
    MAX_Gs = '2' * (max_repeat)
    ADD_Z = '1' * (max_repeat - 1) + '5'
    ADD_P = '2' * (max_repeat - 1) + '4'

#8 Nucleotide Assumption

#utils.pyx
intab = "01234567" 
outtab = "ACGTPZXY"

def int_to_eight(a):
    #a is an array of integers between 0-255.
    #returns 0112322102
    bin_data = ''.join('{0:08b}'.format(element) for element in a) #convert to a long sring of binary values
    return ''.join(str(int(bin_data[t:t+3],2)) for t in xrange(0, len(bin_data),3)) #convert binary array to a string of 0,1,2,3,4,5,6,7

def prepare(max_repeat):
    #Added Ps, Zs global constants (Munsu)
    global As, Cs, Gs, Ts, Ps, Zs, Xs, Ys
    As = '0' * (max_repeat+1)
    Cs = '1' * (max_repeat+1)
    Gs = '2' * (max_repeat+1)
    Ts = '3' * (max_repeat+1)
    Ps = '4' * (max_repeat+1)
    Zs = '5' * (max_repeat+1)
    Xs = '6' * (max_repeat+1)
    Ys = '7' * (max_repeat+1)

def screen_repeat_dna(dna, max_repeat, gc_dev):

    if As in dna or Cs in dna or Gs in dna or Ts in dna or Ps in dna or Zs in dna or Xs in dna or Ys in dna: 
        return 0
    
    #gc = dna.count("1") + dna.count("2")  
    #gc = gc/(len(dna)+0.0)

    #if (gc < 0.5 - gc_dev) or (gc > 0.5 + gc_dev):
        #return 0
    return 1
