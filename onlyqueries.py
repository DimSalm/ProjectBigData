import mysql.connector
import pandas as pd
import math
import numpy as np

conn = mysql.connector.connect(user='root', password='Antonis2008Root!', host='127.0.0.1', allow_local_infile=True)
cursor = conn.cursor(buffered=True)

cursor.execute("drop database if exists books")
cursor.execute("CREATE DATABASE books")
cursor.execute("USE books")


def csim(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def psim(u, v):
    return csim(u - np.mean(u), v - np.mean(v))


def calc_similarities(r, sim=csim):
    return [[sim(u1, u2) for u1 in r] for u2 in r]

def calc_neighbourhood(s, k):
    return [[x for x in np.argsort(s[i]) if x != i][len(s) - 1: len(s) - k - 2: -1] for i in range(len(s))]


def predict(userId, itemId, r, s, nb):
    rsum, ssum = 0.0, 0.0
    for n in nb[userId]:
        rsum += s[userId][n] * (r[n][itemId] - np.mean(r[n]))
        ssum += s[userId][n]
    return np.mean(r[userId]) + rsum / ssum

# mae(p, a) returns the mean average error between
# predictions p and actual ratings a
def mae(p, a):
    return sum(map(lambda x: abs(x[0] - x[1]), zip(p, a))) / len(p)


# rmse(p, a) returns the root mean square error between
# predictions p and actual ratings a
def rmse(p, a):
    return math.sqrt(sum(map(lambda x: (x[0] - x[1]) ** 2, zip(p, a))) / len(p))


# flatten(l) flattens a list of lists l
def flatten(l):
    return [x for r in l for x in r]


#df=pd.read_sql_query("SELECT * FROM bx_users",conn)
#print(df)

users = pd.read_csv('BX_Book_Ratings.csv')
#pinakas = pd.pivot_table(users,values=['Book_Rating'],index=['User_ID'],columns=['ISBN'])
#print(pinakas)
df1 = pinakas.values.tolist()
df = df1[0:9]
nNeighbours = 2
s = calc_similarities(df)
nb = calc_neighbourhood(s, nNeighbours)
pr = [[predict(u, i, df, s, nb) for i in range(len(df[u]))] for u in range(len(df))]
print('\nOriginal ratings table')
for rr in df:
    print(' '.join(['{:.4f}'.format(x) for x in rr]))

print('\nSimilarities table')
for ss in s:
    print(' '.join(['{:.4f}'.format(x) for x in ss]))

print('\nNeighbourhood table')
for ni in range(len(nb)):
    print('{:3d}: '.format(ni) + ' '.join(['{:3d}'.format(nn) for nn in nb[ni]]))

print('\nPredicted ratings table')
for rr in pr:
    print(' '.join(['{:.4f}'.format(x) for x in rr]))

print('\nMAE: {:.4f}'.format(mae(flatten(df), flatten(pr))))
print('\nRMSE: {:.4f}'.format(rmse(flatten(df), flatten(pr))))



cursor.close()
conn.close()