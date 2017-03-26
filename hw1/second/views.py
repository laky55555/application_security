from django.shortcuts import render
from django.template import loader
from django.http import Http404

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from Crypto.PublicKey import RSA
from Crypto import Random

from time import time
import numpy as np


# Create your views here.

from django.http import HttpResponse

def test_symmetric(key_len, open_text):
    key = os.urandom(key_len)
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()
    start = time()
    ct = encryptor.update(open_text.encode('UTF-8')) + encryptor.finalize()
    decryptor.update(ct) + decryptor.finalize()
    return time() - start

def test_asymmetric(key_len, open_text):
    open_text = open_text.encode('UTF-8')
    random_gen = Random.new().read
    start = time()
    key_pair = RSA.generate(key_len, random_gen)
    public_key = key_pair.publickey()
    encrypted = public_key.encrypt(open_text, 32)
    decrypted = key_pair.decrypt(encrypted)
    if open_text != decrypted:
        raise Http404("Error in encrypting/decripting with RSA.\nStart text = " + str(open_text) + ".\nDecripted text = " + str(decrypted))
    return time() - start

def index(request):
    if request.method == 'POST':
        open_text = request.POST.get('open_text')
        if open_text is None or len(open_text) < 2:
            open_text = "This is defaut open text ready for encryption."
        open_orig = open_text
        while len(open_text) < 10000000:
            open_text += '; ' + open_text
        while len(open_text)%16 != 0:
            open_text = " " + open_text

        times_symmetric = np.array([test_symmetric(16, open_text), test_symmetric(24, open_text), test_symmetric(32, open_text)])
        for i in range(50):
            times_symmetric += np.array([test_symmetric(16, open_text), test_symmetric(24, open_text), test_symmetric(32, open_text)])
        times_symmetric = times_symmetric/51

        times_asymmetric = np.array([test_asymmetric(1024, open_orig), test_asymmetric(2048, open_orig), test_asymmetric(4096, open_orig)])
        times_asymmetric += np.array([test_asymmetric(1024, open_orig), test_asymmetric(2048, open_orig), test_asymmetric(4096, open_orig)])
        times_asymmetric += np.array([test_asymmetric(1024, open_orig), test_asymmetric(2048, open_orig), test_asymmetric(4096, open_orig)])
        times_asymmetric = times_asymmetric/3
        return render(request, 'second/cript.html', {'open_text': open_orig, 'times_symmetric': times_symmetric, 'times_asymmetric': times_asymmetric,
                        'symmetric_len': len(open_text), 'asymmetric_len': len(open_orig)})

    return render(request, 'second/cript.html')
