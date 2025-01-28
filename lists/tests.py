# Import the TestCase class for creating test cases
from django.test import TestCase
# Import the HttpRequest class for simulating HTTP requests
from django.http import HttpRequest
# Import the home_page function from the views script in the lists app
from lists.views import home_page

# Define a test case class that inherits from TestCase
class HomePageTest(TestCase):
    # Define a test method to check if the home_page view returns the correct HTML
    def test_home_page_returns_correct_html(self):
        # Create an instance of HttpRequest to simulate a request
        request = HttpRequest()
        # Call the home_page view with the simulated request
        response = home_page(request)
        # Decode the response content to extract the HTML
        html = response.content.decode("utf8")

        # Apply assertions to verify the HTML content
        self.assertIn("<title>To-Do lists</title>", html)  # Check for the correct title
        self.assertTrue(html.startswith("<html>"))        # Check if it starts with <html>
        self.assertTrue(html.endswith("</html>"))         # Check if it ends with </html>
