import math
from pathlib import Path
import pathlib

def calculate_distance(lat1, lon1, lat2, lon2: int) -> int:
    '''Calculates the great-circle distance between two points given the
    latitudes and longitudes of the points'''
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = math.fabs(lat2 - lat1)
    dlon = math.fabs(lon2 - lon1)

    alat = (lat1 + lat2)/2

    R = 3958.8
    x = dlon*(math.cos(alat))

    d = math.sqrt((x**2) + (dlat**2)) * R

    return d

def round_num(x: float) -> int:
    '''Rounds a float to the nearest integer'''

    if (x - math.floor(x)) < 0.5:
        return math.floor(x)
    else:
        return math.ceil(x)

def determine_aqi(conc: float) -> int:
    '''Calculates the air quality index (AQI) given the concentration of
    pollutants in the air'''
    
    if 0.0 <= conc < 12.1:
        if conc == 0:
            AQI = 0
        else:
            x = 12/conc
            AQI = 50/x
            AQI = round_num(AQI)
    elif 12.1 <= conc < 35.5:
        conc = conc - 12.1
        if conc == 0:
            AQI = 51
        else:
            x = 23.4/conc
            AQI = (50/x) + 51
        AQI = round_num(AQI)
    elif 35.5 <= conc < 55.5:
        conc = conc - 35.5
        if conc == 0:
            AQI = 101
        else:
            x = 20/conc
            AQI = (50/x) + 101
        AQI = round_num(AQI)
    elif 55.5 <= conc < 150.5:
        conc = conc - 55.5
        if conc == 0:
            AQI = 151
        else:
            x = 95/conc
            AQI = (50/x) + 151
        AQI = round_num(AQI)
    elif 150.5 <= conc < 250.5:
        conc = conc - 150.5
        if conc == 0:
            AQI = 201
        else:
            x = 100/conc
            AQI = (100/x) + 201
        AQI = round_num(AQI)
    elif 250.5 <= conc < 350.5:
        conc = conc - 250.5
        if conc == 0:
            AQI = 301
        else:
            x = 100/conc
            AQI = (100/x) + 301
        AQI = round_num(AQI)
    elif 350.5 <= conc < 500.5:
        conc = conc - 350.5
        if conc == 0:
            AQI = 401
        else:
            x = 150/conc
            AQI = (100/x) + 401
        AQI = round_num(AQI)
    elif conc >= 500.5:
        AQI = 501
    
    return AQI

def location_input() -> Path:
    '''Takes laction of center from input and returns path for file if file
    is specified'''
    
    location = str(input())
    location = location.split()
    
    if location[1] == "NOMINATIM":
        location = " ".join(location[2:])
        return location
    elif location[1] == "FILE":
        path = Path(location[2])
        return path

def num_input() -> int:
    '''Takes second, third, fourth input which all return integers'''

    num1 = input()
    num1 = num1.split()

    return int(num1[1])

def aqi_input() -> Path:
    '''Takes input and returns a path if file is specified'''

    AQI = input()
    AQI = AQI.split()

    if AQI[1] == "PURPLEAIR":
        pathname = None
    elif AQI[1] == "FILE":
        pathname = Path(AQI[2])

    return pathname

def reverse_input() -> [Path]:
    '''Takes final input and returns as many paths as necessary in a list'''

    input1 = input()
    input1 = input1.split()

    if input1[1] == "NOMINATIM":
        path_list = None
    elif input1[1] == "FILES":
        path_list = []
        for path_index in range(2, len(input1)):
            path_list.append(Path(input1[path_index]))

    return path_list
