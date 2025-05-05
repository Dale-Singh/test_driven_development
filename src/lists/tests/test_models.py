# Import Django's base test case class for writing unit tests
from django.test import TestCase
# Import the Item and List models from the lists app to test database behavior
from lists.models import Item, List
# Import IntegrityError for catching database-level constraint violations (e.g., null fields)
from django.db.utils import IntegrityError
# Import ValidationError for catching Django-level validation issues (e.g., blank fields)
from django.core.exceptions import ValidationError

# This class allows for the creation of a temporary test database
# It verifies that items can be saved and retrieved from the database
# using Django's ORM (Object-Relational Mapper)
class ListandItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # Create a new instance (row) of the List class (table) in memory
        mylist = List()
        # Save the list to the database using Django's ORM (creates a new row)
        mylist.save()

        # Create a new instance (row) of the Item class (table) in memory
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
    
    # This test verifies that calling item.save() with no text present 
    # raises an IntegrityError - if an error is raised the test passes.
    def test_cannot_save_null_list_items(self):
        # Create a new instance (row) of the List class (table) in memory and save it to the Lists table
        mylist = List.objects.create()
        # Create a new instance (row) of the Item model (table), and assign values to the columns list and text
        item = Item(list=mylist, text=None)
        # The 'with' statement triggers the methods __enter__ and __exit__ defined inside self.assertRaises(IntegrityError).
        # __enter__ is called first and does nothing, then the indented commands are ran, followed by __exit__ which checks
        #  whether the expected IntegrityError was raised. These methods are only called when used with 'with'.
        with self.assertRaises(IntegrityError):
            item.save()
    
    def test_cannot_save_empty_list_items(self):
        mylist = List.objects.create()
        item = Item(list=mylist, text=None)
        with self.assertRaises(ValidationError):
            # .save() skips validation (e.g., for blank fields or field types) and only 
            # enforces DB constraints; .full_clean() runs all Django validations but does not save.item.full_clean()
            item.full_clean()

    def test_get_absolute(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")