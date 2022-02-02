import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import os
import sqlite3
from sqlite3 import Error

headless = False
# DATA
url_dafont = 'https://www.dafont.com/alpha.php?lettre={}&page={}&fpp=200'
keys = [ascii for ascii in ascii_lowercase] + ['%23']
values = [url_dafont.format(values, '1') for values in keys]

# dafont - page text vars
xpath_div = "//div[@class='noindex']"
xpath_lastpage_text = ".//a[contains(@href, 'alpha.php?lettre=')]"
xpath_dl = "//a[@class='dl']"



class sqlShit(object):
    list_lastpage = []

    def createConnection(self, db_file):
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

    def initialDataPopulation(self):
        #create the initial data table with page letters and page 1 urls
        for i in range(len(keys)):
            self.insertVaribleIntoTable(lettre=keys[i], page1_url=values[i])
        self.conn.commit()

    # EXPERIMENTAL - need to add functionality to grab page count from webpage
    def update_page_count_test(self, page_count, lettre):
        try:
            cur = self.conn.cursor()
            sql_update_query = "update url_data set page_count = %s where lettre = '%s'" % (page_count, lettre)
            cur.execute(sql_update_query)
            self.conn.commit()
            print("Record Updated successfully")
            cur.close()

        except Error as e:
            print("Failed to update table", e)

    def retrieve_lettre_page1_url(self, lettre):
        cur = self.conn.cursor()
        sql_link_query = "select page1_url from url_data where lettre = '%s'" % (lettre)
        cur.execute(sql_link_query)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        return rows[0]


    def cursor_iteration(self, x):
        cur = self.conn.cursor()
        cur.execute('select * from url_data')
        for row in cur:
            print(row[x])





    def setup_browser(self, strat):  # strat = normal (complete), eager (interactive), none (undefined)
        # BROWSWER SETUP DETAILS
        # PREFERENCES - set preferences for options of browser
        prefs = {"download.default_directory": r"D:\Brushes\00_UPTAKE\00_FONTSPACE_FONTS",
                 'profile.default_content_setting_values.automatic_downloads': 1,
                 "excludeSwitches": ["test-type", "enable-automation"]
                 }

        # OPTIONS
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", prefs)
        options.headless = headless

        # SERVICE
        service = Service(r'D:\Code\Chromedriver\chromedriver.exe')

        # CAPABILITIES - set how long driver waits
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = strat  # see above choices

        self.driver = webdriver.Chrome(desired_capabilities=caps, service=service, options=options)
        self.driver.create_options()
        # self.vars = {}
        print("Browser configuration complete.\n")

    def open_page(self, lettre):
        #use letter from sql to get certain data points on it
        var = self.sqlshit.retrieve_lettre_page1_url(lettre)
        self.driver.get(var)

    def extract_lastpage(self):
        # return list of last page web elements unformatted
        return [elem for elem in self.driver.find_element(By.XPATH, xpath_div).find_elements(By.XPATH, xpath_lastpage_text)]

    def list_convert_pagenumbers(self):
        # return list of last pages for the range selected
        list_elem_pagenumbers = self.extract_lastpage()
        if len(list_elem_pagenumbers) == 1:
            self.sqlshit.update_page_count_test()
            return self.list_lastpage.append(1)

            #for some reason fucks up on x which only has one page but
            #this resolves the issue for some fucking reason

        elif len(list_elem_pagenumbers) > 1:
            self.list_lastpage.append(max([int(elem.get_attribute("text").strip())
                for elem in list_elem_pagenumbers if elem.get_attribute("text").strip() != '']))
        return self.list_lastpage





def main():
    database = "data_dafont.db"
    run = sqlShit()
    nur = scraperDafont()
    run.createConnection(database)
    # run.initial_data_population()
    # run.deleteAll()
    # run.update_page_count_test(23,'b')
    # run.select_link_from_lettre('a')
    # run.getTable()
    nur.setup_browser("normal")
    nur.open_page('a')


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











