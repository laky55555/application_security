from django.shortcuts import render
from django.core.urlresolvers import reverse
# Good for signing/verifying signature. Easy for loading keys/certificates.
import OpenSSL
# Good for encryption/decryption. Easy to transfer keys from OpenSSL to cryptography data types.
# Not good for importing certificates.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# from django.conf import fourthhwkey_PRIVATE_KEY_PASS as fourth_pass
from django.conf import settings

from .models import read_certificate, read_secret_key, check_LDAP_credentials, search_LDAP_user

def index(request):
    page_title = "Fifth homework"
    content = "Authentication, Certificates"
    problem1 = [('read_local', 'Read and print certificate from a local file.'),
                ('read_central', 'Read and print certificate from some central repository (e.g. Certificate Store in Windows).'),
                ('encrypt_decrypt', 'Encrypt and decrypt using the obtained certificate and the corresponding private key.')]
    problem2 = [('https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-a-basic-ldap-server-on-an-ubuntu-12-04-vps', 'Start LDAP server. Create several accounts, protect an access to accounts based on at least 2 security groups.'),
                ('', 'Connects to the LDAP server.'),
                ('authenticate_user', 'Authenticates users.'),
                ('search_user', 'Searches at least 4 attributes of the user.'),
                ('sniffer', 'If you do that without applying an encrypted channel, use sniffer to see the transmission.')]
    problems = [problem1, problem2]

    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})


def read_local(request):
    cert_homework = read_certificate('hw4/certificates/fourthhwcert.pem', True)
    cert_hogwarts = read_certificate('hw4/certificates/fifthhwcert.pem')
    cert_info = [[], []]
    for i, j in cert_homework.get_subject().get_components():
        cert_info[0].append(j)
    cert_info[0].append(cert_homework.get_signature_algorithm())
    for i, j in cert_hogwarts.get_subject().get_components():
        cert_info[1].append(j)
    cert_info[1].append(cert_hogwarts.get_signature_algorithm())
    page_title = "Fifth homework - reading keys/certificates"

    explanation = [('Reading certificates', ['To read certificate we use OpenSSL library (OpenSSL.crypto.load_certificate).',
                                                'After loading certificate we can access all certificate info eg. get_subject ...'])]
    return render(request, 'hw5/show_keys_certs.html', {'page_title': page_title, 'cert_info': cert_info, 'explanation': explanation})


def read_central(request):
    certum = read_certificate('/etc/ssl/certs/Certum_Root_CA.pem', False)
    certum2 = read_certificate(
        '/etc/ssl/certs/Certum_Trusted_Network_CA.pem', False)
    comodo = read_certificate(
        '/etc/ssl/certs/COMODO_Certification_Authority.pem', False)
    names = ['Certum_Root_CA.pem', 'Certum_Trusted_Network_CA.pem',
             'COMODO_Certification_Authority.pem']
    data = [certum.get_subject().get_components(), certum2.get_subject(
    ).get_components(), comodo.get_subject().get_components()]
    zipped = zip(names, data)
    page_title = "Fifth homework"

    explanation = [('Ubuntu certificates', ['All system certificates are located in /etc/ssl/certs/*',
                                                'To read some of system certificates procedure is the same like reading local ones.']) ,
                    ('Bonus', ['Instaling root CA on Ubuntu.', '<b>GUI (easier way)</b>, double click on certificate and then choose options import.' ,
                                '<b>Terminal</b>, Create a directory for extra CA certificates in /usr/share/ca-certificates (probably already exist)',
                                'sudo cp foo.crt /usr/share/ca-certificates/extra/foo.crt copy certificate into new directory',
                                'sudo dpkg-reconfigure ca-certificates, let ubuntu make relative path',
                                'NOTE, certificate needs to be in .crt format openssl x509 -in foo.pem -inform PEM -out foo.crt',
                                '<a href="http://manpages.ubuntu.com/manpages/xenial/man8/update-ca-certificates.8.html">Link to Ubuntu man pages</a>'])]
    return render(request, 'hw5/firefox_certs.html', {'page_title': page_title, 'zipped': zipped, 'explanation': explanation})


