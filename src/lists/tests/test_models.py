# Import Django's base test case class for writing unit tests
from django.test import TestCase
# Import the Item and List models from the lists app to test database behavior
from lists.models import Item, List
# Import IntegrityError for catching database-level constraint violations (e.g., null fields)
from django.db.utils import IntegrityError
# Import ValidationError for catching Django-level validation issues (e.g., blank fields)
from django.core.exceptions import ValidationError

# Tests for the List and Item models and their interactions
class ListandModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text,"")

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item()
        item.list = mylist
        item.save()
        self.assertIn(item, mylist.item_set_all())

    def test_cannot_save_null_list_items(self):
        # Attempting to save an item with text=None should raise a database-level error
        mylist = List.objects.create()
        item = Item(list=mylist, text=None)
        with self.assertRaises(IntegrityError):
            item.save()

    def test_cannot_save_empty_list_items(self):
        # Django-level validation should raise a ValidationError for blank text
        mylist = List.objects.create()
        item = Item(list=mylist, text=None)
        with self.assertRaises(ValidationError):
            # .full_clean() runs model validation but does not save the object
            item.full_clean()
    
    def test_duplicate_items_are_invalid(self):
        mylist = List.objects.create()
        Item.objects.create(list=mylist, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=mylist, text="bla")
            item.full_clean()
    
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean() # should not raise

class ListandModelTest(TestCase):
    def test_get_absolute_url(self):
        # Verifies that the model's URL is correctly generated
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")