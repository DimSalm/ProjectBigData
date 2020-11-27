import pandas as pd
import numpy as np
import mysql.connector

conn = mysql.connector.connect(user='root', password='Antonis2008Root!',
       host='127.0.0.1',allow_local_infile=True)
cursor = conn.cursor(buffered=True)

cursor.execute("DROP DATABASE IF EXISTS books")
cursor.execute("CREATE DATABASE books")
cursor.execute("USE books")
cursor.execute("""
CREATE TABLE BX_Books (
  ISBN varchar(13) binary NOT NULL default '',
  Book_Title varchar(255) default NULL,
  Book_Author varchar(255) default NULL,
  Year_Of_Publication int(10) unsigned default NULL,
  Publisher varchar(255) default NULL,
  Image_URL_S varchar(255) binary default NULL,
  Image_URL_M varchar(255) binary default NULL,
  Image_URL_L varchar(255) binary default NULL,
  PRIMARY KEY  (ISBN)
)""")
cursor.execute("""
CREATE TABLE BX_Users (
  User_ID int(11) NOT NULL default '0',
  Location varchar(250) default NULL,
  Age int(11) default NULL,
  PRIMARY KEY  (User_ID)
)""")
cursor.execute("""
CREATE TABLE BX_Book_Ratings (
  User_ID int(11) NOT NULL default '0',
  ISBN varchar(13) NOT NULL default '',
  Book_Rating int(11) NOT NULL default '0',
  PRIMARY KEY  (User_ID,ISBN)
)""")
cursor.execute("""
load data local infile  'BX_Book_Ratings.csv' 
into table BX_Book_Ratings 
character set latin1
fields terminated by ';' optionally enclosed by '"' 
lines terminated by '\n' 
ignore 1 lines;
""")
cursor.execute("""
load data local infile  'BX_Users.csv' 
into table BX_Users 
character set latin1
fields terminated by ';' optionally enclosed by '"' 
lines terminated by '\n' 
ignore 1 lines;
""")
cursor.execute("""
load data local infile  'BX_Books_clean.cs  
into table BX_Books 
character set latin1
fields terminated by ';' optionally enclosed by '"' 
lines terminated by '\n' 
ignore 1 lines;
""")

df=pd.read_sql_query("SELECT * FROM bx_users",conn)
print(df)











cursor.close()
conn.close()