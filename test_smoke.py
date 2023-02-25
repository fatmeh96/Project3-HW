import pytest
from selenium.webdriver.common.by import By
@pytest.mark.usefixtures("setup")
def test_checkTitle(setup):
    setup.get("http://127.0.0.1:5000/")
    title=setup.find_element(By.CSS_SELECTOR,"div[class='navbar'] h1").text
    print(title)
    assert title=="Our Antiquities Land", "Failed! the title is different"
    print("Passed")

def test_diplayed_picture(setup):
    setup.get("http://127.0.0.1:5000/show_site/1")
    ImageFile2 = setup.find_element(By.XPATH, ("//div[@class='flex-container']//div//img"))
    ImagePresent2 = setup.execute_script(
        "return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",
        ImageFile2);
    assert ImageFile2 == True, "The picture is not displayed!"
    print("Passed")

def test_picture2_is_displayed(setup):
    setup.get("http://127.0.0.1:5000/show_site/16")
    ImageFile = setup.find_element(By.XPATH, ("//div[@class='flex-container']//div//img"))
    ImagePresent = setup.execute_script(
        "return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",
        ImageFile);
    assert ImageFile == True,"The picture is not displayed!"
    print("Passed")