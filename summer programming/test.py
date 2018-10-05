## IS590PR Assignment #2
## Nicholas Wolf
## Summer 2018

# !/usr/bin/python3


# This function reads in the data files one line at a time and updates a dictionary (cy_data) that organizes all data for all cyclones
# Lines starting with an A, E, or C alpha character are presumed to be the cyclone metadata line. Those lines are split and the data points assigned to the appropriate metadata keys
# Remaining lines following an alpha line are presumed to be the measurement points, and are grouped together as a list of row-lists and set to the "data" key of the cy_data cyclone record.
# The updated cy_data dictionary is then returned

def read_data(cy_data, fpath):
    with open(fpath) as file:
        for line in file:
            if line[0] in ['A', 'E', 'C']:
                cy_id, cy_name, data_length = line.split(',')[0].strip(), line.split(',')[1].strip(), line.split(',')[
                    2].strip()
                cy_data[cy_id] = {'name': cy_name, 'num_records': data_length, 'data': []}
            else:
                cy_data[cy_id]['data'].append([i.strip() for i in line.rstrip(',\n').split(',')])
    return cy_data


# This function examines each cyclone dictionary object, looks at its data points, an updates the cyclone's record
# with further metadata explaining its start and stop times.

def get_date_range(cy):
    return {'start_date': {'year': cy['data'][0][0][0:4],
                           'month': cy['data'][0][0][4:6],
                           'day': cy['data'][0][0][6:]},
            'end_date': {'year': cy['data'][-1][0][0:4],
                         'month': cy['data'][-1][0][4:6],
                         'day': cy['data'][-1][0][6:]}}


# This function looks at each cyclone's data points (fed as a list-of-lists) and returns a metadata record (dictionary object)
# that provides the cyclone's max wind speed and time it occurred. Returns none if no max wind speed found

def get_max_wind(cy_points):
    max_wind = (0, 0, 0)
    for row in cy_points:
        try:
            if int(row[6]) > max_wind[0]:
                max_wind = (int(row[6]), row[0], row[1])
        except ValueError:
            continue
    if max_wind[0] > 0:
        return {'speed': str(max_wind[0]), 'year': max_wind[1], 'time': max_wind[2]}
    else:
        return 'NONE'


## This function looks at each cyclone's data points (fed as a list-of-lists) and counts the number of times a landfall occurred (L in column 3)
## Returns another dictionary to add to the cyclone's metadata

def count_landfall(cy_points):
    count = 0
    for row in cy_points:
        if row[2] == 'L':
            count += 1
    return {'number_landfalls': count}


## Quick function to check the cyclone's data points to see if it ever reached hurricane status. Returns True or False

def check_hurricane(cy_points):
    for row in cy_points:
        if row[3] == 'HU':
            return True
    return False


## Function to handle the print out of the information as each file line is processed

def print_cy_info(cy_dict, cyclone):
    name = cy_dict['name'] if cy_dict['name'] != 'UNNAMED' else 'None'
    max_wind_knots = cy_dict['max_wind']['speed'] + ' knots,  first occurred on ' + \
                     cy_dict['max_wind']['year'][4:6] + '/' + cy_dict['max_wind']['year'][6:] + '/' + \
                     cy_dict['max_wind']['year'][0:4] + ' at ' + cy_dict['max_wind']['time'] + \
                     ' hours' if cy_dict['max_wind'] != 'NONE' else 'N/A'
    print("Processing storm id: {}, name: {}. Occured between {}/{}/{} and {}/{}/{}. \
     Maximum sustained winds: {}. Landfall made {} times".format(cyclone, name,
                                                                 cy_dict['start_date']['month'],
                                                                 cy_dict['start_date']['day'],
                                                                 cy_dict['start_date']['year'],
                                                                 cy_dict['end_date']['month'],
                                                                 cy_dict['end_date']['day'],
                                                                 cy_dict['end_date']['year'],
                                                                 max_wind_knots,
                                                                 str(cy_dict['number_landfalls'])))


cy_data = {}
storm_counter = {}  # This is effectively a counter object to help us count total number of storms
hurricane_counter = {}  # Same, to count number of cyclones that were hurricanes

## First part processes each of the two files and creates the single data container for all storms

for file_name in ['hurdat2-1851-2017-050118.txt', 'hurdat2-nepac-1949-2017-050418.txt']:
    fpath = 'C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/' + file_name
    cy_data = read_data(cy_data, fpath)

for cyclone in cy_data:

    ## Now that we have basic data read in, we add additional metadata about each storm, and print out our basic storm information

    cy_data[cyclone].update(get_date_range(cy_data[cyclone]))
    cy_data[cyclone].update({'max_wind': get_max_wind(cy_data[cyclone]['data'])})
    cy_data[cyclone].update(count_landfall(cy_data[cyclone]['data']))
    print_cy_info(cy_data[cyclone], cyclone)

    ## Next, for each cyclone, we do our counts of storms and hurricanes

    try:
        storm_counter[cy_data[cyclone]['start_date']['year']] += 1
    except KeyError:
        storm_counter[cy_data[cyclone]['start_date']['year']] = 1
    if check_hurricane(cy_data[cyclone]['data']):
        try:
            hurricane_counter[cy_data[cyclone]['start_date']['year']] += 1
        except KeyError:
            hurricane_counter[cy_data[cyclone]['start_date']['year']] = 1

print("\nStorms per year")

for storm_year in sorted(storm_counter):
    print("{}: {} storms".format(storm_year, str(storm_counter[storm_year])))

print("\nHurricanes per year")

for hurricane_year in sorted(hurricane_counter):
    print("{}: {} hurricanes".format(hurricane_year, str(hurricane_counter[hurricane_year])))

def func(tail:str) -> float:
    return float(tail[0])