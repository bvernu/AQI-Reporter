from project3_classes import RegFile, Nominatim, PurpleAirFile, PurpleAir
from project3_functions import calculate_distance, round_num, determine_aqi, location_input, num_input, aqi_input, reverse_input

def run() -> None:
    '''Runs the main program'''

    location = location_input()
    max_dist = num_input()
    threshold = num_input()
    max_num = num_input()
    aqi_path = aqi_input()
    reverse = reverse_input()

    if type(location) == str:
        loc = Nominatim(location)
        loc.build_url(location)
        loc.open_url()
        center_lat, center_lon = loc.coordinates()
        loc.print_coordinates()

        display_name_list = []
    else:
        location = RegFile(location)
        location.open_file()
        center_lat, center_lon = location.coordinates()
        location.print_coordinates()

        display_name_list = []

    if aqi_path == None:
        url = ''
        url = PurpleAir(url)
        url.open_url()
        url.valid_location(threshold, max_dist, center_lat, center_lon)
        url.max_data(max_num)
        coordinate_list = url.valid_data_coordinates()
        
        display_name_list = []
        
        if reverse == None:
            I = 1
            reverse = ''
            reverse = Nominatim(reverse)

            for coordinate in coordinate_list:
                reverse.build_url_reverse(coordinate[0], coordinate[1])
                reverse.open_url()
                displayname = reverse.display_name()
                lat, lon = reverse.coordinates()
                coordinate_display = [lat, lon, displayname]

                display_name_list.append(coordinate_display)
        else:
            for path in reverse:
                path = RegFile(path)
                path.open_file()
                displayname = path.display_name()
                lat, lon = path.coordinates()
                coordinate_display = [lat, lon, displayname]

                display_name_list.append(coordinate_display)
    else:
        I = 2
        aqi_path = PurpleAirFile(aqi_path)
        aqi_path.open_file()
        aqi_path.valid_location(threshold, max_dist, center_lat, center_lon)
        aqi_path.max_data(max_num)
        if reverse == None:
            reverse = ''
            reverse = Nominatim(reverse)
            for coordinate in coordinate_list:
                reverse.build_url_reverse(coordinate[0], coordinate[1])
                reverse.open_url()
                displayname = reverse.display_name()
                lat, lon = reverse.coordinates()
                coordinate_display = [lat, lon, displayname]

                display_name_list.append(coordinate_display)
        else:
            for path in reverse:
                path = RegFile(path)
                path.open_file()
                displayname = path.display_name()
                lat, lon = path.coordinates()
                coordinate_display = [lat, lon, displayname]

                display_name_list.append(coordinate_display)        
    
    if I == 1:
        url.print_valid_locations(display_name_list)
    else:
        aqi_path.print_valid_locations(display_name_list)
        
        

if __name__ == "__main__":
    run()
