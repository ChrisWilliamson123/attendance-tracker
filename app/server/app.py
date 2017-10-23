import random
from flask import Flask, render_template
from werkzeug.serving import run_simple
import ssl, sys


try:
  ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  ctx.load_cert_chain('server.crt', 'server.key')
except (FileNotFoundError):
  # No ssl cert was found, continue without TLS.
  pass

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
      ip = sys.argv[1]
    except:
      ip = '0.0.0.0'
    try:
      port = sys.argv[2]
    except:
      port = 5000
    run_simple(ip, port, app, ssl_context=ctx)
