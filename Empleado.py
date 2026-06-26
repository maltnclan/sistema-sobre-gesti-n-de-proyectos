from Persona import Persona

class Empleado(Persona):
    def __init__(self, rut, nombre, apellido, direccion, telefono, correo, fecha_inicio_contrato, salario, id_empleado = None):
        super().__init__(rut, nombre, apellido, direccion, telefono, correo)
        # super() llama al constructor de la clase Persona para que inicialice esos datos
        # y no tener que repetir el codigo de la clase Persona en la clase Empleado

        #atributos solo de la clase Empleado
        self.id_empleado = id_empleado
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario


        #getters y setters para los atributos de la clase Empleado

    def getIdEmpleado(self): return self.id_empleado
    def setIdEmpleado(self, id_empleado): self.id_empleado = id_empleado

    def getFechaInicioContrato(self): return self.fecha_inicio_contrato
    def setFechaInicioContrato(self, fecha_inicio_contrato): self.fecha_inicio_contrato = fecha_inicio_contrato

    def getSalario(self): return self.salario
    def setSalario(self, salario): self.salario = salario
        
      
