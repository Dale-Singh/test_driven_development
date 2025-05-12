from django import forms
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
    