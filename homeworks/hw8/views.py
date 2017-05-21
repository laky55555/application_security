from django.shortcuts import render

import requests
# Create your views here.

def index(request):
    page_title = "Seventh homework"
    content = "Webfinger and OpenID Connect Discovery"
    problem1 = [('webfinger', 'Query webfinger results')]
    problem2 = [('facebook', 'Using Facebook API'), ('twitter', 'Using Twitter API'), ('google', 'Using Google+ API'), ]
    problems = [problem1, problem2]
    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})
