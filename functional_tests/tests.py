# This allows us to interact with the project through a web browser
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
# Imports the By class, which provides different strategies for locating elements on a web page
from selenium.webdriver.common.by import By
# Imports the Keys class, which allows Selenium to simulate keyboard actions
# (e.g., typing, pressing Enter, Backspace).
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 5

# Define the test case class
class NewVisitorTest(LiveServerTestCase):  
    # The setUp method runs before each test to set up any resources needed
    def setUp(self):  
        self.browser = webdriver.Firefox()
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

    def test_can_start_a_todo_list(self):  
        # Edith has heard about a cool new online to-do app
        # She goes to check out its homepage
        # Navigate to the homepage of the Django test server environment
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys("Buy peacock feathers") 
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        # Capture the current URL of the browser after submitting the to-do item
        # This will be used to verify if a unique URL has been generated for Edith's list
        edith_list_url = self.browser.current_url
        # . matches any character, + continues matching any character one or more times
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site.
        # Delete all the browser's cookies to simulate a new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item. 
        # He is less interesting than Edith...
        inputbox = self.browser.find_element(By.ID,"id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peaacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
        
        # Satisfied, they both go back to sleep
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)

        # Her brwoser window is set to a particular size
        self.browser.set_window_size(1024,768)

        # She notices the inbox is nicely centered
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )

        # She starts a new list and and sees the input is nicely centered too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )