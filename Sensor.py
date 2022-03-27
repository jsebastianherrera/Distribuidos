class Sensor(object):
    
    def __init__(self,time,file):
        self.file=file
        self.time=time
        
    def readFile(self):
        with open(self.file,'r') as f:
            lines=f.readlines()
            correct=float(lines[0].strip())
            out_of_range=float(lines[1].strip())
            incorrect=float(lines[2].strip())
        return correct,out_of_range,incorrect
    

