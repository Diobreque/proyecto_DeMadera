from django.shortcuts import render

# Create your views here.

def index(request):
    data = {"imgPrincipal":"fondoPrincipal.jpg"}
    return render(request, "index.html", data)