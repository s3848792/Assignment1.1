import sys
import os
sys.path.insert(0,'var/www/html/Assignment1')


os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAWG5XCPIOBQ765M43'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'


def application(environ, start_response):
    for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        os.environ[key] = environ.get(key, '')

    from Assignment1 import app as _application
    return _application(environ, start_response)