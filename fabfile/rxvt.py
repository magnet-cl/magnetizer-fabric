from fabric.api import task, run
from fabtools.files import upload_template
import utils


@task
def install():
    utils._deb.install('rxvt-unicode-256color')
    print('Uploading .Xresources...')
    upload_template('~/.Xresources', 'rxvt/Xresources')

    print('Uploading urxvtc...')
    upload_template('bin/urxvtc', 'rxvt/urxvtc', mkdir=True)
    run('chmod +x ~/bin/urxvtc')
