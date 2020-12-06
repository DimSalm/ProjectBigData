import mysql.connector
import pandas as pd
import math
import numpy as np
conn = mysql.connector.connect(user='root', password='Antonis2008Root!', host='127.0.0.1', allow_local_infile=True, database='books')
cursor = conn.cursor(buffered=True)
cursor.execute("USE books")

def csim(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def psim(u, v):
    return csim(u - np.mean(u), v - np.mean(v))


def calc_similarities(r, sim=csim):
    return [[sim(u1, u2) for u1 in r] for u2 in r]

def calc_neighbourhood(s, k):
    return [[x for x in np.argsort(s[i]) if x != i][len(s) - 1: len(s) - k - 2: -1] for i in range(len(s))]

#df=pd.read_sql_query("SELECT * FROM bx_users",conn)
#print(df)

users = pd.read_csv('BX_Book_Ratings.csv')
pinakas = pd.pivot_table(users,values=['Book_Rating'],index=['User_ID'],columns=['ISBN'])
#print(pinakas)





cursor.close()
conn.close()