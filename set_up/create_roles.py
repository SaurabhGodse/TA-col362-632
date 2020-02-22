
# coding: utf-8

# In[4]:


import psycopg2
import sys

sys.path.append("..")
from config import SERVERS, CREDENTIALS
from utils import group_IP


# In[5]:


QUERY = """
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {user};
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {user};
REVOKE USAGE ON SCHEMA public FROM {user};
DROP USER IF EXISTS {group};
CREATE USER {user} WITH PASSWORD \'{pswd}\';
"""
QUERY1 = """
GRANT CONNECT ON DATABASE {group} TO {user};
GRANT ALL PRIVILEGES ON DATABASE {group} TO {user};
GRANT USAGE ON SCHEMA public TO {user};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user};
"""

# REVOKE CONNECT ON DATABASE {group} FROM {user};
# REVOKE USAGE ON SCHEMA public FROM {user};

# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user};
# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {user};
# GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {group};
# GRANT USAGE ON ALL TABLES IN SCHEMA public TO {group};
# DROP USER IF EXISTS {group};
# CREATE USER {user} WITH PASSWORD \'{pswd}\';
# REVOKE USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public FROM {group};
# REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM {group};
# QUERY = """
# DROP USER IF EXISTS {group};
# """


# In[6]:


def connect(ip):
    print("Connecting to %s:5432" % (ip))
    try:
        conn = psycopg2.connect(
            user = "postgres",
            host = ip,
            port = "5432",
            password = "vpl-362",
        )
        return conn
    except Exception as e:
        print(e)

        # print("Error connecting to postgres server at %s:5432" % (ip))
        return None
    
        
        


# In[ ]:


if __name__== '__main__':
    for group in CREDENTIALS.keys():
        conn = connect(group_IP(group))
        # print("Connected successfully...")
        query = QUERY.format(group=group, user = group, pswd=CREDENTIALS[group])
        # print(query)
        conn.autocommit = True
        conn.cursor().execute("DROP DATABASE IF EXISTS {};".format(group))
        conn.commit()
        conn.cursor().execute(query)
        conn.commit()
        conn.cursor().execute("CREATE DATABASE {};".format(group))
        conn.cursor().execute("REVOKE ALL PRIVILEGES ON DATABASE {} FROM public;".format(group))
        conn.commit()
        query = QUERY1.format(group=group, user = group, pswd=CREDENTIALS[group])

        conn.cursor().execute(query)
        conn.commit()
        conn.close()
        
        

