# Django
from django.utils.html import escape  # Escapes special HTML characters to prevent injection
from django.shortcuts import redirect, render  # Utilities for rendering templates and handling redirects

# Local application
from lists.models import Item, List  # Models representing to-do items and lists
from lists.forms import ItemForm, ExistingListItemForm  # Forms for creating and validating list items


# View function for rendering the home page
def home_page(request):
    # Always pass an empty form to the home page
    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    # Retrieve the list from the database using the provided list_id
    our_list = List.objects.get(id=list_id)
    
    if request.method == "POST":
        # Bind form to submitted data and associate it with the current list
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        
        if form.is_valid():
            # Save the new item to the existing list and redirect to the same list page
            form.save()
            return redirect(our_list)
    else:
        # Re-initialize the unbound form (relevant on initial GET or failed POST)
        form = ExistingListItemForm(for_list=our_list)

    # Render the list page with the current list and form (bound or unbound)
    return render(request, "list.html", {"list": our_list, "form": form})

def new_list(request):
    # Build a form instance using POST data from the request
    form = ItemForm(data=request.POST)

    if form.is_valid():
        # Create a new List and link a new Item to it using the form
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        # On validation failure, re-render the home page with the invalid form and its errors
        return render(request, "home.html", {"form": form})
