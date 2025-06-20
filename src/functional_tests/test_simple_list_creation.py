# Third-party (Selenium)
from selenium.webdriver.common.by import By  # Provides strategies for locating elements on a web page
from selenium.webdriver.common.keys import Keys  # Simulates keyboard input (e.g., typing, Enter)

# Local application
from functional_tests.base import FunctionalTest  # Base class for shared functional test setup


class NewVisitorTest(FunctionalTest):
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
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys("Buy peacock feathers") 
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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