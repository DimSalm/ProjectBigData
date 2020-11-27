import pandas as pd
import numpy as np
import warnings

books = pd.read_csv('BX-Books.csv',delimiter=';',encoding='Latin-1',quotechar='"',escapechar='\\')
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')

print(books.info(memory_usage='deep'))
print(ratings.info(memory_usage='deep'))
print(users.info(memory_usage='deep'))

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
users_clean = usersclean2[usersclean2['User-ID'].isin(ratingsclean1['User-ID'])]
print(users_clean)

ratings_clean = ratings_clean1[ratings_clean1['User-ID'].isin(users_clean['User-ID'])]
print(ratings_clean)

books_clean = booksclean3[booksclean3['ISBN'].isin(ratings_clean['ISBN'])]
print(books_clean)

#print(usersclean1.isna().sum())
#print(usersclean2.groupby('Age')['Age'].value_counts())





























#users.to_csv(r'C:\Users\dimsa\Desktop\ProjectBigData\poutsa.csv',index=False,na_rep='NULL')