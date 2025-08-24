# Standard library
from unittest import skip  # Temporarily skip tests while keeping them in the suite

# Django
from django.test import TestCase  # Base test case class for writing unit tests
from django.utils.html import escape  # Escapes special HTML characters for safe rendering

# Local application
from lists.models import Item, List  # Models under test from the 'lists' app
from lists.forms import (  # Forms and error messages for list item input and validation
    ItemForm,
    ExistingListItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
)


# Tests for the home page
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        # GET request to root URL should use the home template
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
    
    def test_home_page_uses_item_form(self):
        # Home page context should include an ItemForm
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)

# Tests for existing list pages and form behavior
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
        # The view should pass the correct list object to the template
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        # Submits a new item to a specific list and checks that it's saved correctly
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POSTS_redirects_to_list_view(self):
        # After a valid POST, the user is redirected back to the list page
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
    
    def test_displays_item_form(self):
        # Form is rendered on the list page with expected input field
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
    
    # Helper method for submitting invalid input to a list
    def post_invalid_input(self):
        mylist = List.objects.create()
        return self.client.post(f"/lists/{mylist.id}/", data={"text": ""})
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        # Submitting blank text should not create a new item
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_list_template(self):
        # Invalid input should render the list template again
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")
    
    def test_for_invalid_input_passes_form_to_template(self):
        # The invalid form is passed back to the template for error display
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):
        # Validation error message should be rendered in the response
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text="textey")
        response = self.client.post(
            f"/lists/{list1.id}/",
            data={"text": "textey"},
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)

# Tests for creating new lists
class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        # A POST request to /lists/new should save a new item
        self.client.post("/lists/new", data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
    
    def test_redirects_after_POST(self):
        # After saving a new list, redirect to its list page
        response = self.client.post("/lists/new", data={"text": "A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        # Submitting blank text on the home page should show error
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIsInstance(response.context["form"], ItemForm)
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)
    
    def test_validation_errors_end_up_on_lists_page(self):
        # Submitting blank text on an existing list should show error
        list_ = List.objects.create()
        response = self.client.post(f"/lists/{list_.id}/", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        # No new list or item should be created for blank input
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

# Tests for the "My lists" page that shows lists belonging to a specific user
class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")
