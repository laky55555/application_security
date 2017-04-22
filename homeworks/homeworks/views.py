from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

import os

def home(request):
    return redirect(reverse_lazy('index'))

def index(request):
    page_title = "Welcome page"
    return render(request, 'base.html', {'page_title': page_title})
