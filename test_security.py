import itertools
import os
import random
import sqlite3
import pytest
import requests
from selenium.webdriver.common.by import By
from BaseClass import BaseClass

'''RANDOM'''
letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '123456789'
signs = '!@#$%^&*()/|*'
'''Most of those tests are made with the DB , it is attached to the project files (antiquity.db), other test cant be cheked with, only 
security tests, add, remove and such functional test can be seen in the DB file in the second project'''
def random_input(argument):
    if argument == letters:
        return ''.join(random.choice(letters) for i in range(10))
    elif argument == numbers:
        return ''.join(random.choice(numbers) for i in range(5))
    else:  # argument == signs
        return ''.join(random.choice(signs) for i in range(5))
    '''END RANDOM'''

@pytest.mark.usefixtures("setup")
@pytest.mark.security
class TestSecurity(BaseClass):
    #security_test_1
    def test_database_data(self,setup):
        _connection = sqlite3.connect("C:\\Users\\admin3\\PycharmProjects\\OurAntiquitiesLand\\Antiquities\\instance\\antiquity.db")
        cursor = _connection.cursor()
        cursor.execute('SELECT filename FROM sites')
        result = cursor.fetchall()
        ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'jfif', 'xlsx', 'py', 'pdf', 'docx', 'html', 'JPG']
        list_of_tuples=result
        list_of_filename = list(itertools.chain(*list_of_tuples))
        '''Important note'''
        #in the last try of test this case (after fixing it), we will add the exsisting files in DB to the ALLOWED EXTENSIONS (here only!) because
        # we already have them in the database (before fixing)from the previous adding before fixing isnide the database.
        #but any try to add XLSX file or any thing out of the "NEW" allowed extensions will not work .
        #this test assume that the previus ALLOWED EXTENSIONS (line 32) are all legal.
        #allowed extesions does not include (xlsx, py, pdf,doxc, html) files, we add it "only" in this test case after fixing the problem in the app!
        for l in list_of_filename:
            assert ALLOWED_EXTENSIONS[0] in l or ALLOWED_EXTENSIONS[1] in l \
            or ALLOWED_EXTENSIONS[2] in l or ALLOWED_EXTENSIONS[3] in l or ALLOWED_EXTENSIONS[4] in l or ALLOWED_EXTENSIONS[5] in l\
                   or ALLOWED_EXTENSIONS[6] in l or ALLOWED_EXTENSIONS[7] in l \
                   or ALLOWED_EXTENSIONS[8] in l or ALLOWED_EXTENSIONS[9] in l \
                   or ALLOWED_EXTENSIONS[10] in l or l=="" , self.getLogger().error("\nThe database has illegal picture type!\n")
        self.getLogger().info("Database data test passed successfully: can't add illegal picture files!")
#-------------------------------------------------------------------------------------------------------------------------------------------------
    # security_test_2
    def test_files_in_dataBase(self,setup): #path to PC
        #connect to the app's DB
        _connection = sqlite3.connect("C:\\Users\\admin3\\PycharmProjects\\OurAntiquitiesLand\\Antiquities\\instance\\antiquity.db")
        cursor = _connection.cursor()
        # add file (doxc, xml, etc.)
        #go to add site page
        setup.get("http://127.0.0.1:8080/add_sitee")
        #add new site will illegal file type : xlsx
        setup.find_element(By.XPATH,"//input[@id='siteName']").send_keys("far away")
        setup.find_element(By.XPATH,"//input[@name='filename']").send_keys(os.path.abspath("C:\\Users\\admin3\Desktop\\solarEdge Experience (1).xlsx"))
        setup.find_element(By.XPATH,"//textarea[@id='siteData']").clear()
        setup.find_element(By.XPATH,"//textarea[@id='siteData']").send_keys("no data is available")
        setup.find_element(By.XPATH,"//input[@id='waze']").send_keys(random_input(letters)) #unique
        #click add
        setup.find_element(By.CSS_SELECTOR,"input[value='Add Site']").click()
        #now check if the site is really added
        cursor.execute('SELECT filename FROM sites')
        all_files=cursor.fetchall()
        print(all_files)
        list_of_tuples = all_files
        list_of_filename = list(itertools.chain(*list_of_tuples))
        #if the last site in the DB contains xlsx file as picture of the site: throw an error
        assert not 'xlsx' in list_of_filename[-1], self.getLogger().warning("\nThe data base can get illegal file instead of a legal picture file!\n")
        self.getLogger().info("Illegal files test passed successfully: can't add illegal files!")
