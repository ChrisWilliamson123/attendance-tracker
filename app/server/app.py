import os, random, ssl, sys
from flask import Flask, render_template
from flask_mysqldb import MySQL
from werkzeug.serving import run_simple


try:
  ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  ctx.load_cert_chain('server.crt', 'server.key')
except (FileNotFoundError):
  # No ssl cert was found, continue without TLS.
  ctx = None

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')
app.config.from_object('config')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    a = cur.execute('''CREATE TABLE Attendees (ID int)''')
    print(a)
    return render_template('index.html')

if __name__ == '__main__':
    args = len(sys.argv)
    ip = sys.argv[1] if 1 < args else '0.0.0.0'
    port = sys.argv[2] if 2 < args else 5000
    run_simple(ip, port, app, ssl_context=ctx) if ctx else run_simple(ip, port, app)
