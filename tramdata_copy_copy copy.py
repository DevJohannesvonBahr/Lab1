import os
import json
from haversine import haversine, Unit

os.chdir("/Users/jvbahr/Library/CloudStorage/OneDrive-Personal/PythonKurs/Fortsättning/Lab1")

def build_tram_stops(jsonobject): 

    with open(jsonobject) as file: 
        data = json.load(file)
        #print(data.keys())
        #print("test:    " ,data["Ullevi Norra"])
        stopdict = {}
        for each_stop_key in data: 
            stopdict.setdefault(each_stop_key, None)
            position_list = data[each_stop_key]["position"]     #['57.7511423', '12.0713114']
            lat, lon = float(position_list[0]), float(position_list[1])
            
            stopdict[each_stop_key] = {"lat": lat, "lon": lon}


        #print(json.dumps(stopdict, indent=4)) #verkar funka. 
        return stopdict
    


def build_tram_lines(lines): 

    
    with open(lines) as file: 
        linedict = {} 
        timedict = {}

        for each_line in file: 
            
            if each_line.strip().endswith(":"):
                current_key = each_line[0:each_line.find(":")]
                linedict[current_key] = []
                previous_station = None
                previous_time = None

            elif len(each_line) != 1:           # de helt tomma raderna innehåller bara ett space enl test med .isspace()
                station_name = each_line[0:each_line.rfind(" ")].rstrip()
                station_time = int(each_line[-3:])
                linedict[current_key].append(station_name)

                
        
                if previous_station is not None: 
                    timediff = abs(previous_time - station_time)

                    if previous_station not in timedict: 
                        timedict[previous_station] = {}
                    
                    timedict[previous_station][station_name] = timediff


                previous_station, previous_time = station_name, station_time

        
        #print(json.dumps(timedict, indent=4))
        

        return {"linedict": linedict, "timedict": timedict}

            
                




def build_tram_network(stopfile, linefile): 

    maindict = {
        "stops": build_tram_stops(stopfile), 
        "lines": build_tram_lines(linefile)["linedict"], 
        "times": build_tram_lines(linefile)["timedict"]
    }

    with open("tramnetwork.json", "w") as file:
        json.dump(maindict, file)

    return file



def lines_via_stop(linedict, stop): 
    lines_via_stop_list = []
    for key, value in linedict.items(): 
        if stop in value: 
            lines_via_stop_list.append(key)
    sorted_list = sorted(lines_via_stop_list, key=int) 
    #print(sorted_list)
    return sorted_list



def lines_between_stops(linedict, stop1, stop2):
    lines_between_stops = []

    for each_linje, station_list in linedict.items(): 

        if stop1 in station_list and stop2 in station_list: 
            lines_between_stops.append(each_linje) 


    if lines_between_stops == []: return "inga linjer mellan"   
    
    sorted_list = sorted(lines_between_stops, key=int) 
    return sorted_list




def time_between_stops(linedict, timedict, line, stop1, stop2):
    summed_time = 0
    current_line_list = linedict[line]
    if not (stop1 and stop2 in current_line_list): 
        print("error") 
        return

    startindex = current_line_list.index(stop1)
    slutindex = current_line_list.index(stop2)
    
    if startindex < slutindex: rutt_list = current_line_list[startindex:slutindex+1]
    elif startindex > slutindex: rutt_list = current_line_list[slutindex:startindex+1] #eftersom vi vet att samma mellan a och b samt b och a. 
    elif startindex == slutindex: rutt_list = current_line_list[startindex:slutindex+1]
    
    #print(rutt_list)

    previous_station = None

    for each_station in rutt_list: 
        current_station = each_station

        if previous_station is not None: 
            time_between = timedict[previous_station][current_station]
            type(time_between)
            summed_time += time_between

        previous_station = current_station #sista är att current blir previous. Varje ny loop ger NY current. 

    #print(summed_time)
    return summed_time



def distance_between_stops(stopdict, stop1, stop2): 

    lat1 = float(stopdict[stop1]["lat"])
    lon1 = float(stopdict[stop1]["lon"])
    lat2 = float(stopdict[stop2]["lat"])
    lon2 = float(stopdict[stop2]["lon"])
    stop1cords = (lat1, lon1)
    stop2cords = (lat2, lon2)

    distance = haversine(stop1cords, stop2cords)

    return distance




def dialouge(tramfile): 
    
    with open(tramfile) as file:
        data = json.load(file)
    
    stopdict = data["stops"]
    linedict = data["lines"]
    timedict = data["times"]


    while True: 
        query = input(">")
        if query.strip().lower() == "quit": 
            break 


        #via        
        if query.startswith("via "): 
            station = query.strip()[4:]
            
            if station not in stopdict: #kollar ifall station ens finns. 
                print("unknown arguments")
                continue

            lines_via = lines_via_stop(linedict, station)
            print(lines_via)
            return lines_via

        #between

        elif query.startswith("between ") and " and " in query:
             and_startindex = query.find(" and ")
             stop1 = query[8: and_startindex].strip()
             stop2 = query[and_startindex+5: ].strip()

             if stop1 not in stopdict or stop2 not in stopdict: 
                print("unknown parameters")
                continue 

             #print(stop1, " -> ", stop2)
             linjer_mellan_stop1_stop2 = lines_between_stops(linedict, stop1, stop2)
             
             print(linjer_mellan_stop1_stop2)
             return linjer_mellan_stop1_stop2



        elif query.startswith("time with ") and " from " in query and " to " in query: 

            from_startindex = query.find(" from ")
            to_startindex = query.find(" to ")
            
            linje = query[10: from_startindex]
            stop1 = query[from_startindex+6: to_startindex]
            stop2 = query[to_startindex+4: ]

            if linje not in linedict or stop1 not in stopdict or stop2 not in stopdict: 
                print("unknown parameters")
                continue 

            time = time_between_stops(linedict, timedict, linje, stop1, stop2)
            #print(stop1, "  ->   ", stop2, "linje: ", linje)
            print(time)
            return time

        

        elif query.startswith("distance from ") and " to " in query:
        
            to_startindex = query.find(" to ")
            stop1 = query[14:to_startindex]
            stop2 = query[to_startindex+4:]
        
            if stop1 not in stopdict or stop2 not in stopdict: 
                print("unknown argument")
                continue

            #print(stop1, "   ", stop2) 

            distance = distance_between_stops(stopdict, stop1, stop2)

            print(distance)
            return 



        
        else: print("sorry, try again")

        #time >between Östra SjukhusetandOpaltorget



        #distance from



        #quit

#answer_query("tramsnetwork.json", "with time 1 from Östra Sjukhuset to Östra Sjukhuset")




   
    
   
    

    





#------------

linedict = build_tram_lines("tramlines.txt")["linedict"]
timedict = build_tram_lines("tramlines.txt")["timedict"]
stopdict = build_tram_stops("tramstops.json")

#lines_via_stop(linedict, "Opaltorget")
"""
print(time_between_stops(linedict, timedict, "5", "Varmfrontsgatan", "Östra Sjukhuset"))
print(time_between_stops(linedict, timedict, "5", "Östra Sjukhuset", "Varmfrontsgatan"))

print(time_between_stops(linedict, timedict, "7", "Opaltorget", "Komettorget"))
print(time_between_stops(linedict, timedict, "7", "Komettorget", "Opaltorget"))
"""

dialouge("tramnetwork.json")






"""""
Test: Maximal tid mellan. Ska inte överstiga 63 min eler ngt sådant. 
"""