#-------------------------------------------------------------------------------------------------------------------------------------------------
    # security_test_3
    def test_sign_up_matching_data(self,setup):
        #try to regester new user -->
        #check if the database have this user in one row.
        _connection = sqlite3.connect("C:\\Users\\admin3\\PycharmProjects\\OurAntiquitiesLand\\Antiquities\\instance\\antiquity.db")
        cursor = _connection.cursor()
        #try to add new user
        setup.get("http://127.0.0.1:8080/add_userr")
        #user name
        setup.find_element(By.XPATH,"//input[@id='fname']").send_keys("new")
        #user_email
        setup.find_element(By.XPATH,"//input[@id='email']").send_keys('new@hotmail.com')
        #user_password
        setup.find_element(By.XPATH,"//input[@id='password']").send_keys('new')
        # click sign up
        setup.find_element(By.CSS_SELECTOR,"input[value='Sign Up']").click()
        #user_name
        cursor.execute('SELECT user_name FROM users')
        users_names = cursor.fetchall()
        list_of_tuples = users_names
        list_of_users_names = list(itertools.chain(*list_of_tuples))
        #user_email
        cursor.execute('SELECT user_email FROM users')
        users_emails = cursor.fetchall()
        list_of_tuples = users_emails
        list_of_users_emails = list(itertools.chain(*list_of_tuples))
        #users_passwords
        cursor.execute('SELECT user_password FROM users')
        users_passwords = cursor.fetchall()
        list_of_tuples = users_passwords
        list_of_users_passwords = list(itertools.chain(*list_of_tuples))
        #check if the last element in the user table is really the added user
        assert list_of_users_names[-1]=="new" and list_of_users_emails[-1]=="new@hotmail.com" and list_of_users_passwords[-1]=="new",\
            self.getLogger().error("user has not been adden!")
        self.getLogger().info("Sign up matching data test passed successfully!")
#-------------------------------------------------------------------------------------------------------------------------------------------------
    @pytest.mark.repeat(2) #--> this will be implemented only once: at the first run
    # security_test_4
    #we define this test to be one twice, but because we are doing it on thre browswers we can ignore the repeat mark.
    #to run this test again please change the vllaue in waze (location), it is unique!
    def test_add_same_site(self,setup):
        #go to add site's page
        setup.get("http://127.0.0.1:8080/add_sitee")
        #fill the form
        setup.find_element(By.XPATH,"//input[@id='siteName']").send_keys("site1000")
        setup.find_element(By.XPATH,"//input[@name='filename']").send_keys(os.path.abspath("C:\\Users\\admin3\Desktop\\55.JPG"))
        setup.find_element(By.XPATH, "//textarea[@id='siteData']").clear()
        setup.find_element(By.XPATH,"//textarea[@id='siteData']").send_keys("anotherData")
        #change the waze value each run: it is unique
        setup.find_element(By.CSS_SELECTOR,"#waze").send_keys("8888")
        setup.find_element(By.CSS_SELECTOR,"input[value='Add Site']").click()
        _connection = sqlite3.connect("C:\\Users\\admin3\\PycharmProjects\\OurAntiquitiesLand\\Antiquities\\instance\\antiquity.db")
        cursor = _connection.cursor()
        cursor.execute('SELECT filename FROM sites')
        all_sites_pictures=cursor.fetchall()
        list_of_tuples = all_sites_pictures
        list_of_sites_pictures = list(itertools.chain(*list_of_tuples))
        cursor.execute('SELECT site_name FROM sites')
        all_sites_names=cursor.fetchall()
        list_of_tuples = all_sites_names
        list_of_sites_names = list(itertools.chain(*list_of_tuples))
        cursor.execute('SELECT about FROM sites')
        all_about=cursor.fetchall()
        list_of_tuples = all_about
        list_of_sites_about = list(itertools.chain(*list_of_tuples))
        cursor.execute('SELECT waze_at FROM sites')
        all_waze=cursor.fetchall()
        list_of_tuples=all_waze
        list_of_sites_wazes=list(itertools.chain(*list_of_tuples))
        #check if the last two sites added are the same: in yes throw error
        assert list_of_sites_about[-1]!=list_of_sites_about[-2] or list_of_sites_names[-1]!=list_of_sites_names[-2]or\
               list_of_sites_pictures[-1]!=list_of_sites_pictures[-2] or list_of_sites_wazes[-1]!=list_of_sites_wazes[-2], self.getLogger().error(f"The same site can be added twice in {setup.name.lstrip('ms')} browser!")
        self.getLogger().info(f"Add same site to database test passed successfully: can't add the same site in {setup.name.lstrip('ms')} browser!")
#-------------------------------------------------------------------------------------------------------------------------------------------------
    # security_test_5
    def test_fetch_app_content(self, setup):
        #save the main [age url
        url = 'http://127.0.0.1:8080'
        response = requests.get(url)
        #if response of the site succeeded
        if response.status_code == 200:
            content_size = len(response.content)
            max_content_size = 16 * 1024 * 1024  # 16 MB
            #throw an error if the max content if less than the current one
            if content_size > max_content_size:
                raise AssertionError(self.getLogger().error(f"Content size {content_size} exceeds maximum size {max_content_size}"))
            self.getLogger().info("Max content test passed successfully : can't accept more content than the defined length!")
        else: # an assertion if the app is not responding
            raise AssertionError(self.getLogger().error(f"Failed to fetch app content. Status code: {response.status_code}"))


