from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.conf import settings

from hw6.models import Blog

from django import forms
from captcha.fields import ReCaptchaField

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

import hashlib, binascii

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(attrs={'theme' : 'clean',})

def index(request):
    page_title = "Sixth homework"
    content = "Authentication, CAPTCHA"# + '/home/ivan/Dropbox/Faks/5_godina/application_security/homeworks'
    problem1 = [('s_key', 'Explain and a show demo for S/KEY authentication.'),
                ('s_key_generate', 'Short explanation + S/KEY generation'),]
    problem2 = [('captcha', 'Prepare an example of applying CAPTCHA.')]
    problems = [problem1, problem2]
    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})

def check_captcha(request):
    captcha_version = ('g-recaptcha-response' if getattr(settings, 'NOCAPTCHA', False) else 'recaptcha_response_field')
    # print (captcha_version, request.POST)
    form_params = {captcha_version: request.POST.get(captcha_version)}
    form = FormWithCaptcha(form_params)
    return form.is_valid()


def captcha(request):
    content = "Very fancy forum:"
    error = ''
    if request.method == 'POST':
        if check_captcha(request):
            name = request.POST.get('name')
            comment = request.POST.get('comment')
            new_comment = Blog(name=name, text=comment)
            if name is not '' and comment is not '':
                new_comment.save()
        else:
            error = 'Captcha not solved correctly.'

    page_title = "noCAPTCHA"
    blog = Blog.objects.all()
    captcha = FormWithCaptcha()
    explanation = [('Library', ['We are using <a href="https://github.com/praekelt/django-recaptcha">pip install django-recaptcha</a> library.']),
                    ('Usage', ['First: Add "captcha" to INSTALLED_APPS',
                                'Second: Make account on <a href="https://www.google.com/recaptcha/admin">google</a> for using captcha and get keys.',
                                'Third: Put given keys into settings.py with following names: RECAPTCHA_PUBLIC_KEY = "pub" and RECAPTCHA_PRIVATE_KEY = "priv"',
                                'Fourth: In post you want to use captcha put captcha form (see code)',
                                'Fifth: To verify if captcha is filled use correct name form (reCAPTCHA/noCAPTCHA) and library function is_valid()']),
                    ('Note', ['If you want to use noCAPTCHA put into settings.py => NOCAPTCHA = True'])]
    return render(request, 'hw6/captcha.html', {'page_title': page_title, 'content': content, 'blog': blog, 'captcha': captcha, 'error': error, 'explanation': explanation})

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False

def new_user(request):
    username = request.POST['username']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']
    if(password != password_confirm):
        return "Your passwords didn't match. Please try again."
    try:
        user = User.objects.create_user(username=username)
    except Exception as e:
        return 'User with username "' + username + '" already exist.'
    user.set_password(password)
    user.save()
    return 'User with username "' + username + '" successfully registered.'

def s_key(request):
    page_title = "S/KEY authentication"
    hint = ""
    login_error = False
    register_error = False
    if not request.user.is_authenticated():
        if(request.method == 'POST'):
            if(request.POST.get('type') == 'login'):
                login_error = not login_user(request)
            elif(request.POST.get('type') == 'register'):
                register_error = new_user(request)

    link = reverse('hw6:s_key_generate')
    explanation = [('Note', ['For True S/KEY authentication you need to DISABLE default django authentication service in settings.py AUTHENTICATION_BACKENDS.']),
                    ('S/KEY', ['<a href="https://en.wikipedia.org/wiki/S/KEY">S/KEY</a> is a one-time password system developed for authentication.',
                    'S/KEY works on principle that for hashed string it\'s very hard problem to find started, unhashed value.',
                    'It\'s good replacement for loging on unencrypted networks because even if someone see our password there is no value in it anymore.']),
                    ('Initialization', ['Server or user create secret key and hashes (better if user do it like in out example)',
                                'If server create key/hashes user need to get them somehave, a bit more insecure.',
                                'After user <a href="' + link + '">creates n hash keys</a> from begining key she gives last one (n-th) to server.',
                                'User and server knows with which method will hashing be done.']),
                    ('Usage', ['Server has one key (at start last one), and <b>user has them all saved</b>',
                                'When user wants to log in she send to server last key that she didn\'t used so far (at start (n-1)-th)',
                                'Server for cheching validity of the key first execute hash function onto given key and then it check if given value is the same like one in memory.',
                                'If password matches, we log in user, and save password that user sent us for later use so next time she needs to use new one.']),
                    ('Login backend', ['For logging we did <a href="https://docs.djangoproject.com/en/1.11/topics/auth/customizing/">custom backend</a>.',
                                        'For django to use our backend you need to put it in AUTHENTICATION_BACKENDS in settings.py'
                                        'When user register, we save it in database with default users.',
                                        'When user wants to log in, if user exist we hash given password and check if it matches.'])]

    return render(request, 'hw6/s_key.html', {'page_title': page_title, 'hint': hint, 'login_error': login_error, 'register_error': register_error, 'explanation': explanation})

def s_key_generate(request):
    page_title = "Generate hashed keys."
    content = "Helper for generating hashed keys."
    keys = []
    if(request.method == 'POST'):
        try:
            keyword = request.POST.get('keyword').encode('ascii')
            iterations = int(request.POST.get('number'))
        except Exception as e:
            keyword = b'Error in POST'
            iterations = 10
        for i in range(iterations):
            print(i)
            hashed = hashlib.pbkdf2_hmac('sha256', keyword, b'salt', 100000)
            keys.append((keyword, binascii.hexlify(hashed)))
            keyword = binascii.hexlify(hashed)
    explanation = [('Generating hash keys', ['We use this page for generate n hashes from first key word.',
                                            'We make hash from the first given string, and then we hash value received from hash function and that n times.',
                                            'H(key), H(H(key)), ..., Hn(key).',
                                            'For hashing we use <a href="https://docs.python.org/3/library/hashlib.html">hashlib</a> library and pbkdf2_hmac function.',
                                            'For digest algorithm for HMAC we use sha256, salt and 100,000 iterations'])]

    return render(request, 'hw6/s_key_generate.html', {'page_title': page_title, 'content': content, 'keys': keys, 'explanation': explanation})
