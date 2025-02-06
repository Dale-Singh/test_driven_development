from django.shortcuts import redirect, render
from lists.models import Item, List

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for the home page
def home_page(request):
    # Render the "home.html" template and return an HttpResponse object
    return render(request, "home.html")

def view_list(request):
    items = Item.objects.all()
    # The key "items" specified here is linked to the variable items in the home.html template,
    # It passes the QuerySet 'items' above which is used to populate the table dynamically.
    return render(request, "list.html", {"items": items})

def new_list(request):
    # Create a new instance (row) of the List model (table)
    nulist = List.objects.create()
    # Create a new instance (row) of the Item model (table), request.Post is a dictionary object
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    # Redirect as per the PRG web development pattern
    return redirect("/lists/the-only-list-in-the-world/")
