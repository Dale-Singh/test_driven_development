# Import the TestCase class for creating test cases
from django.test import TestCase
# Import the HttpRequest class for simulating HTTP requests
from django.http import HttpRequest
# Import the home_page function from the views script in the lists app
from lists.views import home_page

# Define a test case class that inherits from TestCase
class HomePageTest(TestCase):
    # This test checks that the root URL ("/") is correctly resolved by the application.
    # It uses Django's test client to simulate an HTTP GET request to "/",
    # ensuring that the URL resolves correctly and the view returns the expected HTML response.
    def test_uses_home_template(self):
        # Send a GET request to the root URL
        response = self.client.get("/")
        # Apply assertions to verify the HTML content
        self.assertTemplateUsed(response, "home.html")
