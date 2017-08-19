from django.shortcuts import render
# import ldap as ld
# from django_auth_ldap.config import LDAPSearch



# Create your views here.

def index(request):
    return render(request, 'hw5/landing.html')

# def ldap(request):
#     ld.SCOPE_SUBTREE
#     AUTH_LDAP_SERVER_URI = 'ldap://homework5.mutiny.codes:389'
#     AUTH_LDAP_BIND_DN = "cn=admin,dc=homework5,dc=mutiny,dc=codes"
#     AUTH_LDAP_BIND_PASSWORD = 'Ivan1357'
#     AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=mutiny,dc=codes", ld.SCOPE_SUBTREE, "uid=1001")
#     print(AUTH_LDAP_USER_SEARCH)
#     return render(request, 'hw5/landing.html')
