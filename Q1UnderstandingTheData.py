import pandas as pd
import numpy as np
import warnings

books = pd.read_csv('BX-Books.csv',delimiter=';',encoding='Latin-1',quotechar='"',escapechar='\\')
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')

print(books.info(memory_usage='deep'))
print('books rows,columns and info: ',books.shape)
print(ratings.info(memory_usage='deep'))
print('book ratings rows,columns and info: ',ratings.shape)
print(users.info(memory_usage='deep'))
print('users rows,columns and info: ',users.shape)

#clean books:year of puplication
booksclean1 = books[books['Year-Of-Publication']<=2020]

#clean books:drop columns with urls
booksclean2 = booksclean1.drop(['Image-URL-S','Image-URL-M','Image-URL-L'],axis=1)

#clean books: drop isbn where not 9 digits and then X or x or digit
warnings.filterwarnings("ignore", 'This pattern has match groups')
filter1 = booksclean2['ISBN'].str.contains("(\d{9}(\d|X|x))")
booksclean3 = booksclean2[filter1]
print(booksclean3)

#clean ratings: isbn not valid in ratings
filter2 = ratings['ISBN'].str.contains("(\d{9}(\d|X|x))")
ratingsclean1 = ratings[filter2]
print(ratingsclean1)

#clean users: drop age where age>100?
usersclean1 = users[~(users['Age']>90)]
usersclean2 = usersclean1[~(usersclean1['Age']<15)]
print(usersclean2)

#keep only the commons
ratings_clean1 = ratingsclean1[ratingsclean1['ISBN'].isin(booksclean3['ISBN'])]
users_clean = usersclean2[usersclean2['User-ID'].isin(ratings_clean1['User-ID'])]
print(users_clean)

ratings_clean = ratings_clean1[ratings_clean1['User-ID'].isin(users_clean['User-ID'])]
print(ratings_clean)

books_clean = booksclean3[booksclean3['ISBN'].isin(ratings_clean['ISBN'])]
print(books_clean)

#book popularity = what book have most ratings (means people have read it)
bookpop = ratings_clean.groupby(['ISBN'])[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
print(bookpop)

#author popularity = group all the books of an author and count how many have read all of them
bru1 = pd.merge(books_clean,ratings_clean)
authorpop = bru1.groupby(['Book-Author'])[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
print(authorpop)

#How many books each age group have read
bru2 = pd.merge(users_clean,ratings_clean)
agegroups = pd.cut(bru2['Age'], bins=[14, 20, 40, 60, 80,90])
ageranges = bru2.groupby(agegroups)[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
print(ageranges)

#rating Outlier detection where rating=0 and where number of times the book was read is 1
booksread = ratings_clean[~(ratings_clean['Book-Rating']==0)]
print(booksread)
booksread2=booksread.groupby(['ISBN']).count()
booksread2_clean=booksread[booksread2['Book-Rating']>1]
print(booksread2_clean)
poutsaki=booksread.merge(booksread2_clean,left_on=['ISBN'],right_on='ISBN',how='right')
print(poutsaki)


#book pop outlier detection based on author
#authorread = books_clean[books_clean['Book-Author'].isin(authorpop['Book-Author']==1)]
#print(authorread)




















#users.to_csv(r'C:\Users\dimsa\Desktop\ProjectBigData\poutsa.csv',index=False,na_rep='NULL')