import pandas as pd
import warnings

#read the csv as dataframes
books = pd.read_csv('BX-Books.csv',delimiter=';',encoding='Latin-1',quotechar='"',escapechar='\\')
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')

#info regarding each csv size,general information,statistics
#print(books.info(memory_usage='deep'))
#print('books rows,columns and info: ',books.shape)
#print(books['Year-Of-Publication'].describe())
#print(ratings.info(memory_usage='deep'))
#print('book ratings rows,columns and info: ',ratings.shape)
#print(ratings['Book-Rating'].describe())
#print(users.info(memory_usage='deep'))
#print('users rows,columns and info: ',users.shape)
#print(users['Age'].describe())

#clean BX-Books:year of puplication for the years bigger than 2020
booksclean1 = books[books['Year-Of-Publication']<=2020]

#clean BX-Books:drop columns with urls(no needed for the analysis)
booksclean2 = booksclean1.drop(['Image-URL-S','Image-URL-M','Image-URL-L'],axis=1)

#clean BX-Books: drop isbn where not 9 numeric digits and then X or x
warnings.filterwarnings("ignore", 'This pattern has match groups')
filter1 = booksclean2['ISBN'].str.contains("(\d{9}(\d|X|x))")
booksclean3 = booksclean2[filter1]
#print(booksclean3)

#clean BX-Book-Ratings: isbn not valid in ratings
filter2 = ratings['ISBN'].str.contains("(\d{9}(\d|X|x))")
ratingsclean1 = ratings[filter2]
#print(ratingsclean1)

#clean users: drop age where age>90 and age<15
usersclean1 = users[~(users['Age']>90)]
usersclean2 = usersclean1[~(usersclean1['Age']<15)]
#print(usersclean2)

#keep only the common values from every dataframe after the cleaning
ratings_clean1 = ratingsclean1[ratingsclean1['ISBN'].isin(booksclean3['ISBN'])]
users_clean = usersclean2[usersclean2['User-ID'].isin(ratings_clean1['User-ID'])]
#print('BX-Users clean:\n',users_clean)

ratings_clean = ratings_clean1[ratings_clean1['User-ID'].isin(users_clean['User-ID'])]
#print('BX-Book-Ratings clean:\n', ratings_clean)

books_clean = booksclean3[booksclean3['ISBN'].isin(ratings_clean['ISBN'])]
#print('BX-Books clean:\n',books_clean)

#book popularity = books ordered by "how many times has a book been read"
bookpop = ratings_clean.groupby(['ISBN'])[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
#print('Book popularity:\n', bookpop)

#author popularity = authors ordered by "how many users have read their books"
bru1 = pd.merge(books_clean,ratings_clean)
authorpop = bru1.groupby(['Book-Author'])[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
#print('Author popularity:\n', authorpop)

#How many books each age group has read
bru2 = pd.merge(users_clean,ratings_clean)
agegroups = pd.cut(bru2['Age'], bins=[14, 20, 40, 60, 80,90])
ageranges = bru2.groupby(agegroups)[['Book-Rating']].count().sort_values(['Book-Rating'],ascending=False)
#print('Books read per Age group:\n', ageranges)

#BX-Book-Rating Outlier detection where rating=0
booksread = ratings_clean[~(ratings_clean['Book-Rating']==0)]

#BX-Book-Rating outlier detection where number of times the book has read is up to 2
booksread2=booksread.groupby(['ISBN'])[['Book-Rating']].count()
booksread3=booksread2[booksread2['Book-Rating']>2].reset_index()
ratingsfinal = booksread[booksread['ISBN'].isin(booksread3['ISBN'])]
#print(ratingsfinal)

#BX-User outlier detection: take out users with 1 rating that have voted a book which has  less than 20 total ratings
x1=ratingsfinal.groupby('User-ID')[['Book-Rating']].count()
x2=ratingsfinal.groupby('ISBN')[['Book-Rating']].count()
x3= x1[x1['Book-Rating'] == 1].reset_index()
x4=x2[x2['Book-Rating']<20].reset_index()
ratingsoutliers = ratingsfinal[~(ratingsfinal['User-ID'].isin(x3['User-ID']) & ratingsfinal['ISBN'].isin(x4['ISBN']))]
#print(ratingsoutliers)

#BX-Books outlier detection: book outlier detection keep only commons from ratings outlier dataset
booksoutliers = books_clean[books_clean['ISBN'].isin(ratingsoutliers['ISBN'])]
#print(booksoutliers)

#BX-User outlier detection on ratings and then keep only commons
users1 = users_clean[users_clean['User-ID'].isin(ratingsoutliers['User-ID'])]

#BX-User outlier detection: take out users with a lot of ratings
usersread2 = ratingsoutliers.groupby('User-ID')[['Book-Rating']].count()
usersread3=usersread2[usersread2['Book-Rating'] < 2000].reset_index()
ratingsfinal= ratingsoutliers[ratingsoutliers['User-ID'].isin(usersread3['User-ID'])]

#keep only the commons after outlier detection
usersfinal = users1[users1['User-ID'].isin(ratingsfinal['User-ID'])]
booksfinal= booksoutliers[booksoutliers['ISBN'].isin(ratingsfinal['ISBN'])]
#print(booksfinal)
#print(ratingsfinal)
#print(usersfinal)

#dataframes with renamed colomnus so that sql recognize them
booksfinal=booksfinal.rename(columns={'Book-Author':'Book_Author','Book-Title':'Book_Title','Year-Of-Publication':'Year_Of_Publication'})
ratingsfinal=ratingsfinal.rename(columns={'User-ID':'User_ID','Book-Rating':'Book_Rating'})
usersfinal=usersfinal.rename(columns={'User-ID':'User_ID'})


#dataframes to csv
#booksfinal.to_csv(r'C:\Users\dimsa\Desktop\ProjectBigData\BX_Books.csv',index=False,na_rep='NULL')
#ratingsfinal.to_csv(r'C:\Users\dimsa\Desktop\ProjectBigData\BX_Book_Ratings.csv',index=False,na_rep='NULL')
#usersfinal.to_csv(r'C:\Users\dimsa\Desktop\ProjectBigData\BX_Users.csv',index=False,na_rep='NULL')