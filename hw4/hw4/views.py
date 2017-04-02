from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You are at very safe page!")

def test(request):
    return HttpResponse("Hello, world. You are at very safe page!")
