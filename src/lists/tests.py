from django.test import TestCase
# Import the home_page function from the lists app
from lists.views import home_page
# Import the Item and List model (tables) from the lists app
from lists.models import Item, List

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
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(F"/lists/{correct_list.id}/")
        # response.context is a dictionary like object containing data 
        # sent to the template from the view. The key "list" is accessed
        # and its value is compared against correct_list
        self.assertEqual(response.context["list"], correct_list)

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
    
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.get()
        # Verify that a redirection occurs not the result of the redirection
        self.assertRedirects(response, f"/lists/{new_list.id}/")

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        # Django treats new_item.list as a List instance, not just an ID reference.
        # When comparing two model instances, Django automatically compares their primary keys (IDs).
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
        

# This class allows for the creation of a temporary test database
# It verifies that items can be saved and retrieved from the database
# using Django's ORM (Object-Relational Mapper)
class ListandItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # Create a new instance (row) of the List model (table) in memory
        mylist = List()
        # Save the list to the database using Django's ORM (creates a new row)
        mylist.save()

        # Create a new instance (row) of the Item model (table) in memory
        first_item = Item()
        first_item.text = "The first (ever) item"
        # Specify which list this item belongs to
        first_item.list = mylist
        first_item.save()

        # Create and save a second item
        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        # Verify that both lists are the same by comparing the IDs (.id) of both lists
        self.assertEqual(saved_list, mylist)

        # Use Django's ORM API to query and retrieve all saved items from the database
        # Returns a QuerySet containing all rows in the Item table
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)


        # Retrieve the first and second items from the QuerySet (a list like collection)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        # Verify that the saved items match the original data
        self.assertEqual(first_saved_item.text,"The first (ever) item")
        # Verify that the saved items are associated to the correct list
        self.assertEqual(first_saved_item.list, mylist)

        self.assertEqual(second_saved_item.text,"Item the second")
        self.assertEqual(second_saved_item.list, mylist)


