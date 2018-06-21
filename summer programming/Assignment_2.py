# Joshua Allen
# IS590PR
# Assignment 2


def storm_info(line: str) -> (str, str, int):
    array = line.replace(' ', '').rstrip(',').split(',')
    ID = array[0]
    Name = array[1]
    count = int(array[2])
    return ID, Name, count


def storm_stats(a_list: list, start: str, end: str, max: str, max_date: str, max_time: str, n: int, h:bool) -> list:
    a_list.append(start[4:6] + '-' + start[6:8] + '-' + start[0:4])
    a_list.append(end[4:6] + '-' + end[6:8] + '-' + end[0:4])
    a_list.append(max)
    a_list.append(max_date[4:6] + '-' + max_date[6:8] + '-' + max_date[0:4])
    a_list.append(max_time[0:2] + ':' + max_time[2:4])
    a_list.append(n)
    a_list.append(h)
    return a_list


def process_file(file):
    storm_ID = ""
    storm_name = ""
    n = 0
    start_date = ""
    end_date = ""
    summary = {}
    with open(file) as f:
        for line in f:
            line = line.rstrip('\n')
            if line[0].isalpha():
                storm_ID, storm_name, n = storm_info(line)
                summary[storm_ID] = [storm_name]
            else:
                nextline = line
                max_wind = 0
                max_wind_date = ""
                max_wind_time = ""
                count = 0
                hurricane = False
                for i in range(n):
                    nextline = nextline.replace(' ', '').rstrip(',').split(',')
                    if i == 0:
                        start_date = nextline[0]
                    elif i == n-1:
                        end_date = nextline[0]
                    else:
                        pass
                    if int(nextline[6]) > max_wind:
                        max_wind = int(nextline[6])
                        max_wind_date = (nextline[0])
                        max_wind_time = nextline[1]
                    if nextline[2] == "L":
                        count += 1
                    if nextline[3] == "HU":
                        hurricane = True
                    if i == n-1:
                        pass
                    else:
                        nextline = next(f).rstrip('\n')
                summary[storm_ID] = storm_stats(summary[storm_ID], start_date, end_date, max_wind, max_wind_date, max_wind_time,
                                                count, hurricane)
    return summary


file1 = "C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/hurdat2-1851-2017-050118.txt"
file2 = "C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/hurdat2-nepac-1949-2017-050418.txt"

summary1 = process_file(file1)
summary2 = process_file(file2)

by_year = {}

for storm in summary1:
    date = storm[-4:]
    if date not in by_year:
        by_year[date] = {'storms': 1}
        if summary1[storm][7]:
            by_year[date]['hurricanes'] = 1
    else:
        by_year[date]['storms'] += 1
        if summary1[storm][7]:
            if 'hurricanes' in by_year[date]:
                by_year[date]['hurricanes'] += 1
            else:
                by_year[date]['hurricanes'] = 1

for storm in summary2:
    date = storm[-4:]
    if date not in by_year:
        by_year[date] = {'storms': 1}
        if summary2[storm][7]:
            by_year[date]['hurricanes'] = 1
    else:
        by_year[date]['storms'] += 1
        if summary2[storm][7]:
            if 'hurricanes' in by_year[date]:
                by_year[date]['hurricanes'] += 1
            else:
                by_year[date]['hurricanes'] = 1

for storm in summary1:
    print(storm)
    print(" ".join(str(e) for e in summary1[storm][0:6]))
for storm in summary2:
    print(storm)
    print(" ".join(str(e) for e in summary2[storm][0:6]))

for year in sorted(by_year):
    print(year)
    print("Total storms:        {}".format(str(by_year[year]['storms'])))
    if 'hurricanes' in by_year[year]:
        print('Total hurricanes:    {}'.format(str(by_year[year]['hurricanes'])))
    else:
        print('No hurricanes recorded for this year')
