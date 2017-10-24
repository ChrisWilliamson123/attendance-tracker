import os, random, ssl, sys
from flask import Flask, render_template
from werkzeug.serving import run_simple
from db import DatabaseManager


try:
  ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  ctx.load_cert_chain('server.crt', 'server.key')
except (FileNotFoundError):
  # No ssl cert was found, continue without TLS.
  ctx = None

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')
app.config.from_object('config')
db_manager = DatabaseManager('test.db')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    arg_len = len(sys.argv)
    ip = sys.argv[1] if 1 < arg_len else '0.0.0.0'
    port = sys.argv[2] if 2 < arg_len else 5000
    run_simple(ip, port, app, ssl_context=ctx) if ctx else run_simple(ip, port, app)
