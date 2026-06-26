import pymysql
from cryptography.fernet import Fernet
from Empleado import Empleado
from Proyecto import Proyecto
from Persona import Persona
from Usuario import Usuario
# es la clase encargada de hablar con la base de datos, es decir, conectar, desconectar y ejecutar las consultas necesarias para el proyecto
class DAO:
    def __init__ (self):
        pass #no se necesita nada en el constructor,
             #ya que la conexion se hace en la funcion conectar y se cierra en la funcion desconectar
    
    # funcion para conectar de manera local a la base de datos de mysql
    def conectar(self): 
        self.con = pymysql.connect(
            host = "localhost", # localhost, ya que es una base de datos local
            user = "root", # usuario por defecto de mysql, ya que es una base de datos local
            password = "", #sin contraseña, ya que es una base de datos local
            db = "base_proyecto_1" #nombre de la bd
        )
        self.cursor = self.con.cursor()
#!cursor para ejecutar las consultas, se guarda como atributo de la clase para poder usarlo en otras funciones

    #funcion para desconectar de la base de datos
    def desconectar(self):
        self.con.close()


##==========================================================================================
##==========================FUNCIONES LOGIN================================================================
##==========================================================================================

    def login(self, rut_ingresado, con_ingresada):
        try:
            self.conectar()
            # Traemos el rut, la clave y el perfil desde la base de datos
            sql = "SELECT rut, password, perfil FROM usuarios WHERE rut = %s"
            self.cursor.execute(sql, (rut_ingresado,))
            rs = self.cursor.fetchone() 
            
            if rs is None:
                return None 
                
            rut_bd = rs[0]
            encriptada = rs[1] 
            perfil_bd = rs[2]     
            
            # Tu llave maestra
            clave_fernet = b"P55qXsnh2LZ8kmRrt5h4Z0xSsF6oURZQe8aCGIhZfZE="     
            f = Fernet(clave_fernet)
            
            # Desencriptamos la clave
            desencriptada = f.decrypt(encriptada.encode()).decode()
            
            if con_ingresada == desencriptada:    
                # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
                # En lugar de "return perfil_bd", creamos el objeto Usuario
                usu = Usuario()          
                usu.setRut(rut_bd)
                usu.setPerfil(perfil_bd)
                
                return usu # Ahora sí devolvemos el objeto completo
                # ---------------------------------
            else:
                return None 
                
        except Exception as e:
            print(f"\n Error en BD al iniciar sesión: {e}")
            return None
        finally:
            self.desconectar()

##==========================================================================================
##==========================FUNCIONES proyecto================================================================
##==========================================================================================

#metodo: crear_proyecto(datos)
#! necesita un sql (insert into proyecto...) para guardar el proyecto
    def crear_proyecto(self, proyecto): # recibe "proyecto" como objeto 
        try:  
            self.conectar() #conecta a la base de datos
            # queda la peticion en "sql" para luego ejecutarla con el cursor
            sql = "INSERT INTO proyecto (titulo, descripcion, fechaInicio) VALUES (%s,%s,%s)"


            # saca los datos del objeto proyecto usando los getters y los guarda en una tupla "valores"
            #  para luego pasarlos a la consulta sql
            valores = (
                proyecto.getTitulo(),
                proyecto.getDescripcion(),
                proyecto.getFechaInicio()
            )
            
            self.cursor.execute(sql, valores) # ejecuta la consulta sql con los valores del proyecto
            self.con.commit() # guarda los cambios en la base de datos

            print("proyecto registrado exitosamente") # mensaje de confirmacion
        except Exception as e:
            print("Error al registrar el proyecto: ", e) # mensaje de error en caso de que algo salga mal
        finally:
            self.desconectar() #siempre se debe desconectar la bd, ya sea que la consulta haya sido exitosa o no
                                # y inyecciones de sql, ya que se usan consultas preparadas con %s y se pasan los valores como tupla, lo que evita que se puedan inyectar consultas maliciosas a la base de datos



#metodo: listar_proyectos
#! necesita un sql (select * from proyecto) para listar los proyectos
    def listar_proyectos(self):
        try:
            self.conectar()#conectamos a la base
            sql = "SELECT * FROM proyecto" #la consulta selecciona todo de la tabla proyecto y lo guarda en la variable "sql"

            self.cursor.execute(sql) #ejecuta la consulta sql

            proyectos = self.cursor.fetchall() #fetchall() devuelve una lista de tuplas con los resultados de la consulta, cada tupla representa un proyecto con sus atributos (id_proyecto, titulo, descripcion, fecha_inicio)

            return proyectos
        
        except Exception as e:# maneja cualquier error que pueda ocurrir durante la consulta, como problemas de conexion, errores en la consulta sql, etc.

            print("Error al listar los proyectos: ", e) # mensaje de error en caso de que algo salga mal

        finally: #finally se ejecuta siempre, ya sea que la consulta haya sido exitosa o no, y se encarga de cerrar la conexion a la base de datos para evitar problemas de conexion y liberar recursos 

            self.desconectar() #siempre se debe desconectar la bd, ya sea que la consulta haya sido exitosa o no



#metodo: buscarProyecto_por_id
#! busca un proyecto especifico por su id usando la instruccion SELECT con WHERE
    def buscarProyecto_por_id(self, id_proyecto):
        try:
            self.conectar()
            sql = "SELECT * FROM proyecto WHERE idProyecto = %s"
            self.cursor.execute(sql, (id_proyecto,)) # ejecuta la consulta sql con el id del proyecto como parametro
            proyecto = self.cursor.fetchone() #fetchone() devuelve una tupla con el resultado de la consulta, que representa el proyecto con sus atributos (id_proyecto, titulo, descripcion, fecha_inicio)
            return proyecto
        except Exception as e:
            print("Error al buscar el proyecto: ", e)
            return None
        finally:
            self.desconectar()




