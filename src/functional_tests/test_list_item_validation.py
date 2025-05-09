# Imports our custom class from base.py
from functional_tests.base import FunctionalTest

# Imports the By class, which provides different strategies for locating elements on a web page
from selenium.webdriver.common.by import By

# Imports the Keys class, which allows Selenium to simulate keyboard actions
# (e.g., typing, pressing Enter, Backspace).
from selenium.webdriver.common.keys import Keys

# Allows skipping tests temporarily while keeping them in the suite
from unittest import skip

class ItemValidationTest(FunctionalTest):
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