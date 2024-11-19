import unittest
#from tramdata import *
from tramdata_copy_copy_copy import *

#/Users/jvbahr/Library/CloudStorage/OneDrive-Personal/PythonKurs/Fortsättning/Lab1/tramdata_copy_copy_copy.py

""" #called b4 every other method! Verkar som att den kallas en gång för varje method. setUp har en motsvarande tearDown som körs (en)? gång sist?
måste använda prefixet test_
unittest.main() verkar bara köra alla test.

setUp laddar in stopdict och linedict
"""

TRAM_FILE = './tramnetwork.json'
TRAM_FILE = "tramnetwork.json"



class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict["times"] #tillagd
            self.list_tramlines = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "13"]    #hardcoded list of desired lines that are found in the .txt file. Used to see if all are in the created linedict
            self.highest_time_between_two_stops = 63
            

    def test_stops_exist(self): 
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

        
    # add your own tests here

    def test_distance(self): 
        
        for stop1 in self.stopdict: 
            
            for stop2 in self.stopdict: 
                distance = distance_between_stops(self.stopdict, stop1, stop2)

                self.assertLess(distance, 20) #19 leder till fail. 


    def test_same_time_between_a_b(self): 
        
        for linje in self.linedict:
            linjens_stops_lista = self.linedict[linje]
            for stop1 in linjens_stops_lista:
                for stop2 in linjens_stops_lista:
                
                    time_a_b = time_between_stops(self.linedict, self.timedict, linje, stop1, stop2)
                    time_b_a = time_between_stops(self.linedict, self.timedict, linje, stop2, stop1)
                    self.assertEqual(time_a_b, time_b_a, "verkar fel")


    def test_all_tramlines_included(self): #baseras på att vi vet hardcoded lista med alla linjer som ska vara med. Kollar för varje linje i denna lista ifall de faktiskt finns i den linedict vi skapat!
        
        
            linedict_linjer_som_finns = list(self.linedict.keys())
            #print(linedict_linjer_som_finns)
            for each_linje in self.list_tramlines: 
                self.assertIn(each_linje, linedict_linjer_som_finns)
                

    def test_all_stations_from_textfile_in_linedict(self): #Kollar antalet rader med stationer i txt-files. Se ifall det motsvarar antalet rader i linedict. 
        
        with open("tramlines.txt") as file: 
            antal_stationer_in_file=0
            for each_line in file: 
                if (not each_line.strip().endswith(":")) and (not each_line.strip() == ""): #ignorerar linjer och "" samt \n
                    antal_stationer_in_file += 1
            
            antal_stationer_in_linedict = 0
            for value in self.linedict.values(): 
                antal_stationer_in_linedict += len(value)
    
            #print(sum)
            self.assertEqual(antal_stationer_in_file, antal_stationer_in_linedict)


    def test_all_time(self):
          
        for linje in self.linedict:
            linjens_stops_lista = self.linedict[linje]
            for stop1 in linjens_stops_lista:
                for stop2 in linjens_stops_lista:

                    time_between = time_between_stops(self.linedict, self.timedict, linje, stop1, stop2)
                    
                    self.assertLess(time_between, self.highest_time_between_two_stops+1)

        
    


   
        
        
        

    




    
    





        

        


    




        


        
            

        


if __name__ == '__main__':
    unittest.main(exit=False)

    
