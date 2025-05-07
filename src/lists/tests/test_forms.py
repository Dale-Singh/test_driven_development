# Import Django's base test case class for writing unit tests
from django.test import TestCase

# Import from forms.py in the lists app
from lists.forms import EMPTY_ITEM_ERROR, ItemForm

class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control form-control-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        # Create a form instance with submitted data to test validation (simulates user input)
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
