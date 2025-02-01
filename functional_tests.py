# Framework
import unittest
# Import the webdriver module from the Selenium library
# This allows us to interact with web browsers through Selenium
from selenium import webdriver
# Imports the By class, which provides different strategies for locating elements on a web page
from selenium.webdriver.common.by import By
# Imports the Keys class, which allows Selenium to simulate keyboard actions
# (e.g., typing, pressing Enter, Backspace).
from selenium.webdriver.common.keys import Keys
# Import the time module
import time

# Define the test case class
class NewVisitorTest(unittest.TestCase):  
    # The setUp method runs before each test to set up any resources needed
    def setUp(self):  
        self.browser = webdriver.Firefox()
    # The tearDown method runs after each test to clean up resources
    def tearDown(self):  
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        # Locate the table element by its ID
        table = self.browser.find_element(By.ID, "id_list_table")
        # Find all table row (<tr>) elements within the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        # Verify the entry is present within in the table
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_todo_list(self):  
        # Edith has heard about a cool new online to-do app
        # She goes to check out its homepage
        # Navigate to the specified URL (localhost:8000)
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        # Locate the first <h1> element this is returned as a WebElement oject
        # Retrieve the text located in the .text field
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        # Verify the placeholder text
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys("Buy peacock feathers") 
        inputbox.send_keys(Keys.ENTER)
        # Pause for 1 second to allow the page to refresh before assertions are executed
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy peacock feathers") 

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep
        self.fail("Finish the test!")

        # (This comment is just a placeholder; in a real test, the application behavior would be validated)

# This runs the tests when the script is executed directly
# All scripts have an inbuilt variable __name__ when a script is run directly
# __name__ is set to __main__ executing the code inside the if statement
if __name__ == "__main__":  
    unittest.main()  # Start the test runner to execute the test methods