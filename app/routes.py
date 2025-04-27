from flask import jsonify, request, url_for
from .calendar import create_event, get_free_slots, convert_timezone
from .config import get_shops, get_barber_by_calendar_id
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from googleapiclient.discovery import build
from app.classes import Barber, Shop
from .utils import send_email
from dateutil import parser
from datetime import datetime, time

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

        barbers = get_barber_by_calendar_id(calendar_id)
        workdays = barbers[0].get_workDays()

        dias_permitidos = {}
        for dia in workdays:
            dias_permitidos[dia.day] = {
                'start': dia.start_time,
                'end': dia.end_time
            }

        slots_filtrados = []

        for slot in free_slots:
            try:
                start_dt = datetime.strptime(slot[0], '%a, %d %b %Y %H:%M:%S %Z')
                end_dt = datetime.strptime(slot[1], '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                continue

            dia_semana = start_dt.strftime('%A')

            if dia_semana in dias_permitidos:
                hora_inicio = dias_permitidos[dia_semana]['start']
                hora_fim = dias_permitidos[dia_semana]['end']
                #print(f"Hoje é {dia_semana} e o barbeiro trabalha das", hora_inicio, "às", hora_fim)
                #print("Slot:", start_dt.time(), "→", end_dt.time())

                if hora_inicio <= start_dt.time() < hora_fim:
                    #print('Considerado\n\n\n')
                    slots_filtrados.append(slot)

        return jsonify(slots_filtrados)

    @app.route('/api/createEvent', methods=['POST'])
    @limiter.limit("1 per hour")
    def create_new_event():
        data = request.json
        calendar_id = data.get('calendar_id') 
        start_time = data.get('start_time') + ':00-03:00'
        end_time = data.get('end_time') + ':00-03:00'
        summary = data.get('summary', 'New Event')
        description = data.get('description', 'Event created via API')

        #Formatar datas
        day = parser.parse(start_time).strftime('%d/%m')
        start_time_f = parser.parse(start_time).strftime('%H:%M')
        end_time_f = parser.parse(end_time).strftime('%H:%M')

        client = summary + ' -(' + description + ')' + f' no dia {day} - {start_time_f} até {end_time_f}'

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
