import os, random, ssl, sys
from flask import Flask, render_template
from flask_mysqldb import MySQL
from werkzeug.serving import run_simple

ssl_enabled = True
try:
  ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  ctx.load_cert_chain('server.crt', 'server.key')
except (FileNotFoundError):
  # No ssl cert was found, continue without TLS.
  ssl_enabled = False

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    a = cur.execute('''CREATE TABLE Attendees (ID int)''')
    print(a)
    return render_template('index.html')

if __name__ == '__main__':
    try:
      ip = sys.argv[1]
    except:
      ip = '0.0.0.0'
    try:
      port = sys.argv[2]
    except:
      port = 5000
    if ssl_enabled:
        run_simple(ip, port, app, ssl_context=ctx)
    else:
        run_simple(ip, port, app)