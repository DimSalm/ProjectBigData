import pandas as pd
import numpy as np
import csv

books = pd.read_csv('BX-Books_clean.csv',delimiter=';',encoding='Latin-1',dtype={3:'object'})
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')
print('books rows,columns and info: ',books.shape)
print(books.info(memory_usage='deep'))
print('book ratings rows,columns and info: ',ratings.shape)
print(ratings.info(memory_usage='deep'))
print('users rows,columns and info: ',users.shape)
print(users.info(memory_usage='deep'))
