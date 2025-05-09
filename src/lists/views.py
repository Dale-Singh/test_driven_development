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

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()
    return render(request, "list.html", {"list": our_list, "form": form})

def new_list(request):
    # Create a form by passing in data from the post request
    form = ItemForm(data=request.POST)

    if form.is_valid():
        # Create a new List instance and save it to the database
        nulist = List.objects.create()
        # Create a new Item instance linked to the new list
        Item.objects.create(text=request.POST["text"], list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})
