import mysql.connector
import pandas as pd
import math
import numpy as np
import csv
import json
from numpyencoder import NumpyEncoder

conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', allow_local_infile=True)
cursor = conn.cursor(buffered=True)
cursor.execute("drop database if exists books")
cursor.execute("CREATE DATABASE books")
cursor.execute("USE books")
cursor.execute("CREATE TABLE BX_Books (ISBN varchar(13) NOT NULL PRIMARY KEY,Book_Title varchar(255) default NULL,Book_Author varchar(255) default NULL,Year_Of_Publication int(10) default NULL,Publisher varchar(255) default NULL)")
cursor.execute("CREATE TABLE BX_Users (User_ID int(11) NOT NULL PRIMARY KEY default '0',Location varchar(250) default NULL,Age int(11) default NULL)")
cursor.execute("CREATE TABLE BX_Book_Ratings (User_ID int(11) NOT NULL default '0',ISBN varchar(13) NOT NULL,Book_Rating int(11) NOT NULL default '0',FOREIGN KEY (ISBN) REFERENCES BX_Books(ISBN),FOREIGN KEY (User_ID) REFERENCES BX_Users(User_ID),PRIMARY KEY (User_ID,ISBN))")
cursor.execute("CREATE TABLE user_neighbors (Userid int(11) NOT NULL PRIMARY KEY,neighbor1 INT(11) NOT NULL,neighbor2 INT(11) NOT NULL)")
cursor.execute("CREATE TABLE user_pairs (User_1 int(11) NOT NULL,User_2 INT(11) NOT NULL,Similarity FLOAT(8,7) default NULL,PRIMARY KEY(User_1,User_2))")

cursor.execute("""
load data local infile 'BX_Users.csv' 
into table BX_Users 
fields terminated by ',' OPTIONALLY ENCLOSED BY '"'
lines terminated by '\r\n' 
ignore 1 lines;
""")
cursor.execute("""
load data local infile  'BX_Books.csv'
into table BX_Books 
fields terminated by ',' OPTIONALLY ENCLOSED BY '"' 
lines terminated by '\r\n' 
ignore 1 lines;
""")
cursor.execute("""
load data local infile 'BX_Book_Ratings.csv' 
into table BX_Book_Ratings 
fields terminated by ',' 
lines terminated by '\r\n' 
ignore 1 lines;
""")

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

def mae(p, a):
    return sum(map(lambda x: abs(x[0] - x[1]), zip(p, a))) / len(p)

def rmse(p, a):
    return math.sqrt(sum(map(lambda x: (x[0] - x[1]) ** 2, zip(p, a))) / len(p))

def flatten(l):
    return [x for r in l for x in r]

#pivot the dataframe and make a list of lists
ratings = pd.read_csv('BX_Book_Ratings.csv')
users = pd.read_csv('BX_Users.csv')
ageuntil35=users[users['Age'] <= 35]
agefrom36=users[users['Age'] > 35]
agenan = users[users['Age'].isna()]
ratingsuntil35 = ratings[ratings['User_ID'].isin(ageuntil35['User_ID'])]
ratingsfrom36 = ratings[ratings['User_ID'].isin(agefrom36['User_ID'])]
ratingsnan = ratings[ratings['User_ID'].isin(agenan['User_ID'])]

pivot0 = pd.pivot_table(ratingsuntil35,values=['Book_Rating'],index=['User_ID'],columns=['ISBN']).fillna(0,inplace=True)
pivot1 = pd.pivot_table(ratingsfrom36,values=['Book_Rating'],index=['User_ID'],columns=['ISBN']).fillna(0,inplace=True)
pivot2 = pd.pivot_table(ratingsnan,values=['Book_Rating'],index=['User_ID'],columns=['ISBN']).fillna(0,inplace=True)

list = [pivot0,pivot1,pivot2]
count = 0
nNeighbours = 3

for i in list:
    x = i.values.tolist()
    s = calc_similarities(x)
    y = pd.DataFrame(s, index = i.index ,columns=i.index)
    for user1 in y.index.tolist():
        for user2 in y.columns.tolist():
            if y.loc[user1][user2] !=0 and user1 != user2 :
                with open('C:/Users/dimsa/Desktop/ProjectBigData/user_pairs_books'+str(count)+'.csv','a') as csv1:
                    data= [user1,user2,y.loc[user1][user2]]
                    writer= csv.writer(csv1)
                    writer.writerow(data)
    nb = calc_neighbourhood(s, nNeighbours)
    dict = {}
    dictcount = -1
    users = i.index.tolist()
    for user in users:
        dictcount += 1
        values = []
        for neighbour in nb[dictcount]:
            values.append(users[neighbour])
        dict[user]= values
    with open('C:/Users/dimsa/Desktop/ProjectBigData/neighbors-k-books'+str(count)+'.data','w') as jsonfiles :
        json.dump(dict, jsonfiles,cls=NumpyEncoder)
    pr = [[predict(u, i, x, s, nb) for i in range(len(x[u]))] for u in range(len(x))]
    print(pr)
    print('\nMAE: ',mae(flatten(pr), flatten(x)))
    print('\nRMSE: ',rmse(flatten(pr), flatten(x)))
    count += 1

cursor.execute("""
load data local infile 'C:/Users/dimsa/Desktop/ProjectBigData/user_pairs_books0.csv' 
into table user_pairs 
fields terminated by ',' OPTIONALLY ENCLOSED BY '"'
lines terminated by '\r\n' 
ignore 0 lines;
""")
cursor.execute("""
load data local infile 'C:/Users/dimsa/Desktop/ProjectBigData/user_pairs_books1.csv' 
into table user_pairs 
fields terminated by ',' OPTIONALLY ENCLOSED BY '"'
lines terminated by '\r\n' 
ignore 0 lines;
""")
cursor.execute("""
load data local infile 'C:/Users/dimsa/Desktop/ProjectBigData/user_pairs_books2.csv' 
into table user_pairs 
fields terminated by ',' OPTIONALLY ENCLOSED BY '"'
lines terminated by '\r\n' 
ignore 0 lines;
""")

conn.commit()
cursor.close()
conn.close()