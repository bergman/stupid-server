from gevent import monkey
monkey.patch_all()
from bottle import get, run, error, abort
import sys
import random
from linecache import getline

port = int(sys.argv[1])
page_size = int(sys.argv[2])
filename = sys.argv[3]
# warm up the cache
getline(filename, 0)

@error(404)
def error404(error):
    return ('Request any page of {page_size} rows. Searching outside of the\n'
            'available range will return empty results. The service is\n'
            'extremly shaky so expect erors.\n\n'
            'API usage:\n'
            'GET /logs/<page>\n\n'

            'Debugging:\n'
            'GET /numbers/<page>\n').format(page_size=page_size)

@error(503)
def error503(error):
    return 'Service Unavailable\n'

@get('/numbers/<page:int>')
def numbers(page):
    start = page * page_size
    end = start + page_size

    return get_numbers(start, end)

@get('/logs/<page:int>')
def logs(page):
    # random errors, beware!
    if random.randint(0, 10) == 0:
        abort(503)

    start = page * page_size
    end = start + page_size

    return get_rows(start, end)

def get_rows(start, end):
    output = ''
    for line in xrange(start, end):
        output += getline(filename, line)

    return output

def get_numbers(start, end):
    return '\n'.join([str(i) for i in range(start, end)]) + '\n'

run(server='gevent', port=port)
