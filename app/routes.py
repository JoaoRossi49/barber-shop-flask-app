from flask import jsonify, request
from .calendar import create_event, get_free_slots, convert_timezone
from .config import avaliable_agendas
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from googleapiclient.discovery import build

limiter = Limiter(get_remote_address)

def register_routes(app):
    @app.route('/', methods=['GET'])
    def hello_world():
        return render_template('index.html')

    @app.route('/agendas', methods=['GET'])
    def get_agendas():
        agendas = [{'id': t[0], 'nome': t[1]} for t in avaliable_agendas]
        
        return jsonify(agendas)

    @app.route('/freeSlots', methods=['POST'])
    def free_slots():
        data = request.json
        calendar_id = data.get('calendar_id')
        start_time = data.get('start_time') + ':00-03:00'
        end_time = data.get('end_time') + ':00-03:00'

        free_slots = convert_timezone(get_free_slots(calendar_id, start_time, end_time))

        return jsonify(free_slots)

    @app.route('/createEvent', methods=['POST'])
    @limiter.limit("1 per hour")
    def create_new_event():
        data = request.json
        calendar_id = data.get('calendar_id')
        start_time = data.get('start_time') + ':00-03:00'
        end_time = data.get('end_time') + ':00-03:00'
        summary = data.get('summary', 'New Event')
        description = data.get('description', 'Event created via API')

        if not start_time or not end_time:
            return jsonify({"error": "start_time and end_time are required"}), 400

        free_slots = get_free_slots(calendar_id, start_time, end_time)

        if free_slots:
            create_event(calendar_id, summary, description, start_time, end_time)
            return jsonify({"message": "Event created successfully!"}), 201
        else:
            return jsonify({"message": "Event not created!"}), 400
