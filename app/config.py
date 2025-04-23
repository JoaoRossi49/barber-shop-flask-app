from app.classes import Barber, Shop, Service
def get_shops():
    all_shops = []

    #Definição do barbeiro
    camargo = Barber(name='Camargo', email='joao.rossi.figueiredo@gmail.com', agenda='8d01f0142acd6d77e73b098111c7c1a0decbe76e8a1e1c3e731629847659beba@group.calendar.google.com', picture='camargo.jpeg')

    #Definição de serviços
    camargo.add_service(Service(description='Corte de cabelo masculino', time_in_minutes=30))
    camargo.add_service(Service(description='Barba', time_in_minutes=30))
    
    #O barbeiro Camargo faz parte da barbearia Camargo
    camargo_shop = Shop('Camargo')
    camargo_shop.add_barber(camargo)

    #Definição de todas as barbearias
    all_shops.append(camargo_shop)

############################################################################################################################################################################

    #Definição do barbeiro
    teste = Barber(name='Barbeiro teste', agenda='8d01f0142acd6d77e73b098111c7c1a0decbe76e8a1e1c3e731629847659beba@group.calendar.google.com', picture='teste.jpg')
    teste2 = Barber(name='Irmão do Barbeiro teste', agenda='8d01f0142acd6d77e73b098111c7c1a0decbe76e8a1e1c3e731629847659beba@group.calendar.google.com', picture='teste.jpg')

    #Definição de serviços
    teste.add_service(Service(description='Corte de cabelo masculino', time_in_minutes=60))
    teste.add_service(Service(description='Barba e bigode', time_in_minutes=60))

    teste2.add_service(Service(description='Corte simples', time_in_minutes=15))
    
    #O barbeiro Camargo faz parte da barbearia Camargo
    teste_shop = Shop ('Barbearia Teste')
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