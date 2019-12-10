from bottle import hook, request, static_file, template, route, get

@hook('before_request')
def strip_trailing_slash():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./static")


@get('/')
def index():
    context = {
        'active': 'index'
    }

    return template('index.html', **context)


@get('/loan/create')
def index():
    context = {
        'active': 'add-loan'
    }

    return template('add-loan.html', **context)


@get('/report/read/details')
def index():
    context = {
        'active': 'report-details'
    }

    return template('report-details.html', **context)