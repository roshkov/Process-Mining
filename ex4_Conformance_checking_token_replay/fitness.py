import itertools
import copy
    

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
        # produced += 1    # +1 to produced as we put token into 'start' place
        
        # print (caseid, ' : ',len(log[caseid])) 
        

        #trace steps e.g 'a' in <a,b,c,d>
        for i in range (0, len(log[caseid])):
            event = log[caseid][i]
            
            # print("e: ",event)
            
            #fire transition and updated token counters
            fire_counter = fire_transition_action(pn, event)
            missing += fire_counter[0]
            consumed += fire_counter[1]
            produced += fire_counter[2]  
            
            # if (i == len(log[caseid])-1):
            #       tr_id = pn.transition_name_to_id(event['concept:name'])
            #       pn.removeTokenFromOutput(tr_id)
                 
        
        # print('\n\n')
        # consumed += 1   # +1 to consumed as we consume token from 'end' place as we reached it
        remaining += pn.countAllRemainingTokens()
        
        # print('r: ', remaining)
        # <END OF TRACE>
        
    
    # with this we substract all 'end' tokens that were there and we counted them as missing
    remaining -= test_count
    
    
    #after went through all cases, counting fitness based on formula
    one = 0.5 * (1 - missing/consumed)
    two = 0.5 * (1 - remaining/produced)
    
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


