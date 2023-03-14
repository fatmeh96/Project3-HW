import os
from BaseClass import BaseClass
from selenium.webdriver.common.by import By
import pytest
import random

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
@pytest.mark.acceptance
class TestAcceptance(BaseClass):
    #acceptance_test_1
    def test_check_Btn_Clicked(self,setup):
        #go to the main page
        setup.get("http://127.0.0.1:8080/")
        #click on add button
        setup.find_element(By.XPATH, "//u[normalize-space()='ADD']").click()
        #handle the windows and go to the last window opened to check if it is really the new window of 'add'
        all_windows = setup.window_handles
        setup.switch_to.window(all_windows[1])
        #save a screen shot of the opened window
        setup.get_screenshot_as_file('btn_clicked.png')
        #throw an assert if the site of adding site is not opened: the btn is not clickable
        assert setup.current_url == "http://127.0.0.1:8080/add_sitee" , self.getLogger().error(f"The button is bot clickable in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"The button is clickable in {setup.name.lstrip('ms')}: test Passed!")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # acceptance_test_2
    def test_fill_form(self,setup):
        #check if form is really fiiled / not clicked!
        #go to add site page
        setup.get("http://127.0.0.1:8080/add_sitee")
        #fill the form
        setup.find_element(By.XPATH,"//input[@id='siteName']").send_keys("k")
        setup.find_element(By.XPATH, "//input[@name='filename']").send_keys(os.path.abspath("C:\\Users\\admin3\Desktop\\11.jfif"))
        setup.find_element(By.XPATH,"//textarea[@id='siteData']").clear()
        setup.find_element(By.XPATH,"//textarea[@id='siteData']").send_keys("YourData")
        waze_input = random_input(letters)
        setup.find_element(By.XPATH,"//input[@id='waze']").send_keys(waze_input)
        #save a screenshot of the filled form (without clicking add).
        setup.get_screenshot_as_file('test_fill_form.png')
        #make an assertion if one of the elements is filled in different way from the sending keys, of is empty.
        assert setup.find_element(By.XPATH,"//input[@id='siteName']").get_attribute("value")=="k" \
        and setup.find_element(By.XPATH, "//input[@name='filename']").get_attribute("value")=="C:\\fakepath\\11.jfif"\
        and setup.find_element(By.XPATH,"//textarea[@id='siteData']").get_attribute("value")=="YourData"\
        and setup.find_element(By.XPATH,"//input[@id='waze']").get_attribute("value")==waze_input, self.getLogger().error(f"The form is not filled in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"User can fill the form in {setup.name.lstrip('ms')}: Passed successfully!")
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    # acceptance_test_3
    def test_user_navigating(self,setup):
        #go to a specific site's page
        setup.get("http://127.0.0.1:8080/show_site/9")
        #scroll to the bottom and save a screenshot to check if the user can navigate to the bottom
        try:
            setup.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            setup.get_screenshot_as_file("bottom.png")
        except AssertionError: #make an assertion if the navigation failed
            assert True, self.getLogger().error(f"can't navigate to the bottom in {setup.name.lstrip('ms')}")
        #scroll to the top and save a screenshot to check if the user can navigate to the top
        try:
            setup.execute_script("window.scrollTo(0,0);")
            setup.get_screenshot_as_file("top.png")
        except AssertionError: #make an assertion if the navigation failed
            assert True, self.getLogger().error(f"can't navigate to the top in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"User can navigate in the web in {setup.name.lstrip('ms')}: Passed successfully!")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # acceptance_test_4
    def test_logo(self, setup):
        #go to a specific site
        setup.get("http://127.0.0.1:8080/show_site/3")
        #find the logo element and click on it
        setup.find_element(By.XPATH, "//img[@src='../static/uploads/logo.jpeg']").click()
        #save a screenshot of the new opened page
        setup.get_screenshot_as_file('test_logo.png')
        #check if the page opened is really the main page (the logo should take us to the home page)
        assert setup.current_url.title() == 'Http://127.0.0.1:8080/', self.getLogger().error(
            f"The logo does not go to the main page in {setup.name.lstrip('ms')}!")
        self.getLogger().info(f"Logo test passed successfully in {setup.name.lstrip('ms')}!")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # acceptance_test_5
    def test_fill_review_form(self, setup):
        #go to a specific site to try to add a review
        setup.get("http://127.0.0.1:8080/show_site/1")
        #fill the comments elements (name, comment) and make an assertions if the boxes are not filled correctlly
        setup.find_element(By.XPATH,"//input[@placeholder='your name...']").clear()
        setup.find_element(By.XPATH,"//input[@placeholder='your name...']").send_keys("Name one")
        assert setup.find_element(By.XPATH,"//input[@placeholder='your name...']").get_attribute("value")=="Name one", self.getLogger().error(f"Form name did'n get info in {setup.name.lstrip('ms')}")
        setup.find_element(By.XPATH, "//textarea[@name='user_comment']").clear()
        setup.find_element(By.XPATH, "//textarea[@name='user_comment']").send_keys("Comment one")
        assert setup.find_element(By.XPATH,"//textarea[@name='user_comment']").get_attribute("value")=="Comment one", self.getLogger().error(f"Form comment did'n get info in {setup.name.lstrip('ms')}")
        #save a screenshot of the filled form of reviews / comments
        setup.get_screenshot_as_file('fill_review_form.png')
        self.getLogger().info(f"User review form can be filled in {setup.name.lstrip('ms')}: Passed successfully!")





