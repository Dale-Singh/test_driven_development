from django.test import TestCase
from django.http import HttpRequest
# Import the home_page function from the lists app
from lists.views import home_page
# Import the Item model (table) from the lists app
from lists.models import Item

# Define a test case class that inherits from TestCase
class HomePageTest(TestCase):
    # This test checks that the root URL ("/") is correctly resolved by the application
    # It uses Django's test client to simulate an HTTP GET request to "/",
    # ensuring that the URL resolves correctly and the view returns the expected HTML response
    def test_uses_home_template(self):
        # Send a GET request to the root URL, a HttpResponse object is returned
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

class NewListTest(TestCase):
    # This test checks whether a new To-Do list entry is correctly saved and displayed
    def test_can_save_a_POST_request(self):
        # URLs excluding a trailing / are action URLs, they modify the database
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        # Verify that exactly one item has been saved in the Item table after the POST request
        self.assertEqual(Item.objects.count(), 1)
        # Select the first row in the Item table
        new_item = Item.objects.first()
        # Verify that the saved item’s text matches the submitted data
        self.assertEqual(new_item.text, "A new list item")
    
    def test_redirects_a_POST_request(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        # Verify that a redirection occurs not the result of the redirection
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")

# This class allows for the creation of a temporary test database
# It verifies that items can be saved and retrieved from the database
# using Django's ORM (Object-Relational Mapper)
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # Create a new instance (row) of the Item model (table) 
        first_item = Item()
        first_item.text = "The first (ever) item"
        # Save the item to the database using Django's ORM (creates a new row)
        first_item.save()

        # Create and save a second item
        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        # Use Django's ORM API to query and retrieve all saved items from the database
        # Returns a QuerySet containing all rows in the Item table
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)


        # Retrieve the first and second items from the QuerySet (a list like collection)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        # Verify that the saved items match the original data
        self.assertEqual(first_saved_item.text,"The first (ever) item")
        self.assertEqual(second_saved_item.text,"Item the second")


