from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

# Use ModelForm to automatically create form fields from the Item model
# and handle validation and saving without having to manuallly define input fields.
class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        """
        Saves the form's Item instance to the database, assigning it to the given list.
        This form is a ModelForm linked to the Item model, and this method ensures
        that the required 'list' foreign key is set before saving.
        """
        # Assign the provided list to the form's Item model instance before saving
        self.instance.list = for_list
        # Call the parent ModelForm save method to save the item to the database
        return super().save()

    # Django searches for this Meta class it is used to 
    # link the form to the Item model and specifies the fields to include
    class Meta:
        model = Item
        fields = ('text',)
        # Customise form fields to modify their HTML attributes and appearance
        widgets = {
            'text': forms.widgets.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control form-control-lg',
                }
            ),
        }
        # Override default custom validation error messages
        error_messages = {'text': {'required': EMPTY_ITEM_ERROR}}

DUPLICATE_ITEM_ERROR =  "You've already got this in your list"

# A custom form for adding items to an existing list, with duplicate validation
class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        # Store the list this form is associated with
        self.for_list = for_list
        # Call the parent constructor to handle standard form setup (e.g. data binding)
        super().__init__(*args, **kwargs)
        # Link the form's model instance to the provided list
        self.instance.list = for_list

    def validate_unique(self):
        # Override default unique validation to customize the error message
        try:
            # Run the model-level unique check (e.g. for unique_together constraints)
            self.instance.validate_unique()
        except ValidationError as e:
            # Replace the default error with a custom duplicate item message
            e.error_dict = {"text": [DUPLICATE_ITEM_ERROR]}
            # Attach the updated error to the form's internal error collection
            self._update_errors(e)


    
    