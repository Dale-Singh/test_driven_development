# Third-party (Selenium)
from selenium.webdriver.common.by import By  # Strategies for locating elements on a web page
from selenium.webdriver.common.keys import Keys  # Simulate keyboard input (e.g., Enter, Backspace)

# Local application
from functional_tests.base import FunctionalTest  # Base class for shared functional test setup

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)

        # Her brwoser window is set to a particular size
        self.browser.set_window_size(1024,768)

        # She notices the inbox is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )

        # She starts a new list and and sees the input is nicely centered too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )
