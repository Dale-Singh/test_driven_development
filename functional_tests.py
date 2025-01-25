# Import the webdriver module from the Selenium library.
# This allows us to interact with web browsers through Selenium.
from selenium import webdriver

# Create an instance of the Firefox browser.
# This opens a new Firefox window controlled by Selenium.
browser = webdriver.Firefox()

# Navigate to the specified URL (localhost:8000).
# This URL points to a locally hosted server, typically used for development or testing.
browser.get("http://localhost:8000")

# Assert that the page title contains the string "Congratulations!".
# This checks if the expected content is present on the page.
# If the assertion fails, an error will be raised and the program will stop.
assert "Congratulations!" in browser.title

# If the assertion passes (the title contains "Congratulations!"),
# print "OK" to indicate that the test was successful.
print("OK")
