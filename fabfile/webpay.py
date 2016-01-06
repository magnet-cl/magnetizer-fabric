# standard library
import os
import socket

# fabric
from fabric.api import sudo
from fabric.api import task
from fabric.operations import prompt
from fabric.operations import put

# fabtools
from fabtools.files import upload_template

from fabfile import utils


ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TEMPLATES_FOLDER = os.path.join(ROOT_FOLDER, 'templates/webpay/')


@task
def install():
    # install nginx
    utils.deb.install('nginx')

    # install FastCGI wrapper
    utils.deb.install('fcgiwrap')

    # configure fcgi

    # configure
    webpay_ip = prompt("Webpay server's IP address:")
    webpay_hostname = prompt("Webpay server's hostname:")

    app_ip = prompt("Application server's IP address:")
    app_close_url = prompt("Application server's hostname:")
    
    config = {'commerce_id': 597026007976, # test env id
              'webpay_ip': webpay_ip,
              'webpay_hostname': webpay_hostname,
              'app_ip': app_ip,
              'app_close_url': app_close_url}

    print('Uploading the "kit"...')

    # render testing config
    upload_template(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_config.dat'),
                    '/usr/lib/nginx/html/cgi-bin/datos/',
                    context=config,
                    mkdir=True,
                    use_sudo=True,
                    backup=False)
    
    upload_template(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_param.txt'),
                    '/usr/lib/nginx/html/cgi-bin/datos/',
                    mkdir=True,
                    use_sudo=True,
                    backup=False)

    upload_template(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_trace.dat'),
                    '/usr/lib/nginx/html/cgi-bin/datos/',
                    mkdir=True,
                    use_sudo=True,
                    backup=False)

    # copy the binaries
    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_bp_pago.cgi'),
        '/usr/lib/nginx/html/cgi-bin/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_bp_resultado.cgi'),
        '/usr/lib/nginx/html/cgi-bin/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_check_mac.cgi'),
        '/usr/lib/nginx/html/cgi-bin/',
        use_sudo=True,
        backup=False)

    # copy the keys
    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/privada.pem'),
        '/usr/lib/nginx/html/cgi-bin/maestros/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/tbk.orig.pem'),
        '/usr/lib/nginx/html/cgi-bin/maestros/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/tbk_public_key.pem'),
        '/usr/lib/nginx/html/cgi-bin/maestros/',
        use_sudo=True,
        backup=False)

    # copy template dir
    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/leeme.txt'),
        '/usr/lib/nginx/html/cgi-bin/template/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/reintento.html'),
        '/usr/lib/nginx/html/cgi-bin/template/',
        use_sudo=True,
        backup=False)

    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/transicion.html'),
        '/usr/lib/nginx/html/cgi-bin/template/',
        use_sudo=True,
        backup=False)

    # create log directory
    cmd = 'mkdir /usr/lib/nginx/html/cgi-bin/log/'
    sudo(cmd)

    # set proper permissions
    put(os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/transicion.html'),
        '/usr/lib/nginx/html/cgi-bin/template/',
        use_sudo=True,
        backup=False)

    # configure nginx
    put(os.path.join(TEMPLATES_FOLDER, 'nginx_conf'),
        '/etc/nginx/sites-enabled/default',
        use_sudo=True,
        backup=False)

    # and restart the service
    cmd = 'service nginx restart'
    sudo(cmd)

    print('Done')
