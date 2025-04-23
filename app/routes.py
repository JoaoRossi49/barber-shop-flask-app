from flask import jsonify, request, url_for
from .calendar import create_event, get_free_slots, convert_timezone
from .config import get_shops, get_barber_by_calendar_id
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from googleapiclient.discovery import build
from app.classes import Barber, Shop
from .utils import send_email

limiter = Limiter(get_remote_address)

def register_routes(app):

    @app.route('/api/shops', methods=['GET'])
    def get_all_shops():
        shops = [
            {
                'id': id,
                'name': shop.name,
                'url': shop.url
            }
            for id, shop in enumerate(get_shops())
        ]

        return jsonify(shops)

    @app.route('/api/agendas/<int:shop_id>', methods=['GET'])
    def get_agendas(shop_id):
        shops = get_shops()
        
        shop = shops[shop_id]

        agendas = [
            {
                'id': barber.agenda,
                'nome': barber.name,
                'avatar': url_for('static', filename=f'images/{barber.picture}', _external=True),
                'services': [
                    {
                        'description': service.description,
                        'timeInMinutes': service.time_in_minutes
                    }
                    for service in barber.get_services()
                ]
            }
            for barber in shop.get_barbers()
        ]
        
        return jsonify(agendas)

    @app.route('/api/freeSlots', methods=['POST'])
    def free_slots():
        data = request.json
        calendar_id = data.get('calendar_id')
        start_time = data.get('start_time') + ':00-03:00'
        end_time = data.get('end_time') + ':00-03:00'

        free_slots = convert_timezone(get_free_slots(calendar_id, start_time, end_time))

        return jsonify(free_slots)

    @app.route('/api/createEvent', methods=['POST'])
    @limiter.limit("1 per hour")
    def create_new_event():
        data = request.json
        calendar_id = data.get('calendar_id') 
        start_time = data.get('start_time') + ':00-03:00'
        end_time = data.get('end_time') + ':00-03:00'
        summary = data.get('summary', 'New Event')
        description = data.get('description', 'Event created via API')

        client = summary + ' -(' + description + ')'

        if not start_time or not end_time:
            return jsonify({"error": "start_time and end_time are required"}), 400

        free_slots = get_free_slots(calendar_id, start_time, end_time)

        if free_slots:
            create_event(calendar_id, summary, description, start_time, end_time)
            #Envia e-mail de notificação
            barbers = get_barber_by_calendar_id(calendar_id)

            for barber in barbers:
                if barber.email:
                    send_email(client,barber.name, barber.email)

            return jsonify({"message": "Event created successfully!"}), 201
        else:
            return jsonify({"message": "Event not created!"}), 400
