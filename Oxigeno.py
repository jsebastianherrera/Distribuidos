import random
from time import sleep
import numpy
from Sensor import Sensor
class Oxigeno(Sensor):
    oxigeno:float
    def __init__(self,  file):
        super().__init__(file)
        self.oxigeno=self.generateValues()
            
    
    def generateValues(self):
        correct,out_of_range,incorrect=super().readFile()
        a=list()
        for i in range(0,int(correct*10)):
            a.append(round(numpy.random.uniform(2.0,11.0),1))
        for i in range(0,int(out_of_range*10)):
            a.append(round(numpy.random.uniform(0.0,1.9),1))
        for i in range(0,int(incorrect*10)):
            a.append(round(numpy.random.uniform(-999,-1),1))                    
        return random.choice(a)
     