from django.shortcuts import redirect, render
from lists.models import Item

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for the home page
def home_page(request):
    if request.method == "POST":
        # Create a new instance (row) of the Item model, request.Post is a dictionary object
        Item.objects.create(text=request.POST["item_text"])
        # Redirect as per the PRG web development pattern
        return redirect("/")
    
    items = Item.objects.all()
    # Render the "home.html" template and return an HttpResponse object
    return render(request, "home.html", {"items": items},
    ) 
