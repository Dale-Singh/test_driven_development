# Imports our custom class from base.py
from functional_tests.base import FunctionalTest

# Imports the By class, which provides different strategies for locating elements on a web page
from selenium.webdriver.common.by import By

# Imports the Keys class, which allows Selenium to simulate keyboard actions
# (e.g., typing, pressing Enter, Backspace).
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):
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
