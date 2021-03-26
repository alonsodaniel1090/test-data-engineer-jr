import requests




def main():
    ''' Main prrogram process '''

    
    passengers = get_passengers_info()
    flights  = get_flights_info()

    flights_with_passengers = assign_passenger_to_flight(passengers, flights)








def get_passengers_info():
    '''
    Proceso:
        1. Obtener la informacion de las urls.
        2. Convertir a formato json.
        3. Convertir la informacion a una lista de dictionarios.
        4. Unir las dos listas para obtener una lista con toda
        la informacion.
    '''

    # Set the links to extract the information
    url_passengers_2016 = 'http://analytics.deacero.com/Api/GetApi/ApiPasajeros2016/ecfb5fc7-0932-590f-832c-6d6055f2be07' 
    url_passengers_2017 = 'http://analytics.deacero.com/Api/GetApi/ApiPasajeros2017/faabd632-cc39-552d-a68b-02de4242f636'

    # Get the passengers information from the apis  
    info_2016 = requests.get(url_passengers_2016)
    info_2017 = requests.get(url_passengers_2017)

    # Create the lists of passengers
    passengers_2016 = list(info_2016.json())
    passengers_2017 = list(info_2017.json())

    # Merge the lists
    total_passengers = passengers_2016 + passengers_2017

    return total_passengers


def get_flights_info():
    '''
    Get the flights information from the apis
    provided, and returns a list with all
    the information from the flights on
    2016 and 2017 merged.
    '''

    # Set the links to extract the information
    url_flights_2016 = 'http://analytics.deacero.com/Api/GetApi/ApiVuelos2016/9ea3b836-6938-52dc-9626-a8e35db81dd5'
    url_flights_2017 = 'http://analytics.deacero.com/Api/GetApi/ApiVuelos2017/fc126260-1cf8-5a46-995d-ba639ff5868b' 

    # Get the flights information from the apis
    info_2016 = requests.get(url_flights_2016)
    info_2017 = requests.get(url_flights_2017)

    # Create the lists of flights
    flights_2016 = list(info_2016.json())
    flights_2017 = list(info_2017.json())

    # Merge the lists
    total_flights = flights_2016 + flights_2017
    
    return total_flights
 
#url_aerolineas = 'http://analytics.deacero.com/Api/GetApi/ApiLineaAerea/1a8d9e13-ce30-50fc-bf34-6490eb799a75'


def assign_passenger_to_flight(passengers, flights):
    '''
    Assign a passenger to his corresponding flight
    and return a new dictionary will all the 
    information for each flight.
    '''    

    # Create a copy of the original flights
    flights_with_passengers = flights.copy()

    # Look for the passenger key in each flight 
    # and add the passenger information to it.
    for p in passengers:
        for f in flights_with_passengers:
            if p['ID_Pasajero'] in f.values():    
                f.update(p)

    return flights_with_passengers

    



if __name__ == '__main__':
    main()
