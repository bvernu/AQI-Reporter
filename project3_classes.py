import math
from pathlib import Path
import pathlib
import json
import urllib.parse
import urllib.request
from project3_functions import calculate_distance, round_num, determine_aqi

class RegFile:
    '''Deals with files used as a substitute instead of using Nominatim and for
    files used when reverse geocoding'''

    def __init__(self, path = '', text = [], lat = 0, lon = 0, displayname = ''):
        '''Initializes all necessary terms'''
        
        self.path = path
        self.text = text
        self.lat = lat
        self.lon = lon
        self.displayname = displayname
    
    def open_file(self) -> None:
        '''Opens a file given the path and creates a list of all lines within
        the file as json'''

        try:
            text = []
            f = self.path.open('r')
            json_text = f.read()
            for line in f:
                text.append(line)

            self.text = json.loads(json_text)
        except FileNotFoundError:
            print("FAILED")
            print("MISSING")
            quit()
        except IOError:
            print("FAILED")
            print("FORMAT")
            quit()
        finally:
            f.close()

    def coordinates(self) -> None:
        '''Returns the latitude and longitude given the text in a file'''

        if type(self.text) == list:
            text = self.text[0]
            text = dict(text)
        elif type(self.text) == dict:
            text = self.text
        
        
        lat = float(text["lat"])
        lon = float(text["lon"])

        self.lat = lat
        self.lon = lon

        return self.lat, self.lon

    def print_coordinates(self) -> None:
        '''Prints the coordinates (latitude and longitude)'''

        lat = self.lat
        lon = self.lon
        
        if lat < 0:
            lat = math.fab(lat)
            if lon < 0:
                lon = math.fabs(lon)
                print(f"CENTER {lat}/S {lon}/W")
            else:
                print(f"CENTER {lat}/S {lon}/E")
        else:
            if lon< 0:
                lon = math.fabs(lon)
                print(f"CENTER {lat}/N {lon}/W")
            else:
                print(f"CENTER {lat}/N {lon}/E")

    def display_name(self) -> None:
        '''Returns the diplay name as a string. To be used for reverse files'''

        text = self.text
        
        displayname = text["display_name"]
        self.displayname = displayname

        return self.displayname

class Nominatim():
    '''Used when Nominatim is accessed'''

    def __init__(self, url = '', text = [], lat = 0, lon = 0, displayname = ''):
        '''Initializes all necessary terms'''
        
        self.url = url
        self.text = text
        self.lat = lat
        self.lon = lon
        self.displayname = displayname

    def build_url(self, location: str) -> None:
        '''Builds the url needed to search for the location given by the user'''

        try:
            url = self.url
            base_url = 'https://nominatim.openstreetmap.org/search?'
            parameters = [('q', location), ('format', 'json')]
            query_parameter = urllib.parse.urlencode(parameters)

            url = base_url + query_parameter
            self.url = url
        except:
            print("FAILED")
            print("404")
            print("NETWORK")
            quit()

    def build_url_reverse(self, lat: float, lon: float) -> None:
        '''Builds the url needed to reverse geocode a location description from
        the latitude and longitude provided'''

        try:
            url = self.url
            base_url = 'https://nominatim.openstreetmap.org/reverse?'
            parameters = [('lat', lat), ('lon', lon), ('format', 'json')]
            query_parameter = urllib.parse.urlencode(parameters)

            url = base_url + query_parameter
            self.url = url
        except:
            print("FAILED")
            print("404")
            print("NETWORK")

    def open_url(self) -> None:
        '''Opens a file given the path and creates a list of the lines of text
        in the json'''

        response = None
        
        try:
            url = self.url
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')

            self.text = json.loads(json_text)
            status_code = response.getcode()
        except:
            print("FAILED")
            print(status_code)
            if status_code == '404':
                print("NETWORK")
                quit()
            elif status_code != '200':
                print("Not 200")
                quit()
        finally:
            if response != None:
                response.close()

    def coordinates(self) -> None:
        '''Returns the latitude and longitude given the text in a web api'''

        if type(self.text) == list:
            text = self.text[0]
            text = dict(text)
        elif type(self.text) == dict:
            text = self.text
        
        
        lat = float(text["lat"])
        lon = float(text["lon"])

        self.lat = lat
        self.lon = lon

        return self.lat, self.lon

    def print_coordinates(self) -> None:
        '''Prints the coordinates (latitude and longitude)'''

        lat = self.lat
        lon = self.lon
        
        if lat < 0:
            lat = math.fab(lat)
            if lon < 0:
                lon = math.fabs(lon)
                print(f"CENTER {lat}/S {lon}/W")
            else:
                print(f"CENTER {lat}/S {lon}/E")
        else:
            if lon< 0:
                lon = math.fabs(lon)
                print(f"CENTER {lat}/N {lon}/W")
            else:
                print(f"CENTER {lat}/N {lon}/E")

    def display_name(self) -> None:
        '''Returns the diplay name as a string. To be used for reverse files'''

        text = self.text
        
        displayname = text["display_name"]
        self.displayname = displayname

        return self.displayname

