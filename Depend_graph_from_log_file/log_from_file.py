import re
import pm4py
import datetime


def read_from_file(filename):
    event_log = pm4py.read_xes(filename)
    dc = {}
    for case in event_log: #add the case
        dc[case.attributes['concept:name']] = case  #add all events of the case to the caseID
    return dc
 
     
def __eq__ (curr, prev):
    if not prev == None:
        return curr.__dict__ == prev.__dict__
    else:
        return False
    
def dependency_graph_file(log):
    df = {}
    prev = None
    curr = None
    m = 0
    
    for i in log:
        prev = None
        curr = None
        
        for j in log[i]:    
            curr = j
             
            #sets dict with all tasks existing e.g ['Task_A' :{}, 'Task_B': {}, ..]
            if(not j in df.keys()):
                df[j] = {}
            
            #Notes relation between curr<->prev task e.g case has taskA,taskB,
            #then df['Task_A']['Task_B'] +=1
            if prev is not None:
                if (not curr in df[prev]):
                    df[prev][curr] = 1
                else:
                    df[prev][curr] += 1       
            prev = j
                   
    return df

 
   
log = read_from_file('extension-log.xes')
dg = dependency_graph_file(log)


    
#Test

# general statistics: for each case id the number of events contained
for case_id in sorted(log):
    print((case_id, len(log[case_id])))

# details for a specific event of one case
case_id = "case_123"
event_no = 0
print((log[case_id][event_no]["concept:name"], log[case_id][event_no]["org:resource"], log[case_id][event_no]["time:timestamp"],  log[case_id][event_no]["cost"]))




