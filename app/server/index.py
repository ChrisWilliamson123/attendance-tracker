from flask import Blueprint, render_template

blueprint = Blueprint('index_page', __name__)

@blueprint.route('/')
def index():
  try:
    cur = server.database.connection.cursor()
    a = cur.execute('''CREATE TABLE Attendees (ID int)''')
    print(a)
  except:
    pass
  return render_template('index.html')

