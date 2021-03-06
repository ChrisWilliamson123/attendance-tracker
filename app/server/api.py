import time
import json
import itertools as it
from db import DatabaseManager
from enum import IntEnum
from flask import Blueprint, render_template, request, jsonify

blueprint = Blueprint('api', __name__)

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
  DatabaseManager().insert_event(response)
  return response

def decide_response(ticket_id, direction, gate_id):
  # Allow iff the user is out and coming in, or if they're already in and they're going out
  is_in = is_in_event(ticket_id)
  allow = (not is_in and direction == Direction.IN) or (is_in and direction == Direction.OUT)
  action = Action.ACCEPT if allow else Action.DENY
  # TODO: Include abuse heuristics (e.g. if the same ticket has been used <n times in the past m minutes?)
  return (action, '')

@blueprint.route('/api/get_ticket_history', methods=['GET'])
def get_ticket_history():
  ticket_id = request.args.get('ticket_id')
  
  return json.dumps(get_ticket_history(ticket_id))

def get_ticket_history(ticket_id):
  ticket_filter = lambda row: row[0] == int(ticket_id)
  cursor = DatabaseManager().get_entries_for_ticket(ticket_id)
  return list(map(parse_row, filter(ticket_filter, cursor)))

# TODO: Use Database Query to filter for the latest entry/exit rather than
#       a manual query
def is_in_event(ticket_id):
  # Get events for the ticket
  events = get_ticket_history(ticket_id)
  # If there are no events, the person is assumed to be out
  if not events:
    return False
  # Sort by time descending
  events = sorted(events, key = lambda event: -event['time'])
  # Get the last event
  last_event = max(events, key = lambda event: event['time'])
  return last_event['direction'] == Direction.IN 
  

@blueprint.route('/api/get_event_status', methods=['GET'])
def get_event_status():
  out = {}
  all_gate_events = list(map(parse_row, DatabaseManager().get_all_entries()))
  total_events = len(all_gate_events)
  for entry in all_gate_events:
    # Skip failed attempts to pass the gate
    if entry['action'] == Action.DENY:
      continue
    if not entry['id'] in out:
      out[entry['id']] = []
    out[entry['id']].append(1 if entry['direction'] == Direction.IN else -1)
  total = 0
  for ticket in out:
    in_event = sum(out[ticket]) > 0
    if in_event:
      total += 1
  return json.dumps({'total_events':total_events,'current_population':total})

def parse_row(row):
  return {'id':row[0],
          'direction':Direction(row[1]),
          'action':Action(row[2]),
          'message':row[3],
          'time':row[4]}
