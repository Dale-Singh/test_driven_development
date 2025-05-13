# Import Django's base test case class for writing unit tests
from django.test import TestCase
# Import the form and custom error constant from the lists app
from lists.forms import EMPTY_ITEM_ERROR, ItemForm
# Import models for form-save integration tests
from lists.models import Item, List

# Tests for the ItemForm, including rendering, validation, and saving
class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        # The form should render with the correct placeholder and CSS class
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control form-control-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        # Submitting blank text should make the form invalid and show an error
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])
    
    def test_form_save_handles_saving_to_a_list(self):
        # Saving the form should create a new item linked to the specified list
        mylist = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=mylist)
        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, "do me")
        self.assertEqual(new_item.list, mylist)