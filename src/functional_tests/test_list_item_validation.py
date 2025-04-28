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

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item, which now works

        # Perversely, she now decides to submit a second blank list item

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail("write me!")