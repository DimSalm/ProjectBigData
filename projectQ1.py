import pandas as pd
import numpy as np
from scipy import stats

#Q1 read-shape-info and do we nned info from read me file as comments?edw mporoume na to grapsoume kalitera
books = pd.read_csv('BX-Books_clean.csv',delimiter=';',encoding='Latin-1',dtype={3:'object'})
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')
print('books rows,columns and info: ',books.shape)
print(books.info(memory_usage='deep'))
print('book ratings rows,columns and info: ',ratings.shape)
print(ratings.info(memory_usage='deep'))
print('users rows,columns and info: ',users.shape)
print(users.info(memory_usage='deep'))

br = pd.merge(books,ratings,how='outer')
bru = pd.merge(br,users,how='outer')
print(bru.info())

#book popularity = what book have most ratings (means people have read it)
bookpop = bru.groupby(['ISBN'])[['Book-Rating']].count()
print(bookpop.sort_values(['Book-Rating'],ascending=False))

#author popularity = group all the books of an author and count how many have read all of them
authorpop = bru.groupby(['Book-Author'])[['Book-Rating']].count()
print(authorpop.sort_values(['Book-Rating'],ascending=False))

#How many books each age group have read
agegroups = pd.cut(bru['Age'], bins=[0, 20, 40, 60, 80, np.inf])
ageranges = bru.groupby(agegroups)[['ISBN']].count()
print(ageranges.sort_values(['ISBN'],ascending=False))

#Book Outlier detection
booksread = bru['ISBN'].value_counts()
bookoutliers=booksread[((booksread-booksread.mean()).abs() > 4*booksread.std())]
print('\n',bookoutliers)

#Author pop outlier detection
authorbook = bru['Book-Author'].value_counts()
authoroutliers=authorbook[((authorbook-authorbook.mean()).abs() > 4*authorbook.std())]
print(authoroutliers)

#User outlier detection
userread = bru.groupby('User-ID')['ISBN'].count()
useroutliers=userread[((userread-userread.mean()).abs() > 4*userread.std())]
print(useroutliers.sort_values(ascending=False))