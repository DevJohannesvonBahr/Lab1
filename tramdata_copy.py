import os
import json


os.chdir("/Users/jvbahr/Library/CloudStorage/OneDrive-Personal/PythonKurs/Fortsättning/Lab1")
"""
3 dictionary building functions
4 extracting from dict functions
1 dialogue function (two parts)
"""

def build_tram_stops(jsonobject): 
    """
    builds a "stop dictionary". Keys är namnet på tram stops. Values är ytterligare en dict med latitud och longitud. Såhär ser 
    ett key-value pair ut: 
    
    'Majvallen': {'lat': 57.6909343, 'lon': 11.9354935}

    argumentet jsonobject är given tramstops.json vilket är en mkt standardiserad json-fil med rådata, som extractas mha json-library!

    tänker att en for loop som loopar genom ytligaste nivån i json-filen räcker för att skapa keys, sedan values från nästa nivå. 
    """


    with open(jsonobject, "r") as file: 
        data = json.load(file)
        #print(data.keys())
        #print("test:    " ,data["Ullevi Norra"])
        stopdict = {}
        for each_stop_key in data: 
            stopdict.setdefault(each_stop_key, None)
            position_list = data[each_stop_key]["position"]     #['57.7511423', '12.0713114']
            stopdict[each_stop_key] = {"lat": position_list[0], "lon": position_list[1]}


        #print(json.dumps(stopdict, indent=4)) #verkar funka. 
        return stopdict
    


def build_tram_lines(lines): 
    """build a line dictionary
    Keys är NAMNEN på de olika linjerna, tex 7an eller 5ans spårvagn har namnen "7" och "5". 

    Values är lisor med linjens stopp-stationer! Det var dessa som angavs som keys i funktionen ovan. Men varje linjes tillhörande 
    stationer fås från en txt-fil. Här finns även stoptider med utgång 10:00. 
    ----
    Sedan börjar vi med första. Kollar ifall denna återfinns i listan av stationer. Sedan så kollar vi i vilka Lines som denna återfinns. 
    När vi hittat vilka lines som är relevanta tar vi alla unika stationer från dessa tex 3st lines. Sedan tar vi fram 
    

    """
    with open(lines, "r", encoding="utf-8") as file: 
        linedict = {}
        timedict = {}
        temptime = {}
        temp = []
        
        current_key = None


        for each_line in file: 
            
            if each_line.strip("\n").endswith(":"):
                current_key = each_line[0:each_line.find(":")]
                linedict[current_key] = []
            elif len(each_line) != 1:           # de helt tomma raderna innehåller bara ett space enl test med .isspace()
                station_name = each_line[0:each_line.rfind(" ")].rstrip()
                station_time = each_line[-3:]
                
                linedict[current_key].append(station_name)
                temptime[station_name] = int(each_line[-3:])
                

        for stationer_list in linedict.values(): 
            i=0

            while i != len(stationer_list) - 1: #Fail när i+1 inte hade funnits. 

                current_station = stationer_list[i]
                next_station = stationer_list[i+1]
            
                if current_station not in timedict: 
                    timedict[current_station] = {}
                
                
                timedict[current_station][next_station] = (temptime[next_station],  temptime[current_station])

                i+=1
                 

        
        print(json.dumps(timedict, indent=4))
    
        return {"linedict": linedict, "timedict": timedict}
        

    
            
            
            
                




def build_tram_network(stopfile, linefile): 
    """
    känns lite svår. Vi får alltså tids-info från txt-filen, samt vilka stationer som tillhör vilken linje. För varje unik station
    ska nu vara en key. Value är sedan en ytterligare dictionary. I denna ska det vara keys som för det första är stationer som då 
    faktiskt går att komma till från vald station. Detta är svårt. Hur ska man hitta dessa keys? 

    Man får en station, tex Centralstationen. Sedan ska man alltså hitta alla stationer som faktiskt är anslutna till denna. Detta är möjligt genom att 
    identifiera alla de linjer som faktiskt innehåller "Centralstationen". Då får vi tex 1,2,3,7,9,10,11,13. Nu när vi väl har dessa så kommer alla UNIKA 
    stationer i alla dessa linjer att kunna nås. När detta sedan är gjort får man bara ta respektive av dessa som faktiskt går att nå och ta ut differensen 
    mellan denna och den angivna stationen. Borde funka. 



    """
    maindict = {
        "stops": build_tram_stops(stopfile), 
        "lines": build_tram_lines(linefile)[0], 
        "times": build_tram_lines(linefile)[1]
    }

    with open("tramnetwork.json", "w") as file:
        json.dump(maindict, file)

    return file



def lines_via_stop(linedict, stop): 
    lines_via_stop_list = []
    for key, value in linedict.items(): 
        if stop in value: 
            lines_via_stop_list.append(key)
    print(lines_via_stop_list.sort())



def lines_between_stops(linedict, stop1, stop2):
    lines_between_stops_list = []
    for key, value in linedict.items(): 
        if stop1 and stop2: 
            pass




def time_between_stops(linedict, timedict, line, stop1, stop2):
    current_line_list = linedict[line]
    if not (stop1 and stop2 in current_line_list): print("error")

    startindex = current_line_list.index(stop1)
    slutstation_index = current_line_list.index(stop2)
    
    summed_time = 0
    for i in range(startindex, slutstation_index + 1): 

        current_station = current_line_list[i]
        next_station = current_line_list[i+1]

        deltid = timedict[current_station][next_station]
        summed_time += deltid

    print(summed_time)    



    


#time_between_stops(build_tram_lines("tramlines.txt")["linedict"], build_tram_lines("tramlines.txt")["timedict"], "1", "Tingvallsvägen", "Järntorget")
build_tram_lines("tramlines.txt")["timedict"]












#print(json.dumps(build_tram_lines("tramlines.txt")[1], indent=4))



    









