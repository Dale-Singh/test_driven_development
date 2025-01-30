from django.shortcuts import render

# All Django views must accept a request object, even if not used
# The request object contains data about the HTTP request, which can be useful later

# View function for the home page
def home_page(request):
    # Render the "home.html" template and return an HTTP response object
    return render(request, "home.html")
