
# coding: utf-8

# In[12]:


import csv
import smtplib
import sys
sys.path.append("..")
from config import *
from utils import group_IP
from email.mime.text import MIMEText


# In[13]:


SUBJECT = "COL362/632 Project 1 credentials"


# In[24]:


def setup_connection(sender):
    """
    Establish connection with the smtp server
    """
    smtp = smtplib.SMTP(SMTP_SERVER)
    user = sender["uname"]
    password = sender["pswd"]
    smtp.connect("smtp.iitd.ernet.in")
    smtp.starttls()
    smtp.login(user, password)
    return smtp


# In[25]:


def kerberosId(entryNO): # 2019MCS2574  mcs192574
    kid = entryNO[4:7] + entryNO[2:4] +entryNO[7:]
    return kid.lower()


# In[26]:


if __name__=="__main__":
    conn = setup_connection(SENDER)
    print("Connection established...")
    with open(RECIPIENTS_FILE) as recepients_file:
        reader = csv.reader(recepients_file)
        next(reader)
        for row in reader:
            # print(row)
            group = row[0].strip().lower()
            names = [each.strip() for each in row[1 : -1 : 2] if each.strip()]
            entry_numbers = [each.strip() for each in row[2 : -1 : 2] if each.strip()]
            if group not in CREDENTIALS:
                print("Credentials for {} does not exists".format(group))
            else:
                # to email each  group
                to_list = [kerberosId(en) + MAIL_SERVER for en in entry_numbers]
                
                host = group_IP(group)
                portal_url = host +":5000"
                body = EMAIL_TEMPLATE.format(
                    uname = group,
                    pswd = CREDENTIALS[group],
                    members = ", ".join(names),
                    url = portal_url,
                    host = host
                )
                msg = MIMEText(body)
                msg['Subject'] = SUBJECT
                msg['From'] = SENDER['email']
                msg['To'] = ", ".join(to_list)
                print("Sending credentials to {}".format(msg['To']))
                print(msg.as_string())
                # break
                # conn.sendmail(SENDER['email'], to_list, msg.as_string())
                
                
                

