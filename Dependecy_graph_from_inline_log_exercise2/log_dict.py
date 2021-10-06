import csv
import re
 
f = """
Task_A;case_1;user_1;2019-09-09 17:36:47
Task_B;case_1;user_3;2019-09-11 09:11:13
Task_D;case_1;user_6;2019-09-12 10:00:12
Task_E;case_1;user_7;2019-09-12 18:21:32
Task_F;case_1;user_8;2019-09-13 13:27:41

Task_A;case_2;user_2;2019-09-14 08:56:09
Task_B;case_2;user_3;2019-09-14 09:36:02
Task_D;case_2;user_5;2019-09-15 10:16:40

Task_G;case_1;user_6;2019-09-18 19:14:14
Task_G;case_2;user_6;2019-09-19 15:39:15
Task_H;case_1;user_2;2019-09-19 16:48:16
Task_E;case_2;user_7;2019-09-20 14:39:45
Task_F;case_2;user_8;2019-09-22 09:16:16

Task_A;case_3;user_2;2019-09-25 08:39:24
Task_H;case_2;user_1;2019-09-26 12:19:46
Task_B;case_3;user_4;2019-09-29 10:56:14
Task_C;case_3;user_1;2019-09-30 15:41:22"""

#read tje data
lines = f.splitlines()
reader = csv.reader(lines, delimiter=';')
parsed_csv = list(reader)


#makes a proper structure of given data
def log_as_dictionary(log):
    event_dict = {}
    dict1, dict2, dict3 = [], [], []
    
    for row in parsed_csv:
        if row:
           if row[1] == 'case_1':
               dict1.append(row)
           elif row[1] == 'case_2':
               dict2.append(row)
           elif row[1] == 'case_3':
               dict3.append(row) 
        
    event_dict['case_1'] = dict1
    event_dict['case_2'] = dict2
    event_dict['case_3'] = dict3
    return event_dict



def dependency_graph(log):
    df = {}
    prev = None
    curr = None
    
    for i in log:
        prev = None
        curr = None
        
        for j in log[i]:     
            curr = j[0]
            # print ('curr', curr, '  prev', prev)
             
            #sets dict with all tasks existing e.g ['Task_A' :{}, 'Task_B': {}, ..]
            if(not j[0] in df.keys()):
                df[j[0]] = {}
            
            #Notes relation between curr<->prev task e.g case has taskA,taskB,
            #then df['Task_A']['Task_B'] +=1
            if prev is not None:
                if (not curr in df[prev]):
                    df[prev][curr] = 1
                else:
                    df[prev][curr] += 1       
            prev = j[0]
                   
    return df




log = log_as_dictionary(f)
dg = dependency_graph(log)

 
# print final data   
for ai in sorted(dg.keys()):
    for aj in sorted(dg[ai].keys()):
        print (ai, '->', aj, ':', dg[ai][aj])









