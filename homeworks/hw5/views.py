from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import template
# Good for signing/verifying signature. Easy for loading keys/certificates.
import OpenSSL
# Good for encryption/decryption. Easy to transfer keys from OpenSSL to cryptography data types.
# Not good for importing certificates.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import os
from django.conf import settings


def index(request):
    page_title = "Fifth homework"
    content = "In fifth homework we had 2 problems." + '/home/ivan/Dropbox/Faks/5_godina/application_security/homeworks'
    return render(request, 'hw5/landing.html', {'page_title': page_title, 'content': content})

def open_certificate(path, relative=True):
    if(relative):
        # path = os.path.join(settings.BASE_DIR, path)
        path = os.path.join('/home/ivan/Dropbox/Faks/5_godina/application_security/homeworks', path)
    open_file = open(path, 'r')
    certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open_file.read())
    open_file.close()
    return certificate

def load_keys():
    open_fourth = open(os.path.join(settings.BASE_DIR, 'hw4/certificates/fourthhwkey.pem'), 'r')
    pass_fourth = 'fourthhwkey'.encode('ascii')
    fourth = OpenSSL.crypto.load_privatekey(type=OpenSSL.crypto.FILETYPE_PEM, buffer=open_fourth.read(), passphrase=pass_fourth)
    open_fifth = open(os.path.join(settings.BASE_DIR, 'hw4/certificates/fifthhwkey.pem'), 'r')
    pass_fifth = 'fifthhwkey'.encode('ascii')
    fifth = OpenSSL.crypto.load_privatekey(type=OpenSSL.crypto.FILETYPE_PEM, buffer=open_fifth.read(), passphrase=pass_fifth)
    open_fourth.close()
    open_fifth.close()
    return fourth, fifth


def read_local(request):
    cert_homework = open_certificate('hw4/certificates/fourthhwcert.pem', True)
    cert_hogwarts = open_certificate('hw4/certificates/fifthhwcert.pem')
    cert_info = [[], []]
    for i, j in cert_homework.get_subject().get_components():
        cert_info[0].append(j)
    cert_info[0].append(cert_homework.get_signature_algorithm())
    for i, j in cert_hogwarts.get_subject().get_components():
        cert_info[1].append(j)
    cert_info[1].append(cert_hogwarts.get_signature_algorithm())
    page_title = "Fifth homework - reading keys/certificates"
    return render(request, 'hw5/show_keys_certs.html', {'page_title': page_title, 'cert_info': cert_info})



def read_central(request):
    certum = open_certificate('/etc/ssl/certs/Certum_Root_CA.pem', False)
    certum2 = open_certificate('/etc/ssl/certs/Certum_Trusted_Network_CA.pem', False)
    comodo = open_certificate('/etc/ssl/certs/COMODO_Certification_Authority.pem', False)
    names = ['Certum_Root_CA.pem', 'Certum_Trusted_Network_CA.pem', 'COMODO_Certification_Authority.pem']
    data = [certum.get_subject().get_components(), certum2.get_subject().get_components(), comodo.get_subject().get_components()]
    zipped = zip(names, data)
    page_title = "Fifth homework"
    return render(request, 'hw5/firefox_certs.html', {'page_title': page_title, 'zipped': zipped})



def encrypt_decrypt(request):
    # Load certificates and PKeys from files.
    cert_homework = open_certificate('hw4/certificates/fourthhwcert.pem')
    cert_hogwarts = open_certificate('hw4/certificates/fifthhwcert.pem')

    privat_homework, privat_hogwarts = load_keys()

    # Get RSA public keys from certificates
    public_homework = cert_homework.get_pubkey().to_cryptography_key()
    public_hogwarts = cert_hogwarts.get_pubkey().to_cryptography_key()

    # Message to encrypt and padding using for encryption.
    message = "Secret spell needed to do for homework."
    message_asci = message.encode('ascii')
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#encryption
    used_padding = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None)
    # Encrypting message with reciever public key.
    encrypted = public_hogwarts.encrypt(message_asci, used_padding)
    # Signing message with our private key
    signature = OpenSSL.crypto.sign(privat_homework, encrypted, "sha256")
    # Reciever first verify that message is from targeted sender.
    try:
        OpenSSL.crypto.verify(cert_homework, signature, encrypted, 'sha256')
        verify = "Signature verified"
    except Exception as e:
        verify = "Signature NOT correct!!!"
    # Reciever decrypt message with his private key. First need to get RSA private key from loaded key.
    try:
        decrypted = privat_hogwarts.to_cryptography_key().decrypt(encrypted, used_padding)
    except Exception as e:
        decrypted = 'Decryption FAILED!'
    data = [('message', message), ('encrypted (hex)', encrypted.hex()[0:60]+'....'), ('signature (hex)', signature.hex()[0:60]+'....'), ('verify', verify), ('decrypted', decrypted)]

    page_title = "Fifth homework - encrypting/decrypting"
    return render(request, 'hw5/encrypting.html', {'page_title': page_title, 'data': data})
