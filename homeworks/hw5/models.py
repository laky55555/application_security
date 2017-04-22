from django.db import models
import os
import OpenSSL
from django.conf import settings
import ldap

ldap_server='homework5.mutiny.codes'



def read_certificate(path, relative=True):
    if(relative):
        path = os.path.join(settings.BASE_DIR, path)
        # path = os.path.join(
        #     '/home/ivan/Dropbox/Faks/5_godina/application_security/homeworks', path)
    open_file = open(path, 'r')
    certificate = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, open_file.read())
    open_file.close()
    return certificate

def read_secret_key(path, password):
    open_file = open(os.path.join(settings.BASE_DIR, path), 'r')
    password = password.encode('utf-8')
    key = OpenSSL.crypto.load_privatekey(
        type=OpenSSL.crypto.FILETYPE_PEM, buffer=open_file.read(), passphrase=password)
    return key

def check_LDAP_credentials(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user_dn = "uid="+username+',ou=users,dc=homework5,dc=mutiny,dc=codes'
    base_dn = "dc=homework5,dc=mutiny,dc=codes"
    connect = ldap.open(ldap_server)

    search_filter = "uid="+username
    try:
    	#if authentication successful, get the full user data
    	connect.bind_s(user_dn,password)
    	result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
    	# return all user data results
    	connect.unbind_s()
    	return (1, result[0][1])
    except ldap.LDAPError as e:
        connect.unbind_s()
        return (-1, "Authentication error")

def search_LDAP_user(request):
    connect = ldap.open(ldap_server)
    attributes = request.POST.get('attributes')
    if attributes:
        attributes = attributes.replace(" ", "").split(',')

    search_filter = request.POST.get('filter')
    if not search_filter:
        search_filter = 'objectClass=*'

    scope = request.POST.get('scope')
    try:
        scope = int(scope)
        if scope not in range(4):
            raise
    except Exception as e:
        scope = ldap.SCOPE_SUBTREE

    base_dn = "dc=homework5,dc=mutiny,dc=codes"

    try:
    	result = connect.search_s(base_dn, scope, search_filter, attributes)
    	connect.unbind_s()
    	return result
    except ldap.LDAPError as e:
    	connect.unbind_s()
    	return 0
