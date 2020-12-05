import mysql.connector
import pandas as pd
import math
import csv
import numpy as np
conn = mysql.connector.connect(user='root', password='Antonis2008Root!', host='127.0.0.1', allow_local_infile=True, database='books')
cursor = conn.cursor(buffered=True)
cursor.execute("USE books")

#df=pd.read_sql_query("SELECT * FROM bx_book_ratings",conn)
#print(df)


def csim(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def psim(u, v):
    return csim(u - np.mean(u), v - np.mean(v))


def calc_similarities(r, sim=csim):
    return [[sim(u1, u2) for u1 in r] for u2 in r]

def calc_neighbourhood(s, k):
    return [[x for x in np.argsort(s[i]) if x != i][len(s) - 1: len(s) - k - 2: -1] for i in range(len(s))]


#y = open('BX_Book_Ratings.csv', 'r', newline='\r\n')
#spamwriter = csv.reader(x)
#data = list(spamwriter)
#my_list = [[int(float(x)) for x in i] for i in csv.reader(y)]
#print(my_list)


x = pd.read_csv('BX_Book_Ratings.csv')
y=x.drop('ISBN',axis=1).values.tolist()




cursor.close()
conn.close()