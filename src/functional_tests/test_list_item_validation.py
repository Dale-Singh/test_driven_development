# Third-party (Selenium)
from selenium.webdriver.common.by import By  # Strategies for locating elements on a web page
from selenium.webdriver.common.keys import Keys  # Simulate keyboard input (e.g., Enter, Backspace)

# Local application
from functional_tests.base import FunctionalTest  # Base class for shared functional test setup

# Allows skipping tests temporarily while keeping them in the suite
from unittest import skip

class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback")
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the list page
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys("Purchase milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Purchase milk")

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table("1: Purchase milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # And she can make it happy by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                "#id_text:valid",
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")
    
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy wellies")

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                "You've already got this in your list",
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Banter too thick")
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertTrue(self.get_error_element().is_displayed())
        )
        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys("a")

        # She is pleased to see that the error message disappears
        self.wait_for(
            lambda: self.assertFalse(self.get_error_element().is_displayed())
        )
