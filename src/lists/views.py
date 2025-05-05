from django.shortcuts import redirect, render
from lists.models import Item, List
# Import ValidationError for catching Django-level validation issues (e.g., blank fields)
from django.core.exceptions import ValidationError
# Import Django utility to escape special HTML characters for safe rendering
from django.utils.html import escape

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for the home page
def home_page(request):
    # Render the "home.html" template and return an HttpResponse object
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    # The list id is passed to the template, the template then accesses the related items using list.item_set.all
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    # Create a new instance (row) of the List model (table)
    nulist = List.objects.create()
    # Create a new instance (row) of the Item model (table), request.Post is a dictionary object
    item = Item(text=request.POST["item_text"], list=nulist)
    try:
        # Checks for validation and DB constraint violations, stopping the code if one is found
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        error = escape("You can't have an empty list item")
        return render(request, "home.html", {"error": error})
    # Redirect as per the PRG web development pattern
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")
