class Monitor:
    def checkQualityParameters(self, value: float, type):
        if type == "Ph":
            if value >= 6.0 and value <= 8.0:
                return True
            return False
        elif type == "Temperatura":
            if value >= 68.0 and value <= 89.0:
                return True
            return False

        elif type == "Oxigeno":
            if value >= 2 and value <= 11:
                return True
            return False
        return False
