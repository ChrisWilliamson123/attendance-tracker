import time
import json
from enum import IntEnum
from flask import Blueprint, render_template, request, jsonify

blueprint = Blueprint('api', __name__)

# Mock a table
fake_database = []

class Direction(IntEnum):
  IN = 1
  OUT = 2

class Action(IntEnum):
  ACCEPT = 1
  DENY = 2

@blueprint.route('/api/check_ticket', methods=['GET'])
def check_ticket():
  ticket_id = request.args.get('ticket_id')
  direction = Direction[request.args.get('direction')]
  gate_id = request.args.get('gate_id')
  
  return json.dumps(process_ticket_check(ticket_id, direction, gate_id))

def process_ticket_check(ticket_id, direction, gate_id):
  # TODO: Validate arguments
  response = {'id':ticket_id, 'direction':direction,'gate_id':gate_id}
  (action, message) = decide_response(ticket_id, direction, gate_id)
  response['action'] = action
  response['message'] = message
  response['time'] = int(time.time())
  fake_database.append(response)
  return response

def decide_response(ticket_id, direction, gate_id):
  # TODO: Decide on a response
  # TODO: Include abuse heuristics (e.g. if the same ticket has been used <n times in the past m minutes?)
  return (Action.ACCEPT, 'Auto accepted')

@blueprint.route('/api/get_ticket_history', methods=['GET'])
def get_ticket_history():
  ticket_id = request.args.get('ticket_id')
  
  return json.dumps(get_ticket_history(ticket_id))

def get_ticket_history(ticket_id):
  ticket_filter = lambda row: row['id'] == ticket_id
  return list(filter(ticket_filter, fake_database))

