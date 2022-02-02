import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import os
import sqlite3
from sqlite3 import Error


# DATA
url_dafont = 'https://www.dafont.com/alpha.php?lettre={}&page={}&fpp=200'
keys = [ascii for ascii in ascii_lowercase] + ['%23']
values = [url_dafont.format(values, '1') for values in keys]


class sql_shit:

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None

        try:
            self.conn = sqlite3.connect(db_file)
            print("Successfully connected to the database.")
        except Error as e:
            print("Failed to connect to database",e)

        return self.conn

    def getTable(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM url_data")
            print(cur.fetchall())
        except Error as e:
            print("\nERROR:", e, "\nCheck database name.")

    def deleteAll(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM url_data;')
        print(cur.fetchall())

    def insertVaribleIntoTable(self, lettre=None, page1_url=None, page_count=None):
        try:
            sqlite_insert_with_param = """INSERT INTO url_data
                              (lettre, page1_url, page_count) 
                              VALUES (?, ?, ?);"""

            data_tuple = (lettre, page1_url, page_count)
            cur = self.conn.cursor()
            cur.execute(sqlite_insert_with_param, data_tuple)
            # self.conn.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")

        except Error as e:
            print("Failed to insert Python variable into sqlite table", e)

    def initial_data_population(self):
        #create the initial data table with page letters and page 1 urls
        for i in range(len(keys)):
            self.insertVaribleIntoTable(lettre=keys[i], page1_url=values[i])
        self.conn.commit()

    def update_page_count_test(self):
        try:
            cur = self.conn.cursor()
            sql_update_query = """update url_data set page_count = 23 where lettre = 'b'"""
            cur.execute(sql_update_query)
            self.conn.commit()
            print("Record Updated successfully ")
            cur.close()

        except Error as e:
            print("Failed to update table", e)


    def cursor_iteration(self, x):
        cur = self.conn.cursor()
        cur.execute('select * from url_data')
        for row in cur:
            print(row[x])



def main():
    database = "data_dafont.db"
    run = sql_shit()
    run.create_connection(database)
    # run.deleteAll()
    run.updatepagecount()

    # run.initial_data_population()
    # run.updateTable(database)
    # run.create_connection(database)

    run.getTable()


if __name__ == '__main__':
    main()


#

# cur.execute("create table url_data (lettre, page1_url, page_count)")

# for i in range(len(keys)):
#     cur.execute("INSERT INTO url_data (lettre, page1_url) VALUES (?, ?)", (keys[i], values[i]))
# con.commit()

# cur.execute("insert into url_data (lettre) values ('cum')")
#
# for row in cur.execute('SELECT page1_url FROM url_data'):
#         print(row)











