from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from SQLinjection.models import Secrets

# Create your views here.

def landing(request):
    return render(request, 'SQLinjection/landing.html')

def sql(request):
    if request.method == 'POST':
        key = request.POST.get('secret_key')
        print(key, "  ", request.POST.get('security'))
        secrets = []
        if request.POST.get('security') == 'secure':
            query_set = Secrets.objects.raw('SELECT * FROM SQLinjection_secrets WHERE name = %s', [key])
        else:
            query = 'SELECT * FROM SQLinjection_secrets WHERE name = "%s"' % key
            query_set = Secrets.objects.raw(query)
        print(query_set)
        for i in query_set:
            print("KJLK")
            secrets.append(i)
            print(i)
        return render(request, 'SQLinjection/sql.html', {'secrets': secrets, 'secret_key': key})
    else:
        return render(request, 'SQLinjection/sql.html')
