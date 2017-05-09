from django.shortcuts import render
from social_django.admin import UserSocialAuth

import requests
# Create your views here.

def index(request):
    page_title = "Seventh homework"
    content = "Using OAuth2 from popular social networks"# + '/home/ivan/Dropbox/Faks/5_godina/application_security/homeworks'
    problem1 = [('login', 'Create a simple server-side web application that uses OAuth2 from popular sites for login.')]
    problem2 = [('facebook', 'Using Facebook API'), ('twitter', 'Using Twitter API'), ('google', 'Using Google+ API'), ]
    problems = [problem1, problem2]
    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})

def login(request):
    page_title = "Login via social networks"
    providers = []
    if request.user.is_authenticated():
        providers = list(UserSocialAuth.objects.filter(user=request.user).values_list('provider', flat=True))
    explanation = [('Account linked to:', providers),
                    ('Facebook', ['<a href="/login/facebook?next=/hw7">Login via facebook</a>',
                                    'Specificy what permissions you want to get in settings: SOCIAL_AUTH_FACEBOOK_SCOPE = ["email", "user_photos"]']),
                    ('Google', ['<a href="/login/google-oauth2?next=/hw7">Login via google</a>']),
                    ('Twitter', ['<a href="/login/twitter?next=/hw7">Login via twitter [NOT IN YET IN USE]</a>']),
                    ('Slack', ['<a href="/login/slack?next=/hw7">Login via slack</a>',]),
                    ('Note', ['Add backends of API-s you want to use in backend tuple (setting.py)',
                                'Add keys (secret and public) of backed',
                                'Add pipelanes; info and specification of new users you want to get and import into database)',
                                'Using pipeline associate_by_email just with services that check email. If they don\'t check it -> <a href="http://python-social-auth.readthedocs.io/en/latest/configuration/django.html">security risk</a>.'])]
    return render(request, 'base.html', {'page_title': page_title, 'explanation': explanation})

def get_data_from_facebook(url, token):
    response = requests.get(url, params={'access_token': token}).json()
    data = response.get('data')
    next = response.get('paging').get('next')
    return (data, next)

def facebook(request):
    page_title = "Playing with Facebook API"
    providers = []
    friend_list = my_albums = latest_posts = False

    if request.user.is_authenticated():
        providers = list(UserSocialAuth.objects.filter(user=request.user).values_list('provider', flat=True))

        user = UserSocialAuth.objects.filter(provider='facebook', user=request.user).first()
        if request.method == 'POST' and user and not user.access_token_expired() and request.POST.get('usage') in {'posts', 'albums', 'taggable_friends'}:
            usage = request.POST.get('usage')
            url = 'https://graph.facebook.com/v2.9/' + user.uid
            if usage == 'posts':
                latest_posts, next = get_data_from_facebook(url +'/feed?fields=picture,message,permalink_url,created_time', user.access_token)
            elif usage == 'albums':
                my_albums, next = get_data_from_facebook(url +'/albums?fields=count,link,name,photo_count,picture', user.access_token)
            elif usage == 'taggable_friends':
                friend_list, next = get_data_from_facebook(url + '/taggable_friends?fields=picture.width(300),name', user.access_token)

    return render(request, 'hw7/facebook.html', {'page_title': page_title, 'providers': providers, 'friend_list': friend_list, 'my_albums': my_albums, 'latest_posts': latest_posts})

def twitter(request):
    a = 2
def google(request):
    a = 2
