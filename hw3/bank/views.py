from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, render
from django.template  import *
import ldap

from bank.models import Money

# Create your views here.

def index(request):
    return render(request, 'bank/landing.html')

@login_required
def profile(request):
    return render(request, 'bank/profile.html')

@login_required
def spend(request):

    money = None
    if request.method == 'POST':
        money = request.POST.get('money_to_spend')
    if request.method == 'GET':
        money = request.GET.get('money_to_spend')

    try:
        user_money = Money.objects.get(person=request.user)
    except:
        user_money = Money(account=500, person=request.user)

    if(money != None):
        try:
            money = int(money)
        except:
            money = 1
        user_money.account -= money
        user_money.save()
        print(user_money)

    return render(request, 'bank/spend.html', {'current': user_money.account, 'name': request.user})


@login_required
def garbage_stat_info(request):
    template = loader.get_template('stat_info.html')
    context = Context({'is_auth': str(request.user.is_authenticated())})
    return HttpResponse(template.render(context))

@login_required
def stat_info(request):
    return render_to_response('stat_info.html',
        {'is_auth':request.user.is_authenticated(), 'user':request.user},
        RequestContext(request))

@login_required
def mainmenu(request):
    return render(request, 'mainmenu.html')

    return render_to_response('mainmenu.html',{},
        context_instance=RequestContext(request))

def hacker(request):
    return render(request, 'bank/hacker.html')
