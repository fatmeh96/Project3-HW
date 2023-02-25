import time
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
@pytest.mark.usefixtures("setup")
def test_add1(setup):
    #trying to add new site without adding location info (which is not nullable)
    setup.get("http://127.0.0.1:5000/add_sitee")
    setup.find_element(By.XPATH, "//input[@id='siteName']").send_keys("site2")
    time.sleep(10)
    x = setup.find_element(By.CSS_SELECTOR, "#siteData")
    x.clear()
    x.send_keys("Data...")
    time.sleep(5)
    setup.find_element(By.XPATH, "//input[@name='form']").click()

def test_add2(setup):
    #this test cant be made more than one time, because the location (waze) is unique, so to make this test again change the location (send key).
    setup.get("http://127.0.0.1:5000/add_sitee")
    setup.find_element(By.XPATH, "//input[@id='siteName']").send_keys("site1")
    time.sleep(10)
    x = setup.find_element(By.CSS_SELECTOR, "#siteData")
    x.clear()
    x.send_keys("Data...")
    time.sleep(5)
    setup.find_element(By.XPATH, "//input[@id='waze']").send_keys("far far away!!!")
    time.sleep(3)
    setup.find_element(By.XPATH, "//input[@name='form']").click()
    time.sleep(5)
    assert setup.find_element(By.CSS_SELECTOR,"a:nth-child(14) img:nth-child(1)").is_displayed(), "No site is added!"
    print("Passed")

def test_delete1(setup):
    # #Check Delete
    setup.get("http://127.0.0.1:5000/")  # mainpage
    # checking in a previous site is actually deleted
    try:
        setup.find_element(By.XPATH, "//img[@src='/display/telMegiddo.JPG']").click()
    except NoSuchElementException:

        print("The element is already deleted!")

def test_delete(setup):
    setup.get("http://127.0.0.1:5000/")  # mainpage
    setup.find_element(By.XPATH, "//img[@src='/display/Avdat.jpg']").click()  # ///display/masada.jpg']
    setup.find_element(By.XPATH, "//u[normalize-space()='Delete']").click()


def test_update1(setup):
    setup.get("http://127.0.0.1:5000/")  # mainpage
    setup.find_element(By.XPATH, "//img[@src='/display/Qumran.jpg']").click()
    setup.get("http://127.0.0.1:5000/alter_site/5")
    a = setup.find_element(By.XPATH, "//input[@name='site_name']")
    b = setup.find_element(By.XPATH, "//input[@value='Update']")
    a.send_keys("oiehfowhgiarbg")
    b.click()
    check1=setup.find_element(By.XPATH,"//p[position()=1]")
    assert check1.text == 'oiehfowhgiarbg', "The site does not updated!"
    print("Passed")


def test_update2(setup):
    setup.get("http://127.0.0.1:5000/alter_site/10")
    a = setup.find_element(By.XPATH, "//textarea[@id='siteData']")
    b = setup.find_element(By.XPATH, "//input[@name='form']")
    a.clear()
    a.send_keys("Herdos palace!!!!")
    b.click()
    check = setup.find_element(By.CSS_SELECTOR,"p:nth-child(3)").text
    assert check == 'Herdos palace!!!!', "The site does not updated!"
    print("Passed")


def test_logo(setup):
    setup.get("http://127.0.0.1:5000/show_site/3")  # mainpage
    setup.find_element(By.XPATH, "//img[@src='../static/uploads/logo.jpeg']").click()
    assert setup.current_url.title() == 'Http://127.0.0.1:5000/', "The logo does not go to the main page!"
    print("Passed")