#metodo: modificar_proyecto
# ! modifica los datos de un proyecto existente usando UPDATE    
    def modificar_proyecto(self, id_proyecto, titulo, descripcion, fecha_inicio):
        try:
            self.conectar()
            # Usamos los nombres exactos de tus columnas según la foto: idProyecto, titulo, descripcion, fechaInicio
            sql = "UPDATE proyecto SET titulo = %s, descripcion = %s, fechaInicio = %s WHERE idProyecto = %s"
            valores = (titulo, descripcion, fecha_inicio, id_proyecto)
            
            self.cursor.execute(sql, valores)
            self.con.commit() # ¡Súper importante para guardar los cambios!
            
            return True # Retornamos True para avisar que todo salió bien
            
        except Exception as e:
            print("Error al modificar el proyecto en BD: ", e)
            return False # Retornamos False si algo falló
            
        finally:
            self.desconectar()



#metodo reasignar_empleado_proyecto
# ! cambia el proyecto de un empleado existente usando UPDATE en la tabla intermedia proyecto_empleado
    def reasignar_empleado_proyecto(self, rut_empleado, id_proyecto_actual, id_proyecto_nuevo):
        try:
            self.conectar()
            
            # Actualizamos el proyecto nuevo, buscando por el RUT y el proyecto viejo
            sql = "UPDATE proyecto_empleado SET id_proyecto = %s WHERE rut_empleado = %s AND id_proyecto = %s"
            valores = (id_proyecto_nuevo, rut_empleado, id_proyecto_actual)
            
            self.cursor.execute(sql, valores)
            
            # rowcount nos dice cuántas filas fueron afectadas por el UPDATE
            if self.cursor.rowcount > 0:
                self.con.commit() # Guardamos los cambios
                return True
            else:
                return False # Falso si no encontró esa combinación de RUT y Proyecto
                
        except Exception as e:
            print("Error al reasignar en BD: ", e)
            return False
        finally:
            self.desconectar()



##==========================================================================================
##==========================FUNCIONES EMPLEADO================================================================
##==========================================================================================
#metodo: crear_empleado(datos)
#! necesita un sql (insert into empleado...) para guardar el empleado
    def crear_empleado(self, empleado): # recibe "empleado" como objeto
        try:
            self.conectar()

            sql = "insert into empleado (rut, nombre, apellido, direccion, telefono, correo, fechaInicioContrato, salario) values (%s,%s,%s,%s,%s,%s,%s,%s)"

            valores = (
                empleado.getRut(),
                empleado.getNombre(),
                empleado.getApellido(),
                empleado.getDireccion(),
                empleado.getTelefono(),
                empleado.getCorreo(),
                empleado.getFechaInicioContrato(),
                empleado.getSalario()
            )

            self.cursor.execute(sql, valores)
            self.con.commit()
            return True

        except Exception as e:
            print("Error al registrar el empleado: ", e)
            return False
        finally:
            self.desconectar()



#metodo: listar_empleados
#! necesita un sql (select * from empleado) para listar los empleados
    def listar_empleados(self):
        try:
            self.conectar()
            sql = "SELECT * FROM empleado"
            self.cursor.execute(sql)
            empleados = self.cursor.fetchall()
            return empleados
        except Exception as e:
            print("Error al listar los empleados: ", e)
            return None
        finally:
            self.desconectar()



#metodo: buscar_empleado_por_rut
#! busca un empleado especifico por su rut usando la instruccion SELECT con WHERE
    def buscarEmpleado_por_rut(self, rut):
        try:
            self.conectar()
            sql = "SELECT * FROM empleado WHERE rut = %s"
            self.cursor.execute(sql, (rut,))
            empleado = self.cursor.fetchone()
            return empleado
        except Exception as e:
            print("Error al buscar el empleado: ", e)
            return None
        finally:
            self.desconectar()


#metodo: modificar_empleado
#! modifica los datos de un empleado existente usando UPDATE
    def actualizar_empleado(self, rut, nombre, apellido, telefono, direccion, correo, salario):
        try:
            self.conectar()
            sql = "UPDATE empleado SET nombre=%s, apellido=%s, telefono=%s, direccion=%s, correo=%s, salario=%s WHERE rut=%s"
            valores = (nombre, apellido, telefono, direccion, correo, salario, rut)
            self.cursor.execute(sql, valores)
            self.con.commit()
            return True
        except Exception as e:
            print("Error al actualizar el empleado: ", e)
            return False
        finally:
            self.desconectar()




#metodo: eliminar_empleado
#! borra un empleado de la base de datos usando DELETE
    def eliminar_empleado(self, rut):
        try:
            self.conectar()
            sql = "DELETE FROM empleado WHERE rut = %s"
            self.cursor.execute(sql, (rut,))
            self.con.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("Error al eliminar el empleado: ", e)
            return False
        finally:
            self.desconectar()



#metodo: asignar_empleado_proyecto
#! vincula un empleado a un proyecto guardando sus IDs en la tabla intermedia
    def asignar_empleado_proyecto(self, rut, id_proyecto):
        try:
            self.conectar()
            sql = "INSERT INTO proyecto_empleado (rut_empleado, id_proyecto) VALUES (%s, %s)"
            self.cursor.execute(sql, (rut, id_proyecto))
            self.con.commit()
            return True
        except Exception as e:
            print("Error al asignar el empleado al proyecto: ", e)
            return False
        finally:
            self.desconectar()
            
