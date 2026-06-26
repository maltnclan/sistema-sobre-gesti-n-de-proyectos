class Usuario:
    def __init__(self):
        self.rut = ""
        self.perfil = 0

    # Setters (para guardar los datos)
    def setRut(self, rut):
        self.rut = rut

    def setPerfil(self, perfil):
        self.perfil = perfil

    # Getters (para obtener los datos después)
    def getRut(self):
        return self.rut

    def getPerfil(self):
        return self.perfil