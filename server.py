import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from agendas import avaliable_agendas
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Escopos de permissão (leitura e escrita no calendário)
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_api():
    creds = None
    # Verificar se já existe um token salvo
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Se não houver token ou ele for inválido, autentique novamente
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Salvar o token para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def list_calendars(service):
    """
    Lista os calendários acessíveis pelo usuário autenticado.
    """
    # Requisita a lista de calendários
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    if not calendars:
        print("Nenhum calendário encontrado.")
        return

    # Exibe o ID e o nome de cada calendário
    for calendar in calendars:
        print(f"Calendário: {calendar['summary']}, ID: {calendar['id']}")


def create_event(service, calendar_id, summary, description, start_time, end_time, timezone="America/Sao_Paulo"):
    """
    Cria um novo evento em um calendário especificado.

    Args:
        service: Objeto da API Google Calendar.
        calendar_id: ID do calendário onde o evento será criado.
        summary: Título do evento.
        description: Descrição do evento.
        start_time: Início do evento (ISO 8601).
        end_time: Fim do evento (ISO 8601).
        timezone: Fuso horário do evento (padrão é UTC).
    """
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
    }

    # Faz a requisição para criar o evento
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

    print(f"Evento criado com sucesso: {created_event['htmlLink']}")
    return created_event

def get_free_slots(service, calendar_id, start_time, end_time, interval_minutes=30):
    """
    Obtém os slots de tempo disponíveis em um calendário dentro de um intervalo de tempo.

    Args:
        service: Serviço da API do Google Calendar.
        calendar_id: ID do calendário para verificar a disponibilidade.
        start_time: Início do intervalo de tempo (ISO 8601).
        end_time: Fim do intervalo de tempo (ISO 8601).
        interval_minutes: Duração dos slots disponíveis em minutos.
    
    Returns:
        Lista de slots disponíveis como pares (start, end).
    """
    # Requisição para verificar períodos ocupados
    body = {
        "timeMin": start_time,
        "timeMax": end_time,
        "timeZone": "America/Sao_Paulo",
        "items": [{"id": calendar_id}]
    }
    print(body)

    busy_slots = service.freebusy().query(body=body).execute()

    # Obter os períodos ocupados
    busy_times = busy_slots['calendars'][calendar_id].get('busy', [])

    # Converter strings ISO 8601 para objetos datetime
    busy_intervals = [
        (datetime.datetime.fromisoformat(slot['start']), datetime.datetime.fromisoformat(slot['end']))
        for slot in busy_times
    ]

    print('Intervalos ocupados:', busy_intervals)

    # Gerar slots de tempo dentro do intervalo especificado
    available_slots = []
    current_time = datetime.datetime.fromisoformat(start_time)

    while current_time + datetime.timedelta(minutes=interval_minutes) <= datetime.datetime.fromisoformat(end_time):
        slot_end = current_time + datetime.timedelta(minutes=interval_minutes)

        # Verificar se o slot não está em nenhum período ocupado
        is_free = all(not (start <= current_time < end or current_time < start < slot_end) for start, end in busy_intervals)

        if is_free:
            available_slots.append((current_time, slot_end))

        current_time = slot_end

    return available_slots

# Criando o aplicativo Flask
app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

CORS(app)

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
    calendar_id = avaliable_agendas[0][0]
    start_time = data.get('start_time') + ':00-03:00'
    end_time = data.get('end_time') + ':00-03:00'

    service = build('calendar', 'v3', credentials=creds)
    free_slots = get_free_slots(service, calendar_id, start_time, end_time)

    return free_slots

@app.route('/createEvent', methods=['POST'])
@limiter.limit("1 per hour") 
def create_new_event():
    data = request.json
    calendar_id = avaliable_agendas[0][0]
    start_time = data.get('start_time') + ':00-03:00'
    end_time = data.get('end_time') + ':00-03:00'
    summary = data.get('summary', 'New Event')
    description = data.get('description', 'Event created via API')

    if not start_time or not end_time:
        return jsonify({"error": "start_time and end_time are required"}), 400
    
    creds = authenticate_google_api()
    service = build('calendar', 'v3', credentials=creds)

    free_slots = get_free_slots(service, calendar_id, start_time, end_time)

    if free_slots:
        create_event(
            service=service,
            calendar_id=calendar_id,
            summary=summary,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
    else:
        return jsonify({"message": "Event not created!"}), 400
    
    return jsonify({"message": "Event created successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)