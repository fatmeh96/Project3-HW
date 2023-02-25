from selenium import webdriver
#--------------------------------------------------------
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.firefox.service import Service
#--------------------------------------------------------
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.firefox.options import Options
# #--------------------------------------------------------
import pytest
#-------------------------------------------------------------------------------------------------------------------------------------
#--for chrome--#
@pytest.fixture()
def setup():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service_obj = Service("chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver
#-------------------------------------------------------------------------------------------------------------------------------------
#--for edge--#
# @pytest.fixture()
# def setup():
#     edge_options = Options()
#     edge_options.add_experimental_option("detach", True)
#     service_obj = Service("")
#     driver = webdriver.Edge(service=service_obj, options=edge_options)
#     driver.implicitly_wait(5)
#     driver.maximize_window()
#     return driver
#-------------------------------------------------------------------------------------------------------------------------------------
#--for firefox--#
# def setup():
#     firefox_options = Options()
#     firefox_options.add_experimental_option("detach", True)
#     service_obj = Service("")
#     driver = webdriver.Firefox(service=service_obj, options=firefox_options)
#     driver.implicitly_wait(5)
#     driver.maximize_window()
#     return driver
