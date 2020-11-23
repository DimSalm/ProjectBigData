import pandas as pd
import numpy as np
import csv

books = pd.read_csv('BX-Books_clean.csv',delimiter=';',encoding='Latin-1',dtype={3:'string'})
ratings = pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='Latin-1')
users = pd.read_csv('BX-Users.csv',delimiter=';',encoding='Latin-1')
print(books.head())
print(ratings.head())
print(users.head())