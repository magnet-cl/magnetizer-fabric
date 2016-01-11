# standard library
import os

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
    app_close_url = prompt("Application server close url:")

    config = {
        'commerce_id': 597026007976,  # test env id
        'webpay_ip': webpay_ip,
        'webpay_hostname': webpay_hostname,
        'app_ip': app_ip,
        'app_close_url': app_close_url
    }

    print('Uploading the "kit"...')

    # paths
    bin_path = '/usr/share/nginx/html/cgi-bin/'
    data_path = '/usr/share/nginx/html/cgi-bin/datos/'
    keys_path = '/usr/share/nginx/html/cgi-bin/maestros/'
    templates_path = '/usr/share/nginx/html/cgi-bin/template/'
    logs_path = '/usr/share/nginx/html/cgi-bin/log/'

    # render testing config
    upload_template(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_config.dat'),
        data_path,
        backup=False,
        context=config,
        mkdir=True,
        mode=0644,
        use_sudo=True,
    )

    upload_template(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_param.txt'),
        data_path,
        backup=False,
        mkdir=True,
        mode=0644,
        use_sudo=True,
    )

    upload_template(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/datos/tbk_trace.dat'),
        data_path,
        backup=False,
        mkdir=True,
        mode=0644,
        use_sudo=True,
    )

    # copy the binaries
    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_bp_pago.cgi'),
        bin_path,
        mode=0755,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_bp_resultado.cgi'),
        bin_path,
        mode=0755,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/tbk_check_mac.cgi'),
        bin_path,
        mode=0755,
        use_sudo=True,
    )

    # create keys dir
    cmd = 'mkdir -p {}'.format(keys_path)
    sudo(cmd)

    # copy the keys
    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/privada.pem'),
        keys_path,
        mode=0644,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/tbk.orig.pem'),
        keys_path,
        mode=0644,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/maestros/tbk_public_key.pem'),
        keys_path,
        mode=0644,
        use_sudo=True,
    )

    # create templates dir
    cmd = 'mkdir -p {}'.format(templates_path)
    sudo(cmd)

    # copy template dir
    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/leeme.txt'),
        templates_path,
        mode=0644,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/reintento.html'),
        templates_path,
        mode=0644,
        use_sudo=True,
    )

    put(
        os.path.join(TEMPLATES_FOLDER, 'cgi-bin/template/transicion.html'),
        templates_path,
        mode=0644,
        use_sudo=True,
    )

    # create log directory
    cmd = 'mkdir -p {}'.format(logs_path)
    sudo(cmd)

    # set proper ownership and permissions
    sudo('chown -R www-data:www-data {}'.format(bin_path))
    sudo('chmod 0755 {}'.format(bin_path))
    sudo('chmod 0755 {}'.format(data_path))
    sudo('chmod 0755 {}'.format(keys_path))
    sudo('chmod 0755 {}'.format(templates_path))
    sudo('chmod 0755 {}'.format(logs_path))

    # configure nginx
    put(
        os.path.join(TEMPLATES_FOLDER, 'nginx_conf'),
        '/etc/nginx/sites-enabled/default',
        use_sudo=True
    )

    # and restart the service
    cmd = 'service nginx restart'
    sudo(cmd)

    print('Done')
