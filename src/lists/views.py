# Import ValidationError for catching Django-level validation issues (e.g., blank fields)
from django.core.exceptions import ValidationError
# Import Django utility to escape special HTML characters for safe rendering
from django.utils.html import escape
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for rendering the home page
def home_page(request):
    # Render the "home.html" template with the form and return an HttpResponse
    return render(request, "home.html", {'form': ItemForm()})

def view_list(request, list_id):
    # Retrieve the list from the database using the provided list_id
    our_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            # Create a new Item instance (not saved yet) and validate it
            item = Item(text=request.POST['item_text'], list=our_list)
            item.full_clean()
            item.save()
            # Redirect to the list page after successfully saving the item
            return redirect(our_list)
        except ValidationError:
            # If validation fails, set the error message (escaped for HTML safety)
            error = escape("You can't have an empty list item")

    # Render the list page, passing in the list and any error messages
    return render(request, "list.html", {"list": our_list, 'error': error})

def new_list(request):
    # Create a new List instance and save it to the database
    nulist = List.objects.create()

    # Create a new Item instance linked to the new list (not saved yet)
    item = Item(text=request.POST["item_text"], list=nulist)

    try:
        # Validate the item before saving
        item.full_clean()
        item.save()
    except ValidationError:
        # If validation fails, delete the new list to avoid saving empty lists
        nulist.delete()
        # Set the error message and re-render the home page with the error
        error = escape("You can't have an empty list item")
        return render(request, "home.html", {"error": error})

    # On successful save, redirect to the new list page following PRG pattern
    return redirect(nulist)
