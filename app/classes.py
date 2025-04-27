class Service:
    def __init__(self, description, time_in_minutes):
        self.description = description
        self.time_in_minutes = time_in_minutes

class WorkDay:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

class Barber:
    def __init__(self, name, agenda, picture, email=None):
        self.name = name
        self.email = email
        self.agenda = agenda
        self.picture = picture
        self.services: list[Service] = []
        self.workDays: list[WorkDay] = []

    def add_service(self, service: Service):
        self.services.append(service)

    def get_services(self):
        return self.services
    
    def add_workDays(self, service: Service):
        self.workDays.append(service)

    def get_workDays(self):
        return self.workDays

class Shop:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.barbers: list[Barber] = []

    def add_barber(self, barber: Barber):
        self.barbers.append(barber)

    def get_barbers(self):
        return self.barbers
