import mysql.connector
import pandas as pd
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', allow_local_infile=True)
cursor = conn.cursor(buffered=True)
cursor.execute("drop database if exists books")
cursor.execute("CREATE DATABASE books")
cursor.execute("USE books")
cursor.execute("CREATE TABLE BX_Books (ISBN varchar(13) NOT NULL PRIMARY KEY,Book_Title varchar(255) default NULL,Book_Author varchar(255) default NULL,Year_Of_Publication int(10) default NULL,Publisher varchar(255) default NULL)")
cursor.execute("CREATE TABLE BX_Users (User_ID int(11) NOT NULL PRIMARY KEY default '0',Location varchar(250) default NULL,Age int(11) default NULL)")
cursor.execute("CREATE TABLE BX_Book_Ratings (User_ID int(11) NOT NULL default '0',ISBN varchar(13) NOT NULL,Book_Rating int(11) NOT NULL default '0',FOREIGN KEY (ISBN) REFERENCES BX_Books(ISBN),FOREIGN KEY (User_ID) REFERENCES BX_Users(User_ID),PRIMARY KEY (User_ID,ISBN))")


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

df=pd.read_sql_query("SELECT * FROM bx_book_ratings",conn)
print(df)

conn.commit()
cursor.close()
conn.close()