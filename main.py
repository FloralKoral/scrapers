import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import os
import sqlite3

# DATA
url_dafont = 'https://www.dafont.com/alpha.php?lettre={}&page={}&fpp=200'
keys = [ascii for ascii in ascii_lowercase] + ['%23']
values = [url_dafont.format(values, '1') for values in keys]

con = sqlite3.connect("data_dafont.db")
cur = con.cursor()

def getTable():
    with con:
        cur.execute("SELECT * FROM url_data")
        print(cur.fetchall())

def insertVaribleIntoTable(lettre=None, page1_url=None, page_count=None):
    try:
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO url_data
                          (lettre, page1_url, page_count) 
                          VALUES (?, ?, ?);"""

        data_tuple = (lettre, page1_url, page_count)
        cur.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)

def deleteAll():
    with con:
        cur.execute('DELETE FROM url_data;')
        print(cur.fetchall())

def initial_data_population():
    for i in range(len(keys)):
        insertVaribleIntoTable(lettre=keys[i], page1_url=values[i])
    con.commit()

def cursor_iteration(x):
    cur.execute('select * from url_data')
    for row in cur:
        print(row[x])

cursor_iteration(1)

# cur.execute("create table url_data (lettre, page1_url, page_count)")

# for i in range(len(keys)):
#     cur.execute("INSERT INTO url_data (lettre, page1_url) VALUES (?, ?)", (keys[i], values[i]))
# con.commit()

# cur.execute("insert into url_data (lettre) values ('cum')")
#
# for row in cur.execute('SELECT page1_url FROM url_data'):
#         print(row)











