from django.shortcuts import render

def index(request):
    page_title = "Fourth homework"
    content = "In fourth homework we deployed django app on server using https. Tu sad jos treba doci opis sta smo radili!!!!"
    return render(request, 'hw4/landing.html', {'page_title': page_title, 'content': content})
