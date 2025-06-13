# Standard library
import os  # Interact with the operating system and environment variables
import time  # Provides time-related functions like sleep()

# Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Live server for functional tests with static files

# Third-party (Selenium)
from selenium import webdriver  # Controls a web browser for automated functional testing
from selenium.webdriver.common.by import By  # Strategies for locating elements on a web page
from selenium.common.exceptions import WebDriverException  # Exception class for handling browser-related errors

MAX_WAIT = 5

# Define the test case class, inheriting from StaticLiveServerTestCase  
# to enable functional testing with access to static files
class FunctionalTest(StaticLiveServerTestCase):
    # The setUp method runs before each test to set up any resources needed
    def setUp(self):  
        self.browser = webdriver.Firefox()
        # Check if a test server is specified in the environment variables i.e. staging.example.com
        test_server = os.environ.get("TEST_SERVER")
        # If TEST_SERVER exists, override self.live_server_url to use the specified server  
        # This allows testing on a remote test server instead of Django's default (http://127.0.0.1:8000/)
        if test_server:
            self.live_server_url = "http://" + test_server
    
    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

    # The tearDown method runs after each test to clean up resources
    def tearDown(self):  
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        # Record the start time to track how long the function has been waiting
        start_time = time.time()
    
        # Continuously attempt to find the row until successful or timeout occurs
        while True:
            try:
                # Locate the table element by its ID, returns a WebElement object
                table = self.browser.find_element(By.ID, "id_list_table")
                # Find all table row (<tr>) elements within the table, 
                # each row is returned as a WebElement object
                rows = table.find_elements(By.TAG_NAME, "tr")
                # Verify if the desired row_text exists within the table rows
                self.assertIn(row_text, [row.text for row in rows])
                # Exit the loop and function if the assertion passes (item found)
                return
            
            # Handle AssertionError (if text not found) or WebDriverException (if page not fully loaded)
            except (AssertionError, WebDriverException):
                # Check if the maximum wait time has been exceeded
                if time.time() - start_time > MAX_WAIT:
                    # Re-raise the original error to indicate failure
                    raise  
                # Pause for 0.5 seconds before retrying
                time.sleep(0.5)
    
    def wait_for(self, fn):
        start_time = time.time()
    
        # Continuously attempt to run the function until successful or timeout occurs
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
    
    # Waits until the logout button appears and confirms the user's email is shown in the navbar
    def wait_to_be_logged_in(self, email):
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)
    
    # Waits until the login input appears and confirms the user's email is no longer in the navbar
    def wait_to_be_logged_out(self, email):
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)


