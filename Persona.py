class Persona:
    def __init__(self, rut, nombre, apellido, direccion, telefono, correo):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

        #!getters y setters para la clase Persona,
        #para poder acceder a los atributos desde otras clases y modificarlos si es necesario

    def getRut(self): return self.rut
    def setRut(self, rut): self.rut = rut

    def getNombre(self): return self.nombre
    def setNombre(self, nombre): self.nombre = nombre

    def getApellido(self): return self.apellido
    def setApellido(self, apellido): self.apellido = apellido

    def getDireccion(self): return self.direccion
    def setDireccion(self, direccion): self.direccion = direccion    

    def getTelefono(self): return self.telefono
    def setTelefono(self, telefono): self.telefono = telefono

    def getCorreo(self): return self.correo
    def setCorreo(self, correo): self.correo = correo
