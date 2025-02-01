from django.shortcuts import render
# Imports the HttpResponse class
from django.http import HttpResponse

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for the home page
def home_page(request):
    # Render the "home.html" template and return an HttpResponse object
    return render(
        request,
        "home.html",
        # request.Post is a dictionary object, dict.get() is used when POST is empty
        {"new_item_text": request.POST.get("item_text","")},
    ) 
