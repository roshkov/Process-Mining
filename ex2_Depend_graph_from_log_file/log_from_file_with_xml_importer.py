import re
import xml.etree.ElementTree as ET
import datetime


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
            

 
   
log = read_from_file('extension-log.xes')
dg = dependency_graph_file(log)


# print (log)

# general statistics: for each case id the number of events contained
for case_id in sorted(log):
    print((case_id, len(log[case_id])))

# details for a specific event of one case
case_id = "case_123"
event_no = 0
print((log[case_id][event_no]["concept:name"], log[case_id][event_no]["org:resource"], log[case_id][event_no]["time:timestamp"],  log[case_id][event_no]["cost"]))




