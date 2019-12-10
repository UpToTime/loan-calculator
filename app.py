from bottle import run
from routes import calculator

run(host='localhost', port=8080, debug=True, reloader=True)