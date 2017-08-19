from django.shortcuts import render

from hw9.models import BlogColumnEncryptHW9 as Blog

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Permission, Group

from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy


def index(request):
    page_title = "Ninth homework"
    content = "Using PostgreSQL with django"
    problem1 = [('accounts', 'Create accounts using different roles for users.'), ('blog', 'Use permissions to modify users access')]
    problems = [problem1]
    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # logout(request)
        login(request, user)
        return True
    return False

def set_permissions(user, permissions):
    if 'Delete comments' in permissions:
        user.groups.add(Group.objects.get(name='hw9_moderator'))
    elif 'Modify comments' in permissions:
        user.user_permissions.add(Permission.objects.get(codename='create_post'))
        user.user_permissions.add(Permission.objects.get(codename='modifiy_post'))
    elif 'Add comments' in permissions:
        user.user_permissions.add(Permission.objects.get(codename='create_post'))
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
    set_permissions(user, request.POST.get('permissions'))
    user.save()
    return 'User with username "' + username + '" successfully registered.'

def accounts(request):
    print(request.POST)
    page_title = "Create accounts"
    login_error = False
    register_error = False
    permissions = ['Add comments', 'Modify comments', 'Delete comments']
    if(request.method == 'POST'):
        if(request.POST.get('type') == 'login'):
            login_error = not login_user(request)
        elif(request.POST.get('type') == 'register'):
            register_error = new_user(request)
    return render(request, 'hw9/create_account.html', {'page_title': page_title,
                            'login_error': login_error, 'register_error': register_error, 'permissions': permissions})

def blog(request):
    page_title = "Very fancy forum:"
    message = ''
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get('action') == 'Save' and request.user.has_perm('hw9.create_post'):
            name = request.user.username
            comment = request.POST.get('comment')
            new_comment = Blog(name=name, text=comment)
            if name is not '' and comment is not '':
                new_comment.save()
        elif request.POST.get('action') == 'Modify' and request.user.has_perm('hw9.modifiy_post'):
            comment = request.POST.get('comment_modify')
            if comment == '':
                comment = 'Default comment :)'
            try:
                old_comment = Blog.objects.get(id=request.POST.get('edit'))
                old_comment.text = comment
                old_comment.save()
            except Exception as e:
                message = 'No valid comment selected.'
        elif request.POST.get('action') == 'Delete' and request.user.has_perm('hw9.delete_post'):
            Blog.objects.filter(id=request.POST.get('edit')).delete()
    blog = Blog.objects.all()
    permissions = request.user.get_all_permissions()
    return render(request, 'hw9/blog.html', {'page_title': page_title, 'blog': blog, 'message': message, 'permissions': permissions,})
