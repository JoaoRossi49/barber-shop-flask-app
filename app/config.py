from app.classes import Barber, Shop, Service, WorkDay
from datetime import datetime, time

def get_shops():
    all_shops = []

    #Definição do barbeiro
    camargo = Barber(
    name='Camargo', 
    email='guillhermecs1001@gmail.com', 
    agenda='8d01f0142acd6d77e73b098111c7c1a0decbe76e8a1e1c3e731629847659beba@group.calendar.google.com', 
    picture='camargo.jpeg')

    #Definição de serviços
    camargo.add_service(Service(description='Corte', time_in_minutes=30))
    camargo.add_service(Service(description='Corte navalhado', time_in_minutes=45))
    camargo.add_service(Service(description='Corte + Barba', time_in_minutes=60))
    camargo.add_service(Service(description='Barba', time_in_minutes=30))

    

    #Definição de dias de trabalho
    camargo.add_workDays(WorkDay(day='Monday', start_time=time(9, 0), end_time=time(20, 0)))
    camargo.add_workDays(WorkDay(day='Tuesday', start_time=time(9, 0), end_time=time(20, 0)))
    camargo.add_workDays(WorkDay(day='Wednesday', start_time=time(9, 0), end_time=time(20, 0)))
    camargo.add_workDays(WorkDay(day='Thursday', start_time=time(9, 0), end_time=time(20, 0)))
    camargo.add_workDays(WorkDay(day='Friday', start_time=time(9, 0), end_time=time(20, 0)))
    camargo.add_workDays(WorkDay(day='Saturday', start_time=time(7, 0), end_time=time(19, 0)))
    #camargo.add_workDays(WorkDay(day='Sunday', start_time=time(8, 0), end_time=time(18, 0)))
    
    #O barbeiro Camargo faz parte da barbearia Camargo
    camargo_shop = Shop('Camargo', '/camargo')
    camargo_shop.add_barber(camargo)

    #Definição de todas as barbearias
    all_shops.append(camargo_shop)

############################################################################################################################################################################

    #Definição do barbeiro
    teste = Barber(
        name='Barbeiro teste', 
        email='joao.rossi.figueiredo@gmail.com', 
        agenda='2bb10a63e8c9765c7ba29f01f660a70824c950ffc5452801f141cb57ad0d57fb@group.calendar.google.com', 
        picture='teste.jpg')
    teste2 = Barber(
        name='Irmão do Barbeiro teste', 
        email='joao.rossi.figueiredo@gmail.com', 
        agenda='2bb10a63e8c9765c7ba29f01f660a70824c950ffc5452801f141cb57ad0d57fb@group.calendar.google.com', 
        picture='teste.jpg')

    #Definição de serviços
    teste.add_service(Service(description='Corte de cabelo masculino', time_in_minutes=60))
    teste.add_service(Service(description='Barba e bigode', time_in_minutes=60))

    teste2.add_service(Service(description='Corte simples', time_in_minutes=15))

    #Definição de dias de trabalho
    teste.add_workDays(WorkDay(day='Monday', start_time=time(9, 0), end_time=time(20, 0)))
    teste.add_workDays(WorkDay(day='Tuesday', start_time=time(9, 0), end_time=time(20, 0)))
    teste.add_workDays(WorkDay(day='Wednesday', start_time=time(9, 0), end_time=time(20, 0)))
    teste.add_workDays(WorkDay(day='Thursday', start_time=time(9, 0), end_time=time(20, 0)))
    teste.add_workDays(WorkDay(day='Friday', start_time=time(9, 0), end_time=time(20, 0)))
    teste.add_workDays(WorkDay(day='Saturday', start_time=time(7, 0), end_time=time(19, 0)))
    #teste.add_workDays(WorkDay(day='Sunday', start_time=time(8, 0), end_time=time(18, 0)))

    teste2.add_workDays(WorkDay(day='Monday', start_time=time(9, 0), end_time=time(20, 0)))
    
    #O barbeiro teste faz parte da barbearia teste
    teste_shop = Shop ('Barbearia Teste', '/barbearia-teste')
    teste_shop.add_barber(teste)
    teste_shop.add_barber(teste2)

    #Definição de todas as barbearias
    all_shops.append(teste_shop)

    return all_shops

def get_barber_by_calendar_id(calendar_id):
    shops = get_shops()

    barbers = []
    
    for shop in shops:
        for barber in shop.barbers:
            if barber.agenda == calendar_id:
                barbers.append(barber)
    
    return barbers