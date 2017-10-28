"""
Main entry point for the server
"""
import argparse
from flask import Flask, render_template
from werkzeug.serving import run_simple
from db import DatabaseManager

# Blueprint imports
import index, api

class Server:
  def __init__(self):
    parser = argparse.ArgumentParser(
        description='Backend server for the attendence tracker.')
    parser.add_argument(
        '--hostname',
        metavar='h',
        type=str,
        help='The ip/website to serve on',
        default='localhost')
    parser.add_argument(
        '--port',
        metavar='p',
        type=int,
        help='The port to serve on',
        default=8080)
    parser.add_argument(
        '--dbfile',
        metavar='d',
        type=str,
        help='The sqlite database file',
        default='database.db')
    parser.add_argument(
        '--ssl_cert',
        type=str,
        help='The SSL certificate file to use')
    parser.add_argument(
        '--ssl_key',
        type=str,
        help='The SSL key file to use')
    
    self.args = parser.parse_args()

  def start(self, blueprints=[]):
    # Initialise the server w/ the static folders
    app = Flask(__name__, static_folder='../static/dist', template_folder='../static')
    app.config.from_object('config')
    # Set up the database
    db_manager = DatabaseManager(self.args.dbfile)

    # Parse the optional arguments
    optional_args = {}
    if self.args.ssl_cert and self.args.ssl_key:
      ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
      ctx.load_cert_chain('server.crt', 'server.key')
      optional_args['ssl_context'] = ctx

    # Register the blueprints
    for blueprint in blueprints:
      app.register_blueprint(blueprint)

    # Run the server with the desired config
    run_simple(self.args.hostname, self.args.port, app, **optional_args)

if __name__ == '__main__':
  server = Server()
  server.start([index.blueprint, api.blueprint])