def encrypt_decrypt(request):
    # Load certificates and PKeys from files.
    cert_homework = read_certificate('hw4/certificates/fourthhwcert.pem')
    cert_hogwarts = read_certificate('hw4/certificates/fifthhwcert.pem')

    privat_homework = read_secret_key('hw4/certificates/fourthhwkey.pem', settings.FOURTH_PRIVATEKEY_PASS)
    privat_hogwarts = read_secret_key('hw4/certificates/fifthhwkey.pem', settings.FIFTH_PRIVATEKEY_PASS)

    # Get RSA public keys from certificates
    public_homework = cert_homework.get_pubkey().to_cryptography_key()
    public_hogwarts = cert_hogwarts.get_pubkey().to_cryptography_key()

    # Message to encrypt and padding using for encryption.
    message = "Secret spell needed to do for homework."
    message_asci = message.encode('ascii')
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#encryption
    used_padding = padding.OAEP(mgf=padding.MGF1(
        algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None)
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
    # Reciever decrypt message with his private key. First need to get RSA
    # private key from loaded key.
    try:
        decrypted = privat_hogwarts.to_cryptography_key().decrypt(encrypted, used_padding)
    except Exception as e:
        decrypted = 'Decryption FAILED!'
    data = [('message', message), ('encrypted (hex)', encrypted.hex()[0:60] + '....'),
            ('signature (hex)', signature.hex()[0:60] + '....'), ('verify', verify), ('decrypted', decrypted)]

    page_title = "Fifth homework - encrypting/decrypting"
    explanation = [('Signature', ['''For signing/verifying signature we used <a
                        href="http://www.pyopenssl.org/en/stable/api/crypto.html#signing-and-verifying-signatures">OpenSSL.crypto.sign/verify</a>''']),
                    ('Encryption', ['For encrypting from certificates/keys loaded with OpenSSL we first needed to extract keys.',
                                    'For extracting we used library <a href="https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#encryption">Cryptography</a>'])]

    return render(request, 'hw5/encrypting.html', {'page_title': page_title, 'data': data, 'explanation': explanation})


def authenticate_user(request):
    page_title = "LDAP"
    correct = 0
    message = 0
    if(request.method == 'POST'):
        correct, message = check_LDAP_credentials(request)

    link = reverse('hw6:s_key')
    explanation = [('Authentication, django backend', ['For just simple authentication django has already <a href="https://pypi.python.org/pypi/django-auth-ldap/1.2.8">existing backend</a>, you just need to copy config to your settings and you are ready to go.',
                                                 'When using existing backend django first make attempt to bind to LDAP server with credentials from settings and then checks input from user.',
                                                 'When new user log in, that user is created into django DB (with default config he is active but not staff or superuser.)',
                                                 '<a href="https://pythonhosted.org/django-auth-ldap/users.html">Note:</a> Django 1.7 and later do not directly support user profiles. In these versions, LDAPBackend will ignore the profile-related settings.']),
                    ('Authentication, custom', ['You can either make custom django backend or just check credentials against LDAP and save user in sesion.',
                                                'Checking info agains LDAP can be done with ldap (pip install django-python3-ldap) trying to make bind_s to server.',
                                                'If credentials are valid connection will be made else Authentication error will occur.',
                                                'For making custom backend see <a href="' + link + '">HW6 with S/KEY authentication</a>'])]
    return render(request, 'hw5/authenticate_user.html', {'page_title': page_title, 'correct': correct, 'message': message, 'explanation': explanation})


def search_user(request):
    page_title = "Search user"
    explanation = [('LDAP search', ['Default LDAP settings allow anonymous user to search database.',
                                    'For searching we use ldap function search_s (synchronous search) without any authentication.',
                                    'For parameters of search we can specify base DN, search scope, search filter and attributes which we want to get.',
                                    'In our example default values are: top DN for base, entiry subtree for scope, and the most general filter (no filter) with all attributes',
                                    'For detailed example try search on <a href="https://homework.mutiny.codes/phpldapadmin/">phpldapadmin</a>.'])]

    if(request.method == 'POST'):
        answer = search_LDAP_user(request)
        return render(request, 'hw5/search_user.html', {'page_title': page_title, 'answer': answer, 'explanation': explanation,
                                'attributes': request.POST.get('attributes'), 'filter': request.POST.get('filter')})

    return render(request, 'hw5/search_user.html', {'page_title': page_title, 'explanation': explanation})

def sniffer(request):
    page_title = "Sniffer"
    explanation = [('Wireshark', ['Open source for linux/win/ios <a href="https://www.wireshark.org/#download">download</a>, or sudo apt-get install wireshark.',
                                'Needs root permission to monitor internet traffic.',
                                'If LDAP server is installed locally monitor loopback traffic.',
                                'If both server with application and LDAP are on same computer traffic doesn\'t need to be encrypted because nobody can see it.',]),]
    pic = 'hw5/LDAPsniffer.png'
    return render(request, 'base.html', {'page_title': page_title, 'explanation': explanation, 'pic': pic})