class PurpleAirFile:
    '''Used when dealing with files that substitude calling the PurpleAir web API'''

    def __init__(self, path = '', text = {}, data = [], valid_data = [], max_valid_data = []):
        '''Initializes all necessary parameters'''

        self.path = path
        self.text = text
        self.data = data
        self.valid_data = valid_data
        self.max_valid_data = max_valid_data
        

    def open_file(self) -> None:
        '''Opens a file and prepares it to be used'''
        try:
            self.path = Path(self.path)
            f = self.path.open('r', encoding="utf8")
            json_text = f.read()
            
            self.text = json.loads(json_text)
            self.data = self.text["data"]
        except FileNotFoundError:
            print("FAILED")
            print("MISSING")
            quit()
        except IOError:
            print("FAILED")
            print("FORMAT")
            quit()
        finally:
            f.close()

    def valid_location(self, threshold: int, max_dist, center_lat, center_lon) -> None:
        '''Creates a list of the locations that match the requirements given by
        the user when given the text of a file with data from a previous PurpleAir
        sensor'''

        valid_data = []
        
        for element in self.data:
            
            if element[1] == None or element[4] == None or element[25] == None or element[27] == None or element[28] == None:
                continue
            
            concentration = int(element[1])
            age = int(element[4])
            Type = int(element[25])
            lat = float(element[27])
            lon = float(element[28])

            if age < 3600:
                if Type == 0:
                    aqi = determine_aqi(concentration)
                    if aqi >= threshold:
                        element[1] = aqi
                        distance = calculate_distance(lat, lon, center_lat, center_lon)
                        if distance <= max_dist:
                            valid_data.append(element)
                            
        self.valid_data = valid_data


    def max_data(self, max_num: int) -> None:
        '''Sorts valid data points and appends the max number of points to a list.'''

        self.max_valid_data = []
        self.valid_data.sort(key = lambda x: x[1])
        self.valid_data.reverse()

        if max_num > len(self.valid_data):
            self.max_valid_data = self.valid_data
        else:
            for i in range(max_num):
                self.max_valid_data.append(self.valid_data[i])
            
    def print_valid_locations(self, display_name_list: list) -> None:
        '''Prints valid locations with AQI, coordinates, and their description'''

        i = 0
        for element in self.max_valid_data:
            print(f"AQI {element[1]}")

            lat = element[27]
            lon = element[28]

            if lat < 0:
                lati = math.fab(lat)
                if lon < 0:
                    long = math.fabs(lon)
                    print(f"{lati}/S {long}/W")
                else:
                    long = lon
                    print(f"{lati}/S {long}/E")
            else:
                lati = lat
                if lon< 0:
                    long = math.fabs(lon)
                    print(f"{lati}/N {long}/W")
                else:
                    long = lon
                    print(f"{lati}/N {long}/E")

            print(display_name_list[i][2])
            i += 1

class PurpleAir():

    def __init__(self, url = '', text = {}, data = [], valid_data = [], max_valid_data = [], coordinates = []):
        '''Initializes all necessary parameters'''

        self.url = url
        self.text = text
        self.data = data
        self.valid_data = valid_data
        self.max_valid_data = max_valid_data
        self.coordinates = coordinates
        

    def open_url(self) -> None:
        '''Opens a url and prepares it to be used'''

        response = None
        
        try:
            url = self.url
            url = 'https://www.purpleair.com/data.json'

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            
            self.text = json.loads(json_text)
            self.data = self.text["data"]
        except:
            print("FAILED")
            status_code = response.getcode()
            print(status_code)
            if status_code == '404':
                print("NETWORK")
                quit()
            elif status_code != '200':
                print("Not 200")
                quit()
        finally:
            if response != None:
                response.close()

    def valid_location(self, threshold: int, max_dist, center_lat, center_lon) -> None:
        '''Creates a list of the locations that match the requirements given by
        the user when given the text of a file with data from a previous PurpleAir
        sensor'''

        valid_data = []
        
        for element in self.data:
            
            if element[1] == None or element[4] == None or element[25] == None or element[27] == None or element[28] == None:
                continue
            
            concentration = int(element[1])
            age = int(element[4])
            Type = int(element[25])
            lat = float(element[27])
            lon = float(element[28])

            if age < 3600:
                if Type == 0:
                    aqi = determine_aqi(concentration)
                    if aqi >= threshold:
                        element[1] = aqi
                        distance = calculate_distance(lat, lon, center_lat, center_lon)
                        if distance <= max_dist:
                            valid_data.append(element)
                            
        self.valid_data = valid_data


    def max_data(self, max_num: int) -> None:
        '''Sorts valid data points and appends the max number of points to a list.'''

        self.max_valid_data = []
        self.valid_data.sort(key = lambda x: x[1])
        self.valid_data.reverse()

        if max_num > len(self.valid_data):
            self.max_valid_data = self.valid_data
        else:
            for i in range(max_num):
                self.max_valid_data.append(self.valid_data[i])

    def valid_data_coordinates(self) -> list:
        coordinates = self.coordinates
        for element in self.max_valid_data:
            coordinates.append([element[27], element[28]])

        self.coordinates = coordinates
        return self.coordinates
            
    def print_valid_locations(self, display_name_list: list) -> None:
        '''Prints valid locations with AQI, coordinates, and their description'''

        i = 0
        for element in self.max_valid_data:
            print(f"AQI {element[1]}")

            lat = element[27]
            lon = element[28]

            if lat < 0:
                lati = math.fab(lat)
                if lon < 0:
                    long = math.fabs(lon)
                    print(f"{lati}/S {long}/W")
                else:
                    long = lon
                    print(f"{lati}/S {long}/E")
            else:
                lati = lat
                if lon< 0:
                    long = math.fabs(lon)
                    print(f"{lati}/N {long}/W")
                else:
                    long = lon
                    print(f"{lati}/N {long}/E")

            print(display_name_list[i][2])
            i += 1
