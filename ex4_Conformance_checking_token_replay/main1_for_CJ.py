import re
# from petri_ext import * 
# from log_from_file_with_xml_importer import read_from_file
# from fitness import fitness_token_replay  
import itertools
import copy
import re
import xml.etree.ElementTree as ET
import datetime



class PetriNet():

    def __init__(self):
        self.PaT = {}
        #self.Transitions = []

    def add_place(self, name):
        self.PaT.update({name: {'type':'place', 'obj': Place(name)}  })

    def add_transition(self, name, id):
        self.PaT.update({id: {'type':'trans', 'obj': Transition(name, id)}  })
    
    def add_edge(self, source, target):
        
        s = self.PaT[source]
        t = self.PaT[target]
        
        
        if (s['type']=='place' and t['type']=='trans'):
            t['obj'].addInput(source)
            #print('this one')
            
        elif (s['type']=='trans' and t['type']=='place'):
            s['obj'].addOutput(target)
            #print('another one')
        return self
            
    
    def getPat(self):
        print( self.PaT)
   
    def get_tokens(self, place):
        p = self.PaT[place]
        
        if p and p['type'] == 'place':
            return p['obj'].get_tokens()


    def countAllRemainingTokens (self):
        remaining_token_counter = 0
        
        for item in self.PaT:
            if self.PaT[item]['type'] == 'place':
                remaining_token_counter += self.PaT[item]['obj'].get_tokens()
        
        # print(remaining_token_counter)
        return remaining_token_counter 


    def is_enabled(self, transition):
        inp = self.PaT[transition]['obj'].getAllInputs()
        res = True
        
        for placeId in inp:
            if self.get_tokens(placeId) == 0:
                res = False
                break
        return res
            

    def add_marking(self, place):
        self.PaT[place]['obj'].addToken()

    # id of transition is passed as parameter
    # also returns amount of inputs and outputs
    def fire_transition(self, transition):
        inp = self.PaT[transition]['obj'].getAllInputs()
        oup = self.PaT[transition]['obj'].getAllOutputs()
        
        
        for placeId in inp:
            self.PaT[placeId]['obj'].removeAllTokens()

            
        for placeId in oup:
            self.PaT[placeId]['obj'].addToken()
        
        return len(inp), len(oup)
            
            
    def transition_name_to_id(self, tr_name):
        resId = None
        for item in self.PaT:
            t = self.PaT[item]
            if ( t['type']=='trans' and t['obj'].getName() == tr_name):
                resId = t['obj'].getId()
                break
        return resId
    
    
    # Checks the amount of tokens in each input of a given transition
    # Basically, to fire a transition, all inputs (aka places) must have 1 token each
    # This function checks that and if any input (aka place) does not have a token
    # then it adds the token. As well, this function returns the amount of tokens
    # that were added 'artificially'
    def checkTokenBalanceOfTransitionInputs(self, transition):
        
        inp = self.PaT[transition]['obj'].getAllInputs()
        added_tokens_counter = 0
        
        for i in inp:
            
            #if input (place) has no tokens, then adding one
            if (self.PaT[i]['obj'].get_tokens() == 0):
                self.PaT[i]['obj'].addToken()
                added_tokens_counter+=1
            
            
        
        return added_tokens_counter
        
    
    def removeTokenFromOutput(self, transition):
        oup = self.PaT[transition]['obj'].getAllOutputs()
        for o in oup:
            self.PaT[o]['obj'].removeAllTokens()
        
    
                
        
        
            



class Place:
    def __init__ (self, id):
        self.tokens = 0
        self.id = id
        
    def get_tokens (self): 
        return self.tokens
    
    def addToken (self):
        self.tokens += 1 
        
    def removeAllTokens (self):
        self.tokens= 0
        
    def getId (self):
        return self.id
    
    
class Transition:
     def __init__ (self, name, id):
        self.name = name
        self.id = id
        self.Inputs = []
        self.Outputs = []
          
     def addInput (self, idOfInputPlace):
        self.Inputs.append(idOfInputPlace)
    
     def addOutput (self, idOfOutputPlace):
        self.Outputs.append(idOfOutputPlace)
        
     def removeInput (self, idOfInputPlace):
        self.Inputs.remove(idOfInputPlace)
    
     def removeOutput (self, idOfOutputPlace):
        self.Outputs.remove(idOfOutputPlace)
    
     def getAllInputs (self):
        return self.Inputs
    
     # checks the input places and counts how many places with no tokens
     # are going into this transitions. Returns number value
     # def checkInputsWithNoTokens(self):
         
     #     for i in self.Inputs:
     #         #Inputs[] store only ids of input place
     #         i
    
     def getAllOutputs (self):
         return self.Outputs
     
     def getName (self):
         return self.name
     
     def getId (self):
         return self.id





