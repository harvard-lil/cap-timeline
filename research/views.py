from django.shortcuts import render

# Create your views here.


def index(request):
    print("hello index.html")
    return render(request, "index.html")