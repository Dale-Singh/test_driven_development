# Standard library
import os  # Interact with the operating system and environment variables
import time  # Provides time-related functions like sleep()

# Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Live server for functional tests with static files

# Third-party (Selenium)
from selenium import webdriver  # Controls a web browser for automated functional testing
from selenium.webdriver.common.by import By  # Strategies for locating elements on a web page
from selenium.common.exceptions import WebDriverException  # Exception class for handling browser-related errors

# Local application
from functional_tests.container_commands import _run_commands # used to execute SSH commands to clean up test users from remote server database


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
    
    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

    # Original code
    # def tearDown(self):  
    #     self.browser.quit()

    # The tearDown method runs after each test to clean up resources
    def tearDown(self):
        # ADDED: Clean up test users from server database when testing against remote servers
        # This prevents "UNIQUE constraint failed" errors when multiple tests try to create
        # the same test user (e.g., edith@example.com) on the staging server
        if self.test_server:
            self._cleanup_all_server_users()
        self.browser.quit()

    # ADDED: Function to remove ALL users from server test database
    # This is needed because server tests run against the real production database,
    # not Django's temporary test database, so test data persists between test runs
    def _cleanup_all_server_users(self):
        # ADDED: SSH command to execute user deletion on the remote server
        # Uses proper quoting to escape Python command through bash/SSH layers
        try:
            cleanup_command = [
                "ssh", f"dale@{self.test_server}", 
                "docker", "exec", "superlists",
                "python", "/src/manage.py", "shell", "-c",
                '"from accounts.models import User; User.objects.all().delete()"'
            ]
            _run_commands(cleanup_command)
        except Exception:
            # ADDED: Silent failure handling - cleanup errors shouldn't break tests
            # If cleanup fails, the next test run might have conflicts, but the test
            # itself completed successfully
            pass  # Ignore cleanup errors
    
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


