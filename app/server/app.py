import random
from flask import Flask, render_template
from werkzeug.serving import run_simple
import ssl, sys


ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('server.crt', 'server.key')

def get_hello():
    greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
    return random.choice(greeting_list)

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return get_hello()

if __name__ == '__main__':
    try:
        port = sys.argv[1]
    except:
        port = 5000
    run_simple('0.0.0.0', port, app, ssl_context=ctx)