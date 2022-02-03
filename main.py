import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import os
import sqlite3
from sqlite3 import Error

headless = True
# DATA
url_dafont = 'https://www.dafont.com/alpha.php?lettre={}&page={}&fpp=200'
keys = [ascii for ascii in ascii_lowercase] + ['%23']
values = [url_dafont.format(values, '1') for values in keys]

# dafont - page text vars
xpath_div = "//div[@class='noindex']"
xpath_lastpage_text = ".//a[contains(@href, 'alpha.php?lettre=')]" #working version
# xpath_lastpage_text = "//a[contains(@href, 'alpha.php?lettre=')]" #test
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

    def create_dl_link_table(self):
        cur = self.conn.cursor()
        sqlquery = "create table dl_data (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z)" #CHAR(37)+ 23)"
        sqlquery2 = "ALTER TABLE dl_data ADD \%23''
        cur.execute(sqlquery2)


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
        #update this so it returns a ilst who cares
        cur = self.conn.cursor()
        sql_link_query = "select page1_url from url_data where lettre = '%s'" % (lettre)
        cur.execute(sql_link_query)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        return rows[0]

    def retrieve_lettre_page1_url_list(self):
        #update this so it returns a ilst who cares
        cur = self.conn.cursor()
        sql_link_query = "select page1_url from url_data"
        cur.execute(sql_link_query)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        return rows

    def list_lettres(self):
        cur = self.conn.cursor()
        sql_link_query = "select lettre from url_data"
        cur.execute(sql_link_query)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        return rows

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

    def extract_lastpage_updatetable(self, link):

        cur = self.conn.cursor()
        # this is an initial run anyway so I don't think it'll matter. Can add functionality to check shit
        # later
        #use letter from sql to get certain data points on it
        # this is ass backwards and stupid but I don't care
        sql_link_query = "select lettre from url_data where page1_url = '%s'" % (link)
        cur.execute(sql_link_query)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        lettre = rows[0]

        # var = self.retrieve_lettre_page1_url()
        self.driver.get(link)
        print("Opening page one of letter: {}".format(lettre))

        # component that updates the table will likely need to be moved to separate def that checks
        # if the last page extracted is greater than what already exists in the table but we will
        # let this slide for now fuck it
        # figure out a way to set this object to be passed from the previous definition
        xpath_div_var = self.driver.find_element(By.XPATH, xpath_div)
        xpath_lastpage_text_var = [elem for elem in xpath_div_var.find_elements(By.XPATH, xpath_lastpage_text)]

        if len(xpath_lastpage_text_var) == 1:
            self.update_page_count_test(1, lettre)

            # return self.list_lastpage.append(1)

            #for some reason fucks up on x which only has one page but
            #this resolves the issue for some fucking reason

        elif len(xpath_lastpage_text_var) > 1:
            page_ints = [int(elem.get_attribute("text").strip()) for elem in xpath_lastpage_text_var
                               if elem.get_attribute("text").strip() != '']
            max_page = max(page_ints) #returns max of the list
            self.update_page_count_test(max_page, lettre)

    def create_lettre_table(self):
        pass

    def check_page_size(self):
        pass



def main():
    database = "data_dafont.db"
    run = sqlShit()
    run.createConnection(database)
    run.create_dl_link_table()
    # print(','.join(keys))
#
#     run.setup_browser("normal")
#     for i in run.retrieve_lettre_page1_url_list():
#         run.extract_lastpage_updatetable(i)
#
#     run.getTable()

    # run.initial_data_population()
    # run.deleteAll()
    # run.update_page_count_test(23,'b')
    # run.select_link_from_lettre('a')
    # run.getTable()

    #
    # run.getTable()

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











