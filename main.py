# IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import configparser
import sqlite3
from sqlite3 import Error

# OKAY HEAR ME OUT. JUST USE CONFIG FILES
# Like, seriously fuck it, who cares, you can learn sql later.
config = configparser.ConfigParser()
config.read('config.ini')

options = webdriver.ChromeOptions()

headless = True
# DATA
url_dafont = 'https://www.dafont.com/alpha.php?lettre={}&page={}&fpp=200'
keys = [ascii for ascii in ascii_lowercase] + ['%23']
values = [url_dafont.format(values, '1') for values in keys]


class sqlShit:
    # BROWSER SPECIFIC FUNCTIONS
    def setup_browser(self, strat, dl_location):  # strat = normal (complete), eager (interactive), none (undefined)
        # BROWSWER SETUP DETAILS
        # initiate with config file reference for dl_location as to make this more usable for other websites
        # PREFERENCES - set preferences for options of browser
        prefs = {"download.default_directory": dl_location,
                 'profile.default_content_setting_values.automatic_downloads': 1,
                 "excludeSwitches": ["test-type", "enable-automation"]
                 }

        # OPTIONS

        options.add_experimental_option("prefs", prefs)
        options.headless = headless

        # SERVICE
        service = Service(r'D:\Code\Chromedriver\chromedriver.exe')

        # CAPABILITIES - set how long driver waits
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = strat  # see above choices

        self.driver = webdriver.Chrome(desired_capabilities=caps, service=service, options=options)
        self.driver.create_options()
        print("Browser configuration complete.\n")

    # GENERAL SQL FUNCTIONS
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
            print("Failed to connect to database", e)

        return self.conn

    def get_full_table(self, table):
        try:
            cur = self.conn.cursor()
            sql_queery = "SELECT * FROM {}".format(table)
            cur.execute(sql_queery)
            print("Successfully retrieved table:")
            print(cur.fetchall())
            return cur.fetchall()
        except Error as e:
            print("\nERROR:", e, "\nCheck database name.")

    def get_full_column(self, table, column):
        # returns a list that can be iterated through in other functions for efficiency
        # probably make that a sub function of this one for iterable actions
        # enter and retrieve a full column from a selected table
        try:
            cur = self.conn.cursor()
            sql_queery = "SELECT {} FROM {}".format(column, table)
            cur.execute(sql_queery)
            rows = cur.fetchall()
            rows = [i[0] for i in rows]
            print("Successfully retrieved column {}:".format(column))
            print(rows)
            return rows

        except Error as e:
            print("Failed to retrieve the column, check column name in function.")

    def delete_full_table(self, table):
        try:
            cur = self.conn.cursor()
            sql_queery = "DELETE FROM {}".format(table)
            cur.execute(sql_queery)
            print("Table successfully deleted")
        except Error as e:
            print(e)

    # URL_DATA SPECIFIC FUNCTIONS
    def get_page_count_by_letter(self, lettre):
        # returns the page count of the entered letter
        # use this as a comparitor (however the fuck you spell that) variable when checking pages...
        # ...on reruns to rescrape the site for new shit
        try:
            cur = self.conn.cursor()
            sql_queery = "select page_count from url_data where lettre = '%s'" % lettre
            cur.execute(sql_queery)
            rows = cur.fetchall()
            rows = [i[0] for i in rows]
            rows = rows[0]
            print("Successfully retrieved page count for lettre {}: {}".format(lettre, rows))
            return rows
        except Error as e:
            print("ERROR: " + str(e))


    # DL_DATA TABLE SPECIFIC FUNCTIONS




    # EXPERIMENTAL/GRAVEYARD FOR REMOVAL - need to add functionality to grab page count from webpage
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
        # ADD FUNCTIONALITY TO REFERENCE CONFIG FILE HERE

        xpath_div_var = self.driver.find_element(By.XPATH, config['xpaths_dafont']['main_page_elem'])
        xpath_lastpage_text_var = [elem for elem in xpath_div_var.find_elements(By.XPATH,
                                                                                config['xpaths_dafont']['sub_page_elem'])]

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


    def check_page_size(self):
        pass



def main():
    database = "data_dafont.db"
    run = sqlShit()
    run.create_connection(database)
    run.get_full_table('url_data')
    run.get_full_column('url_data', 'page1_url')
    run.get_page_count_by_letter('a')


if __name__ == '__main__':
    main()





# DUST BIN OF HISTORY

# don't do this shit, just manually create it using an sql queery with shit generated from
# excel to save time
# def initialDataPopulation(self):
#     #create the initial data table with page letters and page 1 urls
#     for i in range(len(keys)):
#         self.insertVaribleIntoTable(lettre=keys[i], page1_url=values[i])
#     self.conn.commit()


# PLEASE STOP DOING THIS SHIT. Literally just create the shit manually and populate from there, not
# everything needs to be coded in Python for this to work or for me to be satisfied. Just like tracing
# as a base for a drawing. There is no shame in manual setup.
    #
    # def insertVaribleIntoTable(self, lettre=None, page1_url=None, page_count=None):
    #     try:
    #         sqlite_insert_with_param = """INSERT INTO url_data
    #                           (lettre, page1_url, page_count)
    #                           VALUES (?, ?, ?);"""
    #
    #         data_tuple = (lettre, page1_url, page_count)
    #         cur = self.conn.cursor()
    #         cur.execute(sqlite_insert_with_param, data_tuple)
    #         # self.conn.commit()
    #         print("Python Variables inserted successfully into SqliteDb_developers table")
    #
    #     except Error as e:
    #         print("Failed to insert Python variable into sqlite table", e)

    # for i in range(len(keys)):
    #     print("{}={},".format(keys[i], values[i]))
        # print("\'{}\':\'{}\',".format(keys[i],values[i]))

    # f = config.read("config.ini")


#

# cur.execute("create table url_data (lettre, page1_url, page_count)")

# for i in range(len(keys)):
#     cur.execute("INSERT INTO url_data (lettre, page1_url) VALUES (?, ?)", (keys[i], values[i]))
# con.commit()

# cur.execute("insert into url_data (lettre) values ('cum')")
#
# for row in cur.execute('SELECT page1_url FROM url_data'):
#         print(row)
