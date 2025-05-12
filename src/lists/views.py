# Import Django exceptions and utilities
from django.utils.html import escape  # Escapes HTML to prevent rendering special characters
from django.shortcuts import redirect, render  # For rendering templates and redirecting after POSTs

# Import models and forms from the lists app
from lists.models import Item, List
from lists.forms import ItemForm

# View function for rendering the home page
def home_page(request):
    # Always pass an empty form to the home page
    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    # Retrieve the list from the database using the provided list_id
    our_list = List.objects.get(id=list_id)

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            # The form creates a new Item instance, links it to the list, and saves it to the database
            form.save(for_list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()

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
