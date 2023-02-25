import sqlite3

import pytest
from selenium.webdriver.common.by import By
@pytest.mark.usefixtures("setup")
def test_database_data(setup):
    _connection = sqlite3.connect("antiquity.db")
    cursor = _connection.cursor()
    # eles = setup.find_elements(By.XPATH, "//img[@width='280px']")
    cursor.execute('SELECT filename FROM sites')
    result = cursor.fetchall()
    result=str(result)
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
    for res in result:
        assert  res.__contains__(ALLOWED_EXTENSIONS[0]) or res.__contains__(ALLOWED_EXTENSIONS[1]) or \
        res.__contains__(ALLOWED_EXTENSIONS[2]) or res.__contains__(ALLOWED_EXTENSIONS[3]), "Data base is getting forbidden files!!"
    print("Passed!")
    '''note : this test has to checked again at the end of all the tests "after overriting the database file
    from the project 2 again", due to the adding/ deleting/ updaing results are not shown in the database here, but only 
    in the database of the second project.'''