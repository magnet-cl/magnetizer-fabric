# standard library
import os
import socket

# fabric
# from fabric.api import env
# from fabric.api import run
# from fabric.api import sudo
from fabric.api import task
# from fabric.colors import green
# from fabric.colors import red
# from fabric.contrib.files import append
from fabric.operations import prompt

# fabtools
from fabtools.files import upload_template

from fabfile import utils


ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TEMPLATES_FOLDER = os.path.join(ROOT_FOLDER, 'templates')


def is_valid_ip_address(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


@task
def install():
    # install nginx
    utils.deb.install('nginx')

    # install FastCGI wrapper
    #

    # configure
    webpay_ip = prompt("Webpay server's IP address:", validate=None)
    webpay_hostname = prompt("Webpay server's hostname:")

    app_ip = prompt("Application server's IP address:", validate=None)
    app_close_url = prompt("Application server's hostname:", validate=None)  # TODO: validate URL
    
    config = {'commerce_id': 597026007976,
              'webpay_ip': webpay_ip,
              'webpay_hostname': webpay_hostname,
              'app_ip': app_ip,
              'app_close_url': app_close_url}

    print('Uploading the "kit"...')
    upload_template(os.path.join(TEMPLATES_FOLDER, 'webpay/cgi-bin/datos/tbk_config.dat'), '/usr/lib/nginx/html/cgi-bin/datos/', context=config, mkdir=True, use_sudo=True, backup=False)
    print('Done')
