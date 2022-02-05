# IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from string import ascii_lowercase
import configparser
import sqlite3
from sqlite3 import Error

config = configparser.ConfigParser()
config.read('config.ini')

class sqlShit():
    # PICKLE SHIT
    # create function to pickle dump shit and clear a pickle file, use this to document when there are
    # updates to page count so we can go in and check if there are any to which the code will pull download
    # links according to letters that had changes so the entire website doesn't need to be scanned


    # BROWSER SPECIFIC FUNCTIONS
    def setup_browser(self, strat, dl_location, headless):  # strat = normal (complete), eager (interactive), none (undefined)
        # BROWSWER SETUP DETAILS
        # initiate with config file reference for dl_location as to make this more usable for other websites
        # PREFERENCES - set preferences for options of browser
        prefs = {"download.default_directory": dl_location,
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

    def get_all_table_names(self):
        cur = self.conn.cursor()
        sql_queery = "SELECT name FROM sqlite_master WHERE type='table';"
        cur.execute(sql_queery)
        print(cur.fetchall())

    def drop_table(self, table):
        try:
            cur = self.conn.cursor()
            sql_queery = "drop table {}".format(table)
            cur.execute(sql_queery)
            print("Table successfully deleted.")
        except Error as e:
            print("\nERROR:", e, "\nCheck database name.")

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

    def list_lettre(self):
        cur = self.conn.cursor()
        sql_link_queery = "select lettre from url_data"
        cur.execute(sql_link_queery)
        rows = cur.fetchall()
        rows = [i[0] for i in rows]
        return rows

    def delete_table_rows(self, table):
        try:
            cur = self.conn.cursor()
            sql_queery = "DELETE FROM {}".format(table)
            cur.execute(sql_queery)
            print("Table successfully deleted")
        except Error as e:
            print(e)

    # URL_DATA SPECIFIC FUNCTIONS
    def get_page_count_by_lettre(self, lettre):
        # returns the page count of the entered letter
        # use this as a comparitor (however the fuck you spell that) variable when checking pages...
        # ...on reruns to rescrape the site for new shit
        try:
            cur = self.conn.cursor()
            sql_queery = "select page_count from url_data where lettre = '{}'".format(lettre)
            cur.execute(sql_queery)
            rows = cur.fetchall()
            rows = [i[0] for i in rows]
            rows = rows[0]
            print(rows)
            # rows = rows[0]
            print("Successfully retrieved page count for lettre {}: {}".format(lettre, rows))
            cur.close()
            return rows
        except Error as e:
            print("ERROR: " + str(e))

    def get_page1_url_by_lettre(self, lettre):
        # returns the page count of the entered letter
        # use this as a comparitor (however the fuck you spell that) variable when checking pages...
        # ...on reruns to rescrape the site for new shit
        try:
            cur = self.conn.cursor()
            sql_queery = "select page1_url from url_data where lettre = '{}'".format(lettre)
            cur.execute(sql_queery)
            page1_url = cur.fetchall()
            page1_url = [i[0] for i in page1_url]
            page1_url = page1_url[0]
            print(page1_url)
            # rows = rows[0]
            print("Successfully retrieved page1_url for lettre {}: {}".format(lettre, str(page1_url)))
            cur.close()
            return lettre, page1_url
        except Error as e:
            print("ERROR: " + str(e))

    def update_page_count(self, lettre, update_var):
        try:
            #uhhhhh I have no clue if this will work and if it does I don't know why lol
            let_var, page_count = self.get_page_count_by_lettre(lettre)
            cur = self.conn.cursor()

            if update_var == page_count:
                print("No changes detected in page count since last run.")

            elif update_var > page_count:
                print("Change detected. Updating...")
                sql_update_queery = "update url_data set page_count = %s where lettre = '%s'" % (
                    update_var, let_var)  # page_count
                cur.execute(sql_update_queery)
                self.conn.commit()
                print("Record Updated successfully")

            cur.close()

        except Error as e:
            print("Failed to update table.", e)

    def extract_lastpage_update_table(self,lettre):
        # function to get page count from webpage
        # cur = self.conn.cursor()
        # this is an initial run anyway so I don't think it'll matter. Can add functionality to check shit
        # later
        #use letter from sql to get certain data points on it
        # this is ass backwards and stupid but I don't care
        let_var2, page1_var2 = self.get_page1_url_by_lettre(lettre)
        self.setup_browser(strat='normal', dl_location=config['dl_location']['dafont'], headless=True)
        # var = self.retrieve_lettre_page1_url()
        self.driver.get(page1_var2)
        print("Opening page one of letter: {}".format(let_var2))

        xpath_div_var = self.driver.find_element(By.XPATH, config['xpaths']['dafont_main_page_elem'])
        xpath_lastpage_text_var = [elem for elem in xpath_div_var.find_elements(By.XPATH,
                                                                                str(config['xpaths']['dafont_sub_page_elem']))]
        if len(xpath_lastpage_text_var) == 1:
            self.update_page_count(lettre, 1)

            #for some reason fucks up on x which only has one page but
            #this resolves the issue for some fucking reason

        elif len(xpath_lastpage_text_var) > 1:
            page_ints = [int(elem.get_attribute("text").strip()) for elem in xpath_lastpage_text_var
                               if elem.get_attribute("text").strip() != '']
            max_page = max(page_ints) #returns max of the list
            self.update_page_count(lettre, max_page)


    # OOF DL DATA WILL NEED TO BE SPLIT UP INTO TABLES FOR EACH LETTER SO THAT I CAN TRACK PAGE NUMBER, DL LINK, AND IF
    # I ACTUALLY DOWNLOADED IT OR IF I JUST SCRAPED THE VALUES TO BE DOWNLOADED LATER, MAYBE ADD OBJECT TO TELL IT TO
    # SCRAPE VS DOWNLOAD
    # DL DATA SPECIFIC FUNCTIONS

    def TESTING_get_dl_urls_update_table(self,lettre_var, page_num):
        # checks if the dl_str extracted from the site already exists in the database
        self.setup_browser(strat='normal', dl_location=config['dl_location']['dafont'], headless=True)
        print("Opening URL...")
        link = config['baselink']['dafont'].format(lettre_var, page_num)
        self.driver.get(link)
        print("URL successfully opened.")
        for elem in self.driver.find_elements(By.XPATH, str(config['xpaths']['dafont_dl_elem'])):
            dl_urls = elem.get_attribute("href").replace(config['baselink']['dafont_dl'].format(""), "")
            cur = self.conn.cursor()
            # check if exists in db already
            sql_queery = "SELECT rowid FROM dl_data WHERE dl_str = '{}'".format(dl_urls)
            cur.execute(sql_queery)
            data = cur.fetchall()
            if len(data) == 0:
                print("No record of this string currently exists. Proceeding to enter necessary data.")
                sql_queery_2 = "insert into dl_data (lettre_key, page, dl_str, file_saved) values ('%s', %s, '%s', 'FALSE');" % \
                             (lettre_var, page_num, dl_urls)
                cur.execute(sql_queery_2)
                self.conn.commit()
                cur.close()
                print("Record Updated successfully for: {}".format(dl_urls))
            else:
                print("This record already exists... Proceeding to next record.")




def main():
    # keys = [ascii for ascii in ascii_lowercase] + ["'%23'"]
    database = "data_dafont.db"
    run = sqlShit()
    run.create_connection(database)
    # for let_var in keys:
    #
    #    run.drop_table(let_var)
    lettre = 'a'
    page_count = run.get_page_count_by_lettre(lettre)
    print(page_count)
    for i in range(1, page_count+1):
        run.TESTING_get_dl_urls_update_table(lettre_var=lettre,page_num=i)

    # run.get_full_table(table=let_var)
    # run.delete_table_rows('dl_data')

    # run.get_full_column('url_data', 'page1_url')

    # run.get_page_count_by_lettre(lettre=let_var)
    # run.extract_lastpage_update_table(lettre=let_var)
    # run.get_full_table(table='url_data')
    # run.open_urls_by_lettre()

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


    # def retrieve_lettre_page1_url(self, lettre):
    #     #update this so it returns a ilst who cares
    #     cur = self.conn.cursor()
    #     sql_link_query = "select page1_url from url_data where lettre = '%s'" % (lettre)
    #     cur.execute(sql_link_query)
    #     rows = cur.fetchall()
    #     rows = [i[0] for i in rows]
    #     return rows[0]


    #
    # def retrieve_lettre_page1_url_list(self):
    #     #update this so it returns a ilst who cares
    #     cur = self.conn.cursor()
    #     sql_link_query = "select page1_url from url_data"
    #     cur.execute(sql_link_query)
    #     rows = cur.fetchall()
    #     rows = [i[0] for i in rows]
    #     return rows

    # def cursor_iteration(self, x):
    #     cur = self.conn.cursor()
    #     cur.execute('select * from url_data')
    #     for row in cur:
    #         print(row[x])

# xpath_dl_var = [elem for elem in self.driver.find_elements(By.XPATH, str(config['xpaths']['dafont_dl_elem']))]
        #
        #
        # dl_urls = [elem.get_attribute("href").replace(config['baselink']['dafont_dl'].format(""),"") for elem in xpath_dl_var]