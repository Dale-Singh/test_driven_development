from django.test import TestCase
# Import the home_page function from the lists app
from lists.models import Item, List

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