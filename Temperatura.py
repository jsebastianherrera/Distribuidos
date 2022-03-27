import random
from time import sleep
import numpy
from Sensor import Sensor
class Temperatura(Sensor):
    fahrenheit:float
    def __init__(self, time, file):
        super().__init__(time, file)
        while True:
            self.fahrenheit=self.generateValues()
            print('send alert')
            sleep(super().time)
                
    def generateValues(self):
        correct,out_of_range,incorrect=super().readFile()
        a=list()
        for i in range(0,int(correct*10)):
            a.append(round(numpy.random.uniform(68,89),1))
        for i in range(0,int(out_of_range*10)):
            a.append(round(numpy.random.uniform(0.0,59.9),1))
        for i in range(0,int(incorrect*10)):
            a.append(round(numpy.random.uniform(-999,-1),1))                    
        return random.choice(a)
     