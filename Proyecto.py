
# se encarga de representar la clase proyecto, con sus atributos y metodos correspondientes
class Proyecto:                                           #none, ya que el id se genera automaticamente en la base de datos al crear un nuevo proyecto
    def __init__(self, titulo, descripcion, fecha_inicio, id_proyecto = None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.id_proyecto = id_proyecto
#!getters y setters para cada atributo, para poder acceder a ellos desde otras clases y modificarlos si es necesario

    def getTitulo(self): return self.titulo
    def setTitulo(self, titulo):self.titulo = titulo

    def getDescripcion(self): return self.descripcion
    def setDescripcion(self, descripcion):self.descripcion = descripcion

    def getFechaInicio(self): return self.fecha_inicio
    def setFechaInicio(self, fecha_inicio): self.fecha_inicio = fecha_inicio

    def getIdProyecto(self): return self.id_proyecto
    def setIdProyecto(self, id_proyecto): self.id_proyecto = id_proyecto


