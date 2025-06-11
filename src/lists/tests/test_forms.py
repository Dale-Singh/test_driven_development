# Django
from django.test import TestCase # Base test case class for writing unit tests

# Local application
from lists.models import Item, List # Models under test from the 'lists' app
from lists.forms import ( # Forms and error messages for handling list item input
    ItemForm,
    ExistingListItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
)

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

# Tests for ExistingListItemForm, including rendering and custom validation for duplicates
class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        # The form should render with the correct placeholder when bound to a list
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        # Submitting blank text should make the form invalid and show the appropriate error
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])
    
    def test_form_validation_for_duplicate_items(self):
        # Submitting a duplicate item for the same list should make the form invalid
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="no twins!")
        form = ExistingListItemForm(for_list=list_, data={"text": "no twins!"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [DUPLICATE_ITEM_ERROR])
    
    def test_form_save(self):
        # Saving the form should create and return a new item linked to the given list
        mylist = List.objects.create()
        form = ExistingListItemForm(for_list=mylist, data={"text": "hi"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