#READ FROM FILE
def read_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    ns = {'xes': 'http://www.xes-standard.org/'}
   
    log = dict()
    for trace in root.findall('xes:trace',ns):
        caseid = trace.find('xes:string[@key="concept:name"]', ns).attrib['value']
        log[caseid] = []
        for event in trace.findall('xes:event', ns):
            e=dict()
            #collect all attributes and properly cast them to Python type
            for attribute in event.findall('xes:string', ns):
                e[attribute.attrib['key']] = attribute.attrib['value']
                
            for attribute in event.findall('xes:int', ns):
                e[attribute.attrib['key']] = int(attribute.attrib['value'])
           
            for attribute in event.findall('xes:boolean', ns):
                e[attribute.attrib['key']] = attribute.attrib['value']=='true'
           
            for attribute in event.findall('xes:date', ns):
                if attribute.attrib['key'] == 'time:timestamp':
                    timestamp = attribute.attrib['value']
                    timestamp = datetime.datetime.strptime(timestamp[:-6], '%Y-%m-%dT%H:%M:%S')
                    e[attribute.attrib['key']] = timestamp
                    
            log[caseid].append(e)
    return log
            

    
def dependency_graph_file(log):
    F = dict()
    for caseid in log:
        for i in range (0, len(log[caseid]) -1):
            ai = log[caseid][i]["concept:name"]
            aj = log[caseid][i+1]["concept:name"]
            
            if ai not in F:
                F[ai] = dict()
            
            if aj not in F[ai]:
                F[ai][aj] = 0
            
            F[ai][aj] +=1
    
    return F

#FITNESS
def fitness_token_replay (log, mined_model):

    # counters of tokens. Will be used at the end for fitness metric formula
    # nb: these are coutners are sums of corresponding measures from all traces!
    produced = 0
    consumed = 0
    missing = 0
    remaining = 0

    test_count = 0

    #moving trough cases (aka traces) in a log    
    for caseid in log:
        test_count +=1
         
        pn = copy.deepcopy(mined_model)     #Copy of petri net passed. Needs to be created for each replay
        

        #trace steps e.g 'a' in <a,b,c,d>
        for i in range (0, len(log[caseid])):
            event = log[caseid][i]
            
            # print("e: ",event)
            
            #fire transition and updated token counters
            fire_counter = fire_transition_action(pn, event)
            missing += fire_counter[0]
            consumed += fire_counter[1]
            produced += fire_counter[2]  
            

        remaining += pn.countAllRemainingTokens()

        # <END OF TRACE>
        
    
    # with this we substract all 'end' tokens that were there and we counted them as missing
    remaining -= test_count
    
    
    #after went through all cases, counting fitness based on formula
    # one = 0.5 * (1 - missing/consumed)
    # two = 0.5 * (1 - remaining/produced)
    
    # print ('test_count ', test_count)
    # print('p: ',produced, ' | c: ',consumed, ' | m: ',missing, ', | r: ',remaining)
    fitness_m = 0.5 * (1 - missing/consumed) + 0.5 * (1 - remaining/produced)
    
    return fitness_m


def fire_transition_action(pn, event):
    
            # get Id of transition
            tr_id = pn.transition_name_to_id(event['concept:name'])
            
            # local counter of missing tokens
            # checkTokenBalanceOfTransitionInputs - makes sure all inputs have tokens, such that fire_transition is valid
            l_missing = pn.checkTokenBalanceOfTransitionInputs(tr_id)
            
            # fire transition
            inp_oup_count = pn.fire_transition(tr_id)
            
            # inp_oup_count == amount of tokens consumed[0] and produced[1]
            return l_missing, inp_oup_count[0], inp_oup_count[1]






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

# def check_enabled(pn):
#   ts = ["record issue", "inspection", "intervention authorization", "action not required", "work mandate", "no concession", "work completion", "issue completion"]
#   for t in ts:
#     print (pn.is_enabled(pn.transition_name_to_id(t)))
#   print("")


# trace = ["record issue", "inspection", "intervention authorization", "work mandate", "work completion", "issue completion"]
# for a in trace:
#   check_enabled(mined_model)
#   mined_model.fire_transition(mined_model.transition_name_to_id(a))

    
    



    