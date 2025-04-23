class Service:
    def __init__(self, description, time_in_minutes):
        self.description = description
        self.time_in_minutes = time_in_minutes

class Barber:
    def __init__(self, name, agenda, picture, email=None):
        self.name = name
        self.email = email
        self.agenda = agenda
        self.picture = picture
        self.services: list[Service] = []

    def add_service(self, service: Service):
        self.services.append(service)

    def get_services(self):
        return self.services

class Shop:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.barbers: list[Barber] = []

    def add_barber(self, barber: Barber):
        self.barbers.append(barber)

    def get_barbers(self):
        return self.barbers
