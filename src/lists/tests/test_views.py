# Import Django's base test case class for writing unit tests
from django.test import TestCase
# Import Django utility to escape special HTML characters for safe rendering
from django.utils.html import escape
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

# Define a test case class that inherits from TestCase
class HomePageTest(TestCase):
    # This test checks that the root URL ("/") is correctly resolved by the application
    # It uses Django's test client to simulate an HTTP GET request to "/",
    # ensuring that the URL resolves correctly and the view returns the expected HTML response
    def test_uses_home_template(self):
        # Send a GET request to the root URL, a HttpResponse object is returned
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
    
    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        # Checks that the form returned is of type ItemForm
        self.assertIsInstance(response.context["form"], ItemForm)

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        # Django treats new_item.list as a List instance, not just an ID reference.
        # When comparing two model instances, Django automatically compares their primary keys (IDs).
        self.assertEqual(new_item.list, correct_list)

    def test_POSTS_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
    
    def test_displays_item_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertIsInstance(response.context["form"], ItemForm)
        self.assertContains(response, 'name="text"')
    
    # Helper function used in the other tests
    def post_invalid_input(self):
        mylist = List.objects.create()
        return self.client.post(f"/lists/{mylist.id}/", data={"text": ""},)
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        # Checks that upon a validation error a page is rendered successfully (200)...
        self.assertEqual(response.status_code, 200)
        # ...and that page is the lists page
        self.assertTemplateUsed(response, "list.html")
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

class NewListTest(TestCase):
    # This test checks whether a new To-Do list entry is correctly saved and displayed
    def test_can_save_a_POST_request(self):
        # URLs excluding a trailing / are action URLs, they modify the database
        self.client.post("/lists/new", data={"text": "A new list item"})
        # Verify that exactly one item has been saved in the Item table after the POST request
        self.assertEqual(Item.objects.count(), 1)
        # Select the first row in the Item table
        new_item = Item.objects.first()
        # Verify that the saved item’s text matches the submitted data
        self.assertEqual(new_item.text, "A new list item")
    
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"text": "A new list item"})
        new_list = List.objects.get()
        # Verify that a redirection occurs not the result of the redirection
        self.assertRedirects(response, f"/lists/{new_list.id}/")
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIsInstance(response.context["form"], ItemForm)
        # The view populates the homepage template with the below error message when input is invalid
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)
    
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f"/lists/{list_.id}/", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)