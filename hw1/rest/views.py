from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import hashlib
import os
from time import time

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5


# Create your views here.

def test_hash(hash_func, test_string):
    start = time()
    for i in range(1000):
        hash_func.update(test_string)
    return time()-start

def test_pbkdf2_hmac(test_string, salt, iterations):
    start = time()
    for i in range(1000):
        hashlib.pbkdf2_hmac('sha256', test_string, salt, iterations)
    return time()-start

def index(request):
    return render(request, 'rest/landing.html')

def third(request):
    test_string = "Some very long string! :)"
    while len(test_string) < 1000000:
        test_string += "; " + test_string

    test_string = test_string.encode('UTF-8')
    salt = os.urandom(16)
    names = ['md5', 'sha1', 'sha512', 'ripemd160', 'pbkdf2_hmac 1000', 'pbkdf2_hmac 10000']
    times = []
    times.append(test_hash(hashlib.md5(), test_string))
    times.append(test_hash(hashlib.sha1(), test_string))
    times.append(test_hash(hashlib.sha512(), test_string))
    times.append(test_hash(hashlib.new('ripemd160'), test_string))
    times.append(test_pbkdf2_hmac(test_string, salt, 1000))
    times.append(test_pbkdf2_hmac(test_string, salt, 10000))

    zipped = zip(times, names)
    table = sorted(zipped, key=lambda zipped: zipped[0])

    return render(request, 'rest/third.html', {'times': times, 'table': table, 'string_length': len(test_string)})

def fifth(request):

    if request.method == 'POST':
        igor_message = request.POST.get('igor_message')
        tina_message = request.POST.get('tina_message')
        if igor_message is None:
            igor_message = "This is defaut Igor's message."
        if tina_message is None:
            tina_message = "This is defaut Tina's message."

        igor_message = igor_message.encode('UTF-8')
        tina_message = tina_message.encode('UTF-8')
        KEY_LENGTH = 1024
        random_gen = Random.new().read

        # Generate RSA private/public key pairs for both parties...
        key_tina = RSA.generate(KEY_LENGTH, random_gen)
        key_igor = RSA.generate(KEY_LENGTH, random_gen)

        # Public key export for exchange between parties...
        public_tina = key_tina.publickey()
        public_igor = key_igor.publickey()

        # Plain text messages...

        # Generate digital signatures using private keys...
        hash_of_igor_message = MD5.new(igor_message).digest()
        signature_igor = key_igor.sign(hash_of_igor_message, '')
        hash_of_tina_message = MD5.new(tina_message).digest()
        signature_tina = key_tina.sign(hash_of_tina_message, '')

        # Encrypt messages using the other party's public key...
        encrypted_igor_message = public_tina.encrypt(igor_message, 32)
        encrypted_tina_message = public_igor.encrypt(tina_message, 32)

        # Decrypt messages using own private keys...
        decrypted_igor = key_tina.decrypt(encrypted_igor_message)
        decrypted_tina = key_igor.decrypt(encrypted_tina_message)

        # Signature validation and console output...
        hash_igor_decrypted = MD5.new(decrypted_igor).digest()
        if public_igor.verify(hash_igor_decrypted, signature_igor):
            print ("TINA received from IGOR:")
            print (decrypted_igor)
            print ("")

        hash_tina_decrypted = MD5.new(decrypted_tina).digest()
        if public_tina.verify(hash_tina_decrypted, signature_tina):
            print ("IGOR received from TINA:")
            print (decrypted_tina)
            print ("")

        return render(request, 'rest/fifth.html', {'tina_message': tina_message.decode('UTF-8'), 'igor_message': igor_message.decode('UTF-8'),
                                                    'hash_of_tina_message': str(hash_of_tina_message),
                                                    'hash_of_igor_message': str(hash_of_igor_message),
                                                    'hash_tina_decrypted': str(hash_tina_decrypted), 'hash_igor_decrypted': str(hash_igor_decrypted),
                                                    'igor_verified': public_igor.verify(hash_igor_decrypted, signature_igor),
                                                    'tina_verified': public_tina.verify(hash_tina_decrypted, signature_tina)})

    else:
        return render(request, 'rest/fifth.html')
