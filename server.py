from gevent import monkey
monkey.patch_all()
from bottle import get, run, error, abort
import random

number_of_rows = 3141592
page_size = 100

@error(404)
def error404(error):
    return ('API usage:\n'
            'GET /logs/<page>\n\n'
            'First page:\n'
            'GET /logs/0\n\n'
            'Second page:\n'
            'GET /logs/1\n')

@error(503)
def error503(error):
    return 'Service Unavailable\n'

@get('/logs/<page:int>')
def logs(page):
    # random errors, beware!
    if random.randint(0, 10) == 0:
        abort(503)

    start = page * page_size
    end = min(start + page_size, number_of_rows)

    return get_rows(start, end) + '\n'

def get_rows(start, end):
    return '\n'.join([str(i) for i in range(start, end)])

run(server='gevent')
