import time
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from BaseClass import BaseClass

@pytest.mark.usefixtures("setup")
@pytest.mark.smoke
class TestSmoke(BaseClass):
    #smoke_test_1
    def test_checkTitle(self, setup):
        #go to the main page
        setup.get("http://127.0.0.1:8080/")
        #find the title element and save it
        title = setup.find_element(By.CSS_SELECTOR, "div[class='navbar'] h1").text
        #check ig the text of the title is really as required
        assert title=="Our Antiquities Land", self.getLogger().error(f"Failed! the title is different in {setup.name}")
        self.getLogger().info(f"Check title test (smoke test) passed successfully in {setup.name.lstrip('ms')} --> the title is as required!")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # smoke_test_2
    def test_diplayed_picture(self,setup):
        # go to a specific site's page
        setup.get("http://127.0.0.1:8080/show_site/1")
        # find the image element
        ImageFile2 = setup.find_element(By.XPATH, ("//div[@class='flex-container']//div//img"))
        ImagePresent2 = setup.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",
            ImageFile2);
        #if not diplayed: throw error message
        assert ImagePresent2 == True, self.getLogger().error(f"The picture is not displayed in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"Displayed picture test in {setup.name.lstrip('ms')} passed successfully!!")
#---------------------------------------------------------------------------------------------------------------------------------------------------
    # smoke_test_3
    def test_picture2_is_displayed(self,setup):
        #go to a specific site's page
        setup.get("http://127.0.0.1:8080/show_site/16")
        #find the image element
        ImageFile = setup.find_element(By.XPATH, ("//div[@class='flex-container']//div//img"))
        #check if it is displayed
        ImagePresent = setup.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",
            ImageFile);
        #if not diplayed: throw error message
        assert ImagePresent == True,self.getLogger().error(f"The picture is not displayed in {setup.name.lstrip('ms')}")
        self.getLogger().info(f"Displayed picture test in {setup.name.lstrip('ms')} passed successfully!!")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # smoke_test_4
    def test_response_of_site(self, setup):
        #try to check some page in the web
        setup.get("http://127.0.0.1:8080/show_site/1")
        wait = WebDriverWait(setup, 10)
        body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        #if the body is not displayed : throw an error (normal size)
        assert body.is_displayed(), self.getLogger().error(f"Can't display size in {setup.name.lstrip('ms')}")
        #set new size and scroll to the top to find the body element
        setup.set_window_size(640, 480)
        setup.execute_script("window.scrollTo(0, 0);")
        #find the body and check if displayed, if not throw error message
        body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        assert body.is_displayed(), self.getLogger().error(f"Can't display size in {setup.name.lstrip('ms')}")
        # set new size and scroll to the top to find the body element
        setup.set_window_size(1920, 1080)
        setup.execute_script("window.scrollTo(0, 0);")
        # find the body and check if displayed, if not throw error message
        body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        assert body.is_displayed(), self.getLogger().error(f"Can't display size in {setup.name.lstrip('ms')}")
        #the web can be dislayed in all system's sizes
        self.getLogger().info(f"The site can get all size in {setup.name.lstrip('ms')}")
#----------------------------------------------------------------------------------------------------------------------------------------------------
    # smoke_test_5
    def test_links_of_main_page(self,setup):
        setup.get("http://127.0.0.1:8080/") #main page
        #click add button
        setup.find_element(By.XPATH,"//u[normalize-space()='ADD']").click()
        all_windows = setup.window_handles
        setup.switch_to.window(all_windows[1])
        #check if the second window opened is really the add page
        assert setup.current_url == 'http://127.0.0.1:8080/add_sitee', self.getLogger().error(f"Links are not working as required in {setup.name.lstrip('ms')}!")
        self.getLogger().info(f"Link is working as required in {setup.name.lstrip('ms')}: Passed successfully!")