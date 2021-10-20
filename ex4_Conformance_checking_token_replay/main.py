import re
from petri_ext import * 
from log_from_file_with_xml_importer import read_from_file
from fitness import fitness_token_replay  

def _direct_followers(log, sort=True):
    ds = []
    for case_id in log:
        for index in range(0, len(log[case_id]) -1 ):
            if (log[case_id][index]["concept:name"], log[case_id][index + 1]["concept:name"]) not in ds:
                ds.append( (log[case_id][index]["concept:name"], log[case_id][index+1]["concept:name"]))
    return ds       


# 'x' followed by 'y' but never 'y' followed by 'x'
def _causalities(seen, df):
    cs = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in cs:
                if (event, event2) in df and (event2, event) not in df:
                    cs.append((event, event2))
    return cs


#no x -> y and no y -> x
def _no_causalities(seen, df):
    cs = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in cs:
                if (event, event2) not in df and (event2, event) not in df:
                    cs.append((event, event2))
    return cs


def _parallels(seen, df):
    par = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in par:
                if (event, event2) in df and (event2, event) in df:
                    par.append((event, event2))
    return par


# takes 2 sets of elements (A,B) and list of elements cs. 
# Checks if all elements of A and B are NOT in cs
def _check_outsets(A, B, cs):
    for event in A:
        for event2 in B:
            if (event, event2) not in cs:
                return False
    return True


    
def alpha(log):
    import itertools
    import copy

    T_L = list(set([item["concept:name"] for sub in log for item in log[sub]]))     # event in a trace
    
    T_I = list(set([log[sub][0]["concept:name"] for sub in log]))      #the very first one???

    T_O = list(set([log[sub][len(log[sub]) -1]["concept:name"] for sub in log]))  #the very last one?
       

    
    direct_followers = _direct_followers(log)
    causal = _causalities(T_L, direct_followers)
    not_causal = _no_causalities(T_L, direct_followers)
    parallel = _parallels(T_L, direct_followers)
    
    

    
    xl = set()
    subsets = set()
    for i in range(1, len(T_L)):
        for s in itertools.combinations(T_L, i):
            subsets.add(s)
            

    #check if a,a not causal; b,b are not causal; a,b are causal
    for a in subsets:
        reta = _check_outsets(a, a, not_causal)
        
        for b in subsets:
            retb = _check_outsets(b, b, not_causal)
            if reta and retb and _check_outsets(a, b, causal):
                xl.add((a,b))
                
    
    yl = copy.deepcopy(xl)
    for a in xl:
        A = a[0]
        B = a[1]
        for b in xl:
            if set(A).issubset(b[0]) and set(B).issubset(b[1]):
                if a!=b:
                    yl.discard(a)
    yl = list(yl)
    
    
    pn = PetriNet()
    
    #add transitions
    for t in T_L:
        pn.add_transition(t, -(T_L.index(t) + 1 ))
        
    #add places
    pn.add_place(1001)
    pn.add_place(1002)
    
    for p in yl:
        pn.add_place(yl.index(p) + 1)
    
    #add flow
    for (src, target) in yl:
        for a in src:
            pn.add_edge(-(T_L.index(a) + 1), yl.index((src, target)) +1)
        for b in target:
            pn.add_edge(yl.index((src, target)) + 1, -(T_L.index(b) + 1))
    
    for t in T_I:
        pn.add_edge(1001, -(T_L.index(t) + 1))
    
    for t in T_O:
        pn.add_edge(-(T_L.index(t) + 1), 1002)
        
    pn.add_marking(1001)
    
    return pn
    
                    


log = read_from_file("extension-log.xes")
log_noisy = read_from_file("extension-log-noisy.xes")

mined_model = alpha(log)



print(round(fitness_token_replay(log, mined_model), 5))
print(round(fitness_token_replay(log_noisy, mined_model), 5))





    