class Monitor:  
    def __init__(self,type):
        self.type=type
        
    def checkQualityParameters(self,value:float,type='Ph'):
        if value >= 6.0 and value<=8.0:
            return True
        return False
    def checkQualityParameters(self,value:float,type='Temperatura'):
        if value >= 68 and value<=89:
            return True
        return False
    def checkQualityParameters(self,value:float,type='Oxigeno'):
        if value >= 2 and value<=11:
            return True
        return False

m=Monitor('Oxigeno')
print(m.checkQualityParameters(6,m.type))