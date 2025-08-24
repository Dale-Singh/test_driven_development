# Standard library
import os  # Interact with the operating system and environment variables
import time  # Provides time-related functions like sleep()

# Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Live server for functional tests with static files

# Third-party (Selenium)
from selenium import webdriver  # Controls a web browser for automated functional testing
from selenium.webdriver.common.by import By # Strategies for locating elements on a web page
from selenium.webdriver.common.keys import Keys # Simulate keyboard input (e.g., Enter, Backspace)
from selenium.common.exceptions import WebDriverException  # Exception class for handling browser-related errors

# Local application
from .container_commands import reset_database  # Function to reset database on server for clean test state


MAX_WAIT = 5

# Define the test case class, inheriting from StaticLiveServerTestCase  
# to enable functional testing with access to static files
class FunctionalTest(StaticLiveServerTestCase):
    # The setUp method runs before each test to set up any resources needed
    def setUp(self):  
        self.browser = webdriver.Firefox()
        # Check if a test server is specified in the environment variables i.e. staging.example.com
        self.test_server = os.environ.get("TEST_SERVER")
        # If TEST_SERVER exists, override self.live_server_url to use the specified server  
        # This allows testing on a remote test server instead of Django's default (http://127.0.0.1:8000/)
        if self.test_server:
            self.live_server_url = "http://" + self.test_server
            reset_database(self.test_server) # Flush database to ensure clean state for each test
    
    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

    # The tearDown method runs after each test to clean up resources 
    def tearDown(self):  
        self.browser.quit()
    
    def wait(fn):
        def modified_fn(*args, **kwargs):
            # Record the start time to track how long we’ve been waiting
            start_time = time.time()
            
            # Keep trying the function until it succeeds or times out
            while True:
                try:
                    return fn(*args, **kwargs)
                # Retry on assertion failures or browser loading issues
                except (AssertionError, WebDriverException):
                    # Raise the exception if we've waited too long
                    if time.time() - start_time > MAX_WAIT:
                        raise
                    # Wait briefly before trying again
                    time.sleep(0.5)
        return modified_fn
    
    @wait
    def wait_for_row_in_list_table(self, row_text):
        # Get all rows in the list table
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        # Assert that the expected text is present in one of the rows
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn()
    
    # Waits until the logout button appears and confirms the user's email is shown in the navbar
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)
    
    # Waits until the login input appears and confirms the user's email is no longer in the navbar
    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)
    
    # Adds a new item to the list by typing into the input box and pressing Enter,
    # then waits until the new row appears in the list table with the correct number
    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr"))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")


