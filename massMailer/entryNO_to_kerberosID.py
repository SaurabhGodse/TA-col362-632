
# coding: utf-8

# In[15]:


import csv


# In[18]:


def kerberosId(entryNO): # 2019MCS2574  mcs192574
    kid = entryNO[4:7] + entryNO[2:4] +entryNO[7:]
    return kid.lower()


# In[19]:


student_list = []
with open("students_details .csv") as studdetails:
    reader = csv.reader(studdetails)
    next(reader)
    for row in reader:
        student_list.append(row[5].split("@")[0])

with open("recipients.csv") as grpinfo:
    reader =csv.reader(grpinfo)
    
    #skip the header of csv 
    next(reader)
    
    for row in reader:
        mailids = ""
        for eno in (row[2], row[4], row[6]):
            if not eno:
                continue
            else:
                mailid = kerberosId(eno)
                # to detect any invlaid EntryNumber 
                if mailid not in student_list:
                    print("wrong entry number : ", eno)
                else:
                    continue
                    
            
    
    
    

