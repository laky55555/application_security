from django.shortcuts import render

def index(request):
    page_title = "Welcome page"
    return render(request, 'base.html', {'page_title': page_title})
