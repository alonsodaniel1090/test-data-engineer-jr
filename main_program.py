import requests
import pandas as pd



def main():
    ''' Main prrogram process '''

    # Get the information from passengers and flights 
    passengers = get_passengers_info()
    flights  = get_flights_info()

    # Assign the passengers to their flights
    flights_with_passengers = assign_passenger_to_flight(passengers, flights)
    
    # Assign the airline for each flight
    info_with_airlines = assign_airline(flights_with_passengers)
    info_formatted = format_results(info_with_airlines)

    # Show the results
    results = get_price_mean_by_semester(info_formatted)
    print(results)


    



def get_passengers_info():
    '''
     Get the flights information from the apis
    provided, and returns a list with all
    the information from the flights on
    2016 and 2017 merged. 
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

    
def assign_airline(flights):
    '''
    Assign the airline to each flight, if the
    airline is unknown, assign "other" as 
    the value.
    '''

    # Create a copy of the flights
    flights_with_passengers = flights.copy() 
    
    # Set the links to extract the information
    url_aerolineas = 'http://analytics.deacero.com/Api/GetApi/ApiLineaAerea/1a8d9e13-ce30-50fc-bf34-6490eb799a75'

    # Get the flights information from the apis 
    info_aerolineas = requests.get(url_aerolineas)

    # Create the information as a list
    aerolineas = list(info_aerolineas.json())

    # Create a new dictionary with the value of other.
    otro = {'Code':'OT', 'Linea_Aerea':'Otra'}

    # Assign the airline to the corresponding flight
    for f in flights_with_passengers:
        for a in aerolineas:
            if f['Cve_LA'] in a.values():    
                f.update(a)

    # Check if no airline has been assigned
    # and if it doesn't, assign other as
    # the value
    for f in flights_with_passengers:
        if 'Linea_Aerea' not in f.keys():
            f.update(otro)

    return flights_with_passengers
    
    
def format_results(info_with_airlines):
    '''
    Receives the the complete information
    about the passenger, flight and airlines
    and returns only the necessary columns
    for the analysis.
    '''
    info = info_with_airlines.copy()

    for i in info: 
        del(i['Cve_LA']) 
        del(i['Cve_Cliente']) 
        del(i['ID_Pasajero']) 
        del(i['Pasajero'])
        del(i['Code'])
    
    return info 

def get_price_mean_by_semester(info_formatted):
    '''
    Calculates the mean price by year, 
    semester, class, route an airline
    and return a pandas dataframe
    with the results.
    ''' 
    for info in info_formatted:
        d = {}
        date= info['Viaje']
        year = date[-4:]

        if '/'in date[:2]:
            month = date[:1]
        else:
            month = date[:2]
        if int(month) <= 6:
            d['Year'] = year
            d['Semester'] = '1 semester'
        else:
            d['Year'] = year
            d['Semester'] = '2 semester'
        info.update(d)

    # Set the option to show all the results with pandas
    pd.set_option('display.max_rows', None)

    # Create the data frame
    df = pd.DataFrame(info_formatted)
    
    # Calculate the mean with the parameters needed
    results = df.groupby(['Year', 'Semester','Clase','Ruta','Linea_Aerea']).agg('Precio').mean()

    print(results) 





if __name__ == '__main__':
    main()
