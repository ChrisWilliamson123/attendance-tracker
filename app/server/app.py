"""
Main entry point for the server

TODO: Refactor this class so the index blueprint is not inside,
      or move the server starting to server.py
"""

from server import Server
from flask import Blueprint, render_template

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
    try:
      cur = server.database.connection.cursor()
      a = cur.execute('''CREATE TABLE Attendees (ID int)''')
      print(a)
    except:
      pass
    return render_template('index.html')

if __name__ == '__main__':
  server = Server()
  server.start([index_page])
