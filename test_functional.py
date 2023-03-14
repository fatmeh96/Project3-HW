import itertools
import random
import sqlite3
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from BaseClass import BaseClass

'''RANDOM'''
letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '123456789'
signs = '!@#$%^&*()/|*'
def random_input(argument):
    if argument == letters:
        return ''.join(random.choice(letters) for i in range(10))
    elif argument == numbers:
        return ''.join(random.choice(numbers) for i in range(5))
    else:  # argument == signs
        return ''.join(random.choice(signs) for i in range(5))
    '''END RANDOM'''
@pytest.mark.usefixtures("setup")
@pytest.mark.functional
class TestFunctional(BaseClass):
    #functional_test_1
    def test_add1(self,setup):
        #trying to add new site without adding location info (which is not nullable)
        #go to add site page
        setup.get("http://127.0.0.1:8080/add_sitee")
        #prepare arguments to send to the add form using random function
        site_name = random_input(letters)
        site_data=random_input(letters)
        #sending site's name info
        setup.find_element(By.XPATH, "//input[@id='siteName']").send_keys(site_name)
        x = setup.find_element(By.CSS_SELECTOR, "#siteData")
        x.clear()
        # sending site's data info
        x.send_keys(site_data)
        #click add
        setup.find_element(By.XPATH, "//input[@name='form']").click()
        #connect to the database to check if really added the new site
        _connection = sqlite3.connect("C:\\Users\\admin3\\PycharmProjects\\OurAntiquitiesLand\\Antiquities\\instance\\antiquity.db")
        curses=_connection.cursor()
        curses.execute('SELECT site_name FROM sites')
        sites_names=curses.fetchall()
        list_of_tuples = sites_names
        list_of_filename = list(itertools.chain(*list_of_tuples))
        curses.execute('SELECT about FROM sites')
        sites_data=curses.fetchall()
        list_of_tuples = sites_data
        list_of_sites_data = list(itertools.chain(*list_of_tuples))
        #assertion will be thrown if the site really added : must not add it!
        assert list_of_sites_data[-1] !=site_data and list_of_filename[-1]!= site_name, self.getLogger().error(f"Test failed: can add site without required data of location in {setup.name.lsplit('ms')}")
        self.getLogger().info(f"First add test passed successfully in {setup.name.lstrip('ms')}: can't  add this site doe to null location data!")
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    # functional_test_2
    def test_add2(self,setup):
        #this test cant be made more than one time, because the location (waze) is unique,
        #to run this test again change the location (send key) so we use random for it.
        setup.get("http://127.0.0.1:8080/")
        sites_before = setup.find_elements(By.XPATH, "//img[@height='280px']")
        setup.find_element(By.XPATH,"//u[normalize-space()='ADD']").click()
        all_windows=setup.window_handles
        setup.switch_to.window(all_windows[1])
        #add name
        setup.find_element(By.XPATH, "//input[@id='siteName']").send_keys("site1")
        #add picture
        setup.find_element(By.XPATH,"//input[@name='filename']").send_keys("C:\\Users\\admin3\Desktop\\55.JPG")
        #add data
        setup.find_element(By.CSS_SELECTOR, "#siteData").clear()
        setup.find_element(By.CSS_SELECTOR, "#siteData").send_keys("Data...")
        #add waze (location)
        setup.find_element(By.XPATH, "//input[@id='waze']").send_keys(random_input(letters+signs))
        #click add
        setup.find_element(By.CSS_SELECTOR, "input[value='Add Site']").click()
        sites_after = setup.find_elements(By.XPATH, "//img[@height='280px']")
        assert len(sites_after) > len(sites_before), self.getLogger().error(f"No site is added to {setup.name.lstrip('ms')}")
        self.getLogger().info(f"Second add test passed successfully in {setup.name.lstrip('ms')}!")
#------------------------------------------------------------------------------------------------------------------------------------------------------
    # functional_test_3
    def test_delete1(self,setup):
        #Check Delete
        setup.get("http://127.0.0.1:8080/")
        # checking in a previous site is actually deleted
        try:
            setup.find_element(By.XPATH, "//img[@src='/display/telMegiddo.JPG']").click()
        except NoSuchElementException:
            self.getLogger().info(f"The element is already deleted from {setup.name.lstrip('ms')} : test passed successfully!")
#---------------------------------------------------------------------------------------------------------------------------------------------------
    # functional_test_4
    def test_delete(self,setup):
        #this function will check if a previously deleted item is really deleted.
        setup.get("http://127.0.0.1:8080/")
        try:
            setup.find_element(By.XPATH, "//img[@src='/display/Avdat.jpg']").click()
            setup.find_element(By.XPATH, "//u[normalize-space()='Delete']").click()
        except NoSuchElementException:
            self.getLogger().info(f"The element is already deleted from {setup.name.lstrip('ms')}: test passed successfully!")
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    # functional_test_5
    def test_update1(self,setup):
        #go to the main page
        setup.get("http://127.0.0.1:8080/")
        #click on one of the sites
        setup.find_element(By.XPATH, "//img[@src='/display/Qumran.jpg']").click()
        #click alter
        setup.find_element(By.XPATH,"//u[normalize-space()='Alter']").click()
        #send elements to change: site' name
        a = setup.find_element(By.XPATH, "//input[@name='site_name']")
        b = setup.find_element(By.XPATH, "//input[@value='Update']")
        a.send_keys("oiehfowhgiarbghe")
        #click update
        b.click()
        check1=setup.find_element(By.XPATH,"//p[position()=1]")
        #check if the site's name
        assert check1.text == 'oiehfowhgiarbghe', self.getLogger().error(f"The site does not updated in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"Update test 1 passed successfully in {setup.name.lstrip('ms')}")
#---------------------------------------------------------------------------------------------------------------------------------------------------
    # functional_test_6
    # @pytest.mark.skip
    def test_update2(self,setup):
        #try to update site 10
        setup.get("http://127.0.0.1:8080/alter_site/10")
        a = setup.find_element(By.XPATH, "//textarea[@id='siteData']")
        b = setup.find_element(By.XPATH, "//input[@name='form']")
        a.clear()
        #send new name
        a.send_keys("Herdos palace!!!!..")
        #click update
        b.click()
        check = setup.find_element(By.CSS_SELECTOR,"p:nth-child(3)").text
        #check if the name really chnaged
        assert check == 'Herdos palace!!!!..', self.getLogger().error(f"The site does not updated in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"Update test 2 passed successfully in {setup.name.lstrip('ms')}")



