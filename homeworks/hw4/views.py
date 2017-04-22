from django.shortcuts import render

def index(request):
    page_title = "Fourth homework"
    content = "deploying django app on server using https"

    problem1 = [('ca_certificates', 'Create CA and issue a signed certificate.'),
                ('deploy', 'Deploy application so it can be access via HTTPS.'),]
    problems = [problem1]
    return render(request, 'landing.html', {'page_title': page_title, 'content': content, 'problems': problems})

def ca_certificates(request):
    page_title = "Creating CA and signing certificates"

    problem1 = [('ca_certificates', 'Create CA and issue a signed certificate.'),
                ('deploy', 'Deploy application so it can be access via HTTPS.'),]
    problems = [problem1]

    explanation = [('Certification Authority (preparation)', ['Make directory where you want to save all info <code>mkdir path/ca</code>',
                        '<code>mkdir newcerts certs crl private requests</code> &emsp; inside ca directory make directories',
                        '<code>cp /etc/ssl/openssl.cnf ./config.txt</code> &emsp; copy default setting CA will use',
                        '<code>touch index.txt</code> &emsp; file that will serve as CA database for all issued certificates',
                        '<code>echo "01" > serial</code> &emsp; file in which CA will look when signing certificate request for serial number',
                        'We constructed those directories/files because default ssl setting use them, but you can change their names, and then config.txt file accordingly.',]),
                    ('Certification Authority (initialization)', ['Edit config.txt file so it will match settings you want eq.',
                        '<code>dir = /pwd/ca</code> &emsp; change directory location so when signing script knows where to look for.',
                        '<code>default_days = 3650</code> &emsp; add how many days you want signed certificate will last',
                        '<code>stateOrProvinceName = supplied</code> &emsp; change settings regarding what certificates request will you sign, if match you can only sign certificates with same info like your CA',
                        '<code>openssl genrsa -des3 -out private/cakey.pem 4096</code> &emsp; create CA private key and save it to private directory for later use',
                        '<code>openssl req -new -x509 -key private/cakey.pem -out cacert.pem -days 3650 -set_serial 0</code> &emsp; making CA certificate from private key that will last 3650 days and with serial number 0',
                        'If you want to use different names for key/certificate you will need to change config.txt file accordingly.']),
                    ('Certificate request', ['In our case we will create and sign certificate request, but in practice clients make their certificate request and send to CA just request.',
                        '<code>openssl genrsa -des3 -out webserverkey.pem 2048</code> &emsp; creating private key for new certificate; every client should keep his key SAFE!',
                        '<code>openssl req -new -key webserverkey.pem -out webservercert.csr</code> &emsp; creating certificate request',
                        '<code>cp webservercert.csr /pwd/ca/requests</code> &emsp; copy request to directory/send it to a desired CA company']),
                    ('Signing certificate request', ['<code>cd /pwd/ca/requests</code> emsp; go to directory with requests',
                        '<code>openssl ca -in webservercert.csr -config /pwd/ca/config.txt</code> certificate request is now signed and you can find it in ca/newcerts directory',
                        '[Note] In last comand you could also use -out cert.pem flag if you want extra copy of certificate.']),
                    ('Sources:', ['<a href="http://acidx.net/wordpress/2012/09/creating-a-certification-authority-and-a-server-certificate-on-ubuntu/">Creating CA and Server Certificate on Ubuntu</a>'])]

    return render(request, 'landing.html', {'page_title': page_title, 'explanation': explanation})

def deploy(request):
    page_title = "Deploying django app on apache server via HTTPS"
    explanation = [('Prerequisites', ['Apache server, mod_wsgi, virtualenv']),
                    ('Django app', ['Create virtualenv and start django project in it.',
                                    'Put in settings.py in ALLOWED_HOSTS=["your domain name"]',
                                    'Add static root <code>STATIC_ROOT = os.path.join(BASE_DIR, "static/")</code>']),
                    ('Configure Apache to use SSL certificate', ['Add <code>127.0.0.1 your_domain</code> to /etc/hosts file so when you write your domain name your computer knows where to look for that address.',
                        '[Note] Only need when you are working localy, that way you don\'t need DNS to resolve your url address, needed because you have signed certificate for special domain name.',
                        'Add in /etc/apache2/sites-available/default-ssl.conf in SSLCertificateFile and SSLCertificateKeyFile path to your cert/key.']),
                    ('Configure Apache to serve Django application', ['Inside /etc/apache2/sites-available/default-ssl.conf add following: (pwd is path to your project directory)',
                        '''<code> Alias /static /pwd/static <br> &ltDirectory /pwd/static> <br> &emsp; Require all granted <br> &lt/Directory> <br>
                            &ltDirectory /pwd/myproject> <br> &ltFiles wsgi.py> <br> &emsp; Require all granted <br> &lt/Files> <br> &lt/Directory> <br>
                            WSGIDaemonProcess myproject python-home=/pwd/myprojectenv python-path=/pwd <br> WSGIProcessGroup myproject <br>
                            WSGIScriptAlias / /pwd/myproject/wsgi.py </code>''',
                        'Change permissions on your project database so apache can read it.',
                        '<code>chmod 664 ~/myproject/db.sqlite3</code> &emsp; change the permissions so that the group owner of the database can read and write',
                        '<code>sudo chown :www-data ~/myproject/db.sqlite3</code> &emsp; add apache group (www-data) ownership over database file',
                        '<code>sudo chown :www-data ~/myproject</code> &emsp;  give the Apache group ownership over the database\'s parent directory',
                        '[Note] Apache server should also be able to see your project directory so add read permissions to all your parents directories for www-data group.']),
                    ('Sources:', ['<a href="https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04#configure-apache">How to server Django app with Apache and mod_wsgi</a>'])]
    return render(request, 'landing.html', {'page_title': page_title, 'explanation': explanation})
