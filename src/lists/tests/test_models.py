# Django
from django.test import TestCase  # Base test case class for writing unit tests
from django.db.utils import IntegrityError  # Raised for database-level constraint violations (e.g., null values)
from django.core.exceptions import ValidationError  # Raised for Django-level validation issues (e.g., blank fields)

# Local application
from accounts.models import User
from lists.models import Item, List

# Tests for the List and Item models and their interactions
class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text,"")

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item()
        item.list = mylist
        item.save()
        self.assertIn(item, mylist.item_set.all())

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
    
    def test_list_ordering(self):
        # Items should be ordered by ID by default, as specified in the model's Meta class
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )
    
    def test_string_representation(self):
        # The string representation of an Item should return its text
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")

class ListandModelTest(TestCase):
    def test_get_absolute_url(self):
        # Verifies that the model's URL is correctly generated
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")
    
    def test_lists_can_have_owners(self):
        # Verifies that a list is associated to a User
        user = User.objects.create(email="a@b.com")
        mylist = List.objects.create(owner=user)
        self.assertIn(mylist, user.lists.all())
    
    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise
    
    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="first item")
        Item.objects.create(list=list_, text="second item")
        self.assertEqual(list_.name, "first item")