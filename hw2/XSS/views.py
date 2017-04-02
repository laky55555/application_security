from django.http import HttpResponse
from django.shortcuts import render
from XSS.models import Blog

# Create your views here.

def index(request):
    return render(request, 'XSS/landing.html')

def reflected(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        return render(request, 'XSS/reflected.html', {'name': name, 'security': request.GET.get('security')})
    else:
        return render(request, 'XSS/reflected.html')

def stored(request):
    if request.method == 'POST':
        comment = Blog(text=request.POST.get('comment'))
        comment.save()
    if request.method == 'GET':
        query_set = Blog.objects.all()
        comments = [i for i in query_set]
        print(comments)
        return render(request, 'XSS/stored.html', {'comments': comments, 'security': request.GET.get('security')})

    return render(request, 'XSS/stored.html')

def dom(request):
    return HttpResponse('''Select your favorite number: <select><script>
            document.write("<OPTION value=1>12</OPTION>");
            document.write("<OPTION value=2>34</OPTION>");
            document.write("<OPTION value=3>"+eval(document.location.href.substring(document.location.href.indexOf("default=")+8))+"</OPTION>");
            </script></select>
            <br>
            <br>
            <h4>Try following link:</h4>
            <a href="/xss/dom#default=alert(document.cookie)">XSS DOM</a>''')
    # return render(request, 'SQLinjection/landing.html')


def x_xss_protection_header(request):
    return render(request, 'XSS/protection-header.html')
