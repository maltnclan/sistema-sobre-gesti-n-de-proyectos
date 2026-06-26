import os
import getpass
from os import system
import pymysql
from Persona import Persona
from Empleado import Empleado
from Proyecto import Proyecto
from DAO import DAO
from datetime import datetime


class funciones:
    d = DAO()

    def __init__(self):
        pass




    '''=======================================================================================================================
    ========================     funciones menu   ========================================
    =========================================================================================================================='''
    def menu_inicial(self):
        while True:
            system("cls")
            print("\n ==== MENU PRINCIPAL ====")
            print("1. Iniciar Sesión\n2. Terminar Programa")
            op = input("seleccione opcion del menu: ")
            if op == "1":
                self.iniciar_sesion()
            elif op == "2":
                print("\n Programa finalizado... ")
                system("pause")
                os._exit(1)

    def iniciar_sesion(self):
        while True: # Este bucle hace que si se equivoca, vuelva a pedir los datos
            from os import system
            system("cls")
            print("\n ==== SISTEMA DE GESTIÓN - INICIO DE SESIÓN ====")
            
            rut = input("Ingrese rut de usuario: ")
            # getpass oculta la clave. Escribe con confianza aunque no veas nada y dale Enter.
            con = getpass.getpass("Ingrese contraseña: ") 
            
            # Llamamos al DAO
            usuario_logueado = self.d.login(rut, con)
            
            if usuario_logueado is not None:
                perfil = usuario_logueado.getPerfil()
                
                if perfil == 1:
                    print(f"\n¡Acceso concedido! Bienvenido Administrador (RUT: {usuario_logueado.getRut()})")
                    system("pause")
                    self.menuInicial() # Llama a tu menú principal
                    break # Rompe el ciclo del login porque ya entró
                    
                elif perfil == 2:
                    print(f"\n¡Acceso concedido! Bienvenido Comercial (RUT: {usuario_logueado.getRut()})")
                    system("pause")
                    self.menuAsignacion() # El comercial va directo a las asignaciones
                    break # Rompe el ciclo del login
            else:
                # Si llega aquí, es porque la clave o RUT fallaron. 
                # Mostrará este mensaje, hará una pausa, y por el 'while True' volverá arriba.
                print("\nError: RUT o contraseña incorrectos.")
                print("Por favor, intente nuevamente.")
                system("pause")
    '''=======================================================================================================================
    ========================     funciones menu   ========================================
    =========================================================================================================================='''

    def menuInicial(self):
        try:
            system("cls")
            print("\n ==== MENU PRINCIPAL ====")
            print("1. Gestion Empleado\n2. Gestion Proyecto\n3. Gestion Asignacion\n4. Terminar Programa")
            op= int(input("Seleccione opcion del menu: "))
            if op==1:
                self.menuEmpleado()
            elif op==2:
                self.menuProyecto()
            elif op==3:
                self.menuAsignacion()
            elif op==4:
                print("\n Programa finalizado... ")
                system("pause")
                os._exit(1)
            else:
                print("Opcion del menu inicial incorrecta")
                system("pause")
                self.menuInicial()
        except ValueError:
            print("La opcion del menu inicial debe ser numerica")
            system("pause")
            self.menuInicial()
  
    def menuEmpleado(self):
        try:
            system("cls")
            print("\n ==== MENU EMPLEADO ====")
            print("1. Crear Empleado\n2. Listar Empleados\n3. buscar Empleado por RUT\n4. Modificar Empleado\n5. eliminar Empleado\n6. Regresar a menú anterior")
            op= int(input("Seleccione opcion del menu: "))
            if op==1:
                self.registrarEmpleado()
            elif op==2:
                self.listarEmpleados()
            elif op==3:
                self.buscarEmpleado_por_rut()
            elif op==4:
                self.modificarEmpleado()
            elif op==5:
                self.eliminarEmpleado()
            elif op==6:
                self.menuInicial()
            else:
                print("Opcion del menu incorrecta")
            system("pause")
            self.menuEmpleado()
        except Exception as e:
            print(f"Error: {e}")
        system("pause")
        self.menuEmpleado()

    def buscarEmpleado_por_rut(self):
        try:
            system("cls")
            print("\n ==== BUSCAR EMPLEADO ====")
            rut = input("Ingrese el RUT del empleado a buscar: ")
            empleado = self.d.buscarEmpleado_por_rut(rut)
            
            if empleado:
                print("\nDatos del Empleado:")
                print(f"ID: {empleado[0]} | RUT: {empleado[1]}")
                print(f"Nombre: {empleado[2]} {empleado[3]}")
                print(f"Dirección: {empleado[4]}")
                print(f"Teléfono: {empleado[5]}")
                print(f"Correo: {empleado[6]}")
                print(f"Inicio Contrato: {empleado[7]}")
                print(f"Salario: ${empleado[8]}")
            else:
                print(f"No se encontró ningún empleado con el RUT: {rut}")
        except Exception as e:
            print(f"Error al buscar empleado: {e}")
            
    def modificarEmpleado(self):
        try:
            system("cls")
            print("\n ==== MODIFICAR EMPLEADO ====")
            rut = input("Ingrese el RUT del empleado a modificar: ")
            
            empleado_actual = self.d.buscarEmpleado_por_rut(rut)
            
            if empleado_actual:
                print(f"\nEmpleado encontrado: {empleado_actual[2]} {empleado_actual[3]}")
                print("Deje el campo en blanco si no desea modificarlo.\n")
                
# --- Magia de Python con 'or' ---
                nom = input(f"Nuevo Nombre ({empleado_actual[2]}): ") or empleado_actual[2]
                ape = input(f"Nuevo Apellido ({empleado_actual[3]}): ") or empleado_actual[3]
                tel = input(f"Nuevo Teléfono ({empleado_actual[5]}): ") or empleado_actual[5]
                corr = input(f"Nuevo Correo ({empleado_actual[6]}): ") or empleado_actual[6]
                direc = input(f"Nueva Dirección ({empleado_actual[4]}): ") or empleado_actual[4]
                
                # El salario necesita su validación especial isdigit()
                sal_input = input(f"Nuevo Salario ({empleado_actual[8]}): ")
                sal = int(sal_input) if sal_input.isdigit() else empleado_actual[8]
                
                
                exito = self.d.actualizar_empleado(rut, nom, ape, tel, direc, corr, sal)
                
                if exito:
                    print("Empleado actualizado correctamente.")
                else:
                    print("Error al actualizar el empleado en la base de datos.")
            else:
                print("El empleado no existe.")
        except Exception:
            print(f"Error al modificar empleado")

    def eliminarEmpleado(self):
        try:
            system("cls")
            print("\n ==== ELIMINAR EMPLEADO ====")
            rut = input("Ingrese el RUT del empleado a eliminar: ")
            empleado = self.d.buscarEmpleado_por_rut(rut)
            
            # Cláusula de guarda: si no hay empleado, avisamos y salimos del método
            if not empleado:
                print("El empleado no existe en los registros.")
                return 
            
            print(f"\nSe eliminará a: {empleado[2]} {empleado[3]} (RUT: {empleado[1]})")
            
            # Pedimos confirmación y evaluamos en la misma línea
            if input("¿Está seguro de eliminarlo? (s/n): ").strip().lower() == 's':
                # Evaluamos el éxito de la eliminación directamente en el if
                if self.d.eliminar_empleado(rut):
                    print("Empleado eliminado con éxito.")
                else:
                    print("No se pudo eliminar al empleado. Verifique que no tenga registros asociados activos.")
            else:
                print("Operación cancelada.")
                
        except Exception:
            print("Ocurrió un problema inesperado al intentar eliminar el registro. Intente nuevamente.")

    def registrarEmpleado(self):
        try:
            system("cls")
            print("\n ==== REGISTRO DE NUEVO EMPLEADO ====")

            # --- Validación de RUT (Obligatorio y con límite) ---
            while True:
                rut = input("Ingrese RUT (Max 12): ")
                if not rut:
                    print("Error: El RUT es un campo obligatorio.")
                elif len(rut) > 12:
                    print(f"Error: El RUT no puede superar los 12 caracteres (ingresaste {len(rut)}).")
                else:
                    break # Si todo está bien, salimos del bucle

            # --- Validación de Nombre (Obligatorio y con límite) ---
            while True:
                nombre = input("Ingrese Nombre (Max 50): ")
                if not nombre: print("Error: El Nombre es un campo obligatorio."); continue
                if len(nombre) > 50: print(f"Error: El Nombre no puede superar los 50 caracteres (ingresaste {len(nombre)})."); continue
                if not nombre.replace(" ", "").isalpha(): print("Error: El Nombre solo puede contener letras."); continue
                break

            




            # --- Validación de Apellido (Obligatorio y con límite) ---
            while True:
                apellido = input("Ingrese Apellido (Max 50): ")
                if not apellido: print("Error: El Apellido es un campo obligatorio."); continue
                if len(apellido) > 50: print(f"Error: El Apellido no puede superar los 50 caracteres (ingresaste {len(apellido)})."); continue
                if not apellido.replace(" ", "").isalpha(): print("Error: El Apellido solo puede contener letras."); continue
                break

            direccion = input("Ingrese Dirección [Opcional]: ")[:150] # Cortar es aceptable para campos opcionales
            telefono = input("Ingrese Teléfono [Opcional]: ")[:12]   # y que no son tan críticos.

            while True:
                correo = input("Ingrese Correo (Max 100): ")
                if len(correo) > 100: print(f"Error: El correo no puede superar los 100 caracteres (ingresaste {len(correo)})."); continue
                break

            while True:
                try:
                    fecha_inicio = datetime.strptime(input("Ingrese Fecha Inicio Contrato (YYYY-MM-DD): "), "%Y-%m-%d")
                    break
                except ValueError:













                    print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

            # Validación simple: isdigit() comprueba que el texto solo contenga números
            salario_str = ""
            while not salario_str.isdigit(): 
                salario_str = input("Ingrese Salario (solo números): ")
            salario = int(salario_str)

            nuevo_emp = Empleado(rut, nombre, apellido, direccion, telefono, correo, fecha_inicio, salario)
            exito = self.d.crear_empleado(nuevo_emp)
            
            if exito:
                print("Empleado registrado con éxito.")
            else:
                print("Error: No se pudo guardar el empleado (revise los datos).")
            system("pause")
            self.menuEmpleado()
        except Exception as e:
            print(f"Error al registrar empleado: {e}")
            system("pause")
            self.menuEmpleado()

    def listarEmpleados(self):
        try:
            system("cls")
            print("\n ==== LISTADO DE EMPLEADOS ====")
            empleados = self.d.listar_empleados()
            if empleados:
                for e in empleados:
                    print(f"ID: {e[0]} | RUT: {e[1]} | Nombre: {e[2]} {e[3]} | Salario: ${e[8]}")
                    print(f"    Dir: {e[4]} | Tel: {e[5]} | Correo: {e[6]} | Inicio: {e[7]}")
                    print("-" * 60)
            else:
                print("No hay empleados registrados.")
            system("pause")
            self.menuEmpleado()
        except Exception as e:
            print(f"Error al listar empleados: {e}")
            system("pause")
            self.menuEmpleado()

    # =========================================================================
    # ======================== MENÚ DE PROYECTOS ==============================
    # =========================================================================

    def menuProyecto(self):
        try:
            system("cls")
            print("\n ==== MENU PROYECTO ====")
            print("1. Crear Proyecto\n2. Listar Proyecto\n3. Buscar Proyecto por ID\n4. modificar Proyecto\n5. Regresar a menú anterior")
            op = int(input("Seleccione opcion del menu: "))
            
            if op == 1:
                self.registrarProyecto()
            elif op == 2:
                self.listarProyectos()
            elif op ==3:
                self.buscarProyecto_por_id()
            elif op == 4:
                self.modificarProyecto()
            elif op == 5:
                self.menuInicial()
            else:
                print("Opcion del menu incorrecta")
                system("pause")
                self.menuProyecto()
        except Exception as e:
            print(f"Error en menú de proyectos: {e}")
            system("pause")
            self.menuProyecto()

    def registrarProyecto(self):
        try:
            system("cls")
            print("\n ==== REGISTRO DE NUEVO PROYECTO ====")
            
            # --- Validación de Título (Obligatorio y con límite) ---
            while True:
                titulo = input("Ingrese Título del Proyecto (Max 100): ")
                if not titulo: print("Error: El Título es un campo obligatorio."); continue
                if len(titulo) > 100: print(f"Error: El Título no puede superar los 100 caracteres (ingresaste {len(titulo)})."); continue
                break
            
            descripcion = input("Ingrese Descripción [Opcional]: ")[:150] 

            while True:
                 fecha_inicio = input("Ingrese Fecha Inicio (YYYY-MM-DD): ")
                 try:
                    datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    break
                 except ValueError:
                     print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

            nuevo_proy = Proyecto(titulo, descripcion, fecha_inicio)
            self.d.crear_proyecto(nuevo_proy)
            system("pause")
            self.menuProyecto()
        except Exception as e:
            print(f"Error al registrar proyecto: {e}")
            system("pause")
            self.menuProyecto()

    def listarProyectos(self):
        try:
            system("cls")
            print("\n ==== LISTADO DE PROYECTOS ====")
            proyectos = self.d.listar_proyectos()
            if proyectos:
                for p in proyectos:
                    print(f"ID: {p[0]} | Título: {p[1]} | Fecha Inicio: {p[3]}")
            else:
                print("No hay proyectos registrados.")
            system("pause")
            self.menuProyecto()
        except Exception as e:
            print(f"Error al listar proyectos: {e}")
            system("pause")
            self.menuProyecto()

    def buscarProyecto_por_id(self):
        try:
            system("cls")
            print("\n ==== BUSCAR PROYECTO ====")
            id_proy_str = ""
            while not id_proy_str.isdigit():
                id_proy_str = input("Ingrese el ID del proyecto (solo números): ")


            if id_proy_str.isdigit():
                id_proy = int(id_proy_str)
                proyecto = self.d.buscarProyecto_por_id(id_proy)


                if proyecto:
                    print(f"\nDatos del Proyecto:")
                    print(f"ID: {proyecto[0]} | Título: {proyecto[1]}")
                    print(f"Descripción: {proyecto[2]}")
                    print(f"Fecha Inicio: {proyecto[3]}")
                else:
                    print(f"No se encontró ningún proyecto con el ID: {id_proy}")

                print("\n")
                system("pause")
                self.menuProyecto()
                
        except Exception as e:
            print(f"Error al buscar proyecto: {e}")
            system("pause")
            self.menuProyecto()     

    def modificarProyecto(self):
        try:
            from os import system 
            system("cls")
            print("\n ==== MODIFICAR PROYECTO ====")
            id_proy_str = input("Ingrese el ID del proyecto a modificar: ")
            
            if id_proy_str.isdigit():
                id_proy = int(id_proy_str)
                
                # 1. Buscamos si el proyecto realmente existe usando el método que ya tienes
                proyecto_actual = self.d.buscarProyecto_por_id(id_proy)
                
                if proyecto_actual:
                    print(f"\nModificando el proyecto: {proyecto_actual[1]}") 
                    print("------------------------------------------------")
                    
                    # 2. Pedimos los nuevos datos por teclado
                    nuevo_titulo = input("Ingrese el nuevo título: ")
                    nueva_desc = input("Ingrese la nueva descripción: ")
                    nueva_fecha = input("Ingrese la nueva fecha (formato YYYY-MM-DD): ")
                    
                    # 3. Enviamos los datos al DAO para que haga el UPDATE
                    exito = self.d.modificar_proyecto(id_proy, nuevo_titulo, nueva_desc, nueva_fecha)
                    
                    if exito:
                        print("\n¡Proyecto actualizado correctamente en la base de datos!")
                    else:
                        print("\nHubo un problema al intentar actualizar el proyecto.")
                else:
                    print(f"\nError: No se encontró ningún proyecto con el ID {id_proy}.")
            else:
                print("\nPor favor, ingrese un ID válido (solo números).")
                
            print("\n")
            system("pause")
            self.menuProyecto() # Cambia esto por el nombre de tu menú de proyectos
            
        except Exception as e:
            print(f"Error en el menú de modificación: {e}")
            system("pause")
            self.menuProyecto()


    # =========================================================================
    # ======================== MENÚ DE PROYECTO - EMPLEADO ====================
    # =========================================================================

    def menuAsignacion(self):
        try:
            system("cls")
            print("\n ==== MENU ASIGNACION ====")
            print("1. Asignar Empleado-Proyecto")
            print("2. Reasignar Empleado-Proyecto")
            print("3. Regresar a menú anterior")
            op = int(input("Seleccione opcion del menu: "))
            
            if op == 1:
                self.asignarEmpleadoAProyecto()
            elif op == 2:
                self.reasignarEmpleadoAProyecto()
            elif op == 3:
                self.menuInicial()
            else:
                print("Opcion incorrecta")
                system("pause")
                self.menuAsignacion()
        except Exception as e:
            print(f"Error: {e}")
            system("pause")
            self.menuAsignacion()
            
    def asignarEmpleadoAProyecto(self):
        try:
            system("cls")
            print("\n ==== ASIGNAR EMPLEADO A PROYECTO ====")
            rut = input("Ingrese el RUT del empleado: ")
            
            # Validación simple para que el ID sea solo numérico
            id_proy_str = ""
            while not id_proy_str.isdigit():
                id_proy_str = input("Ingrese el ID del proyecto (solo números): ")
            id_proy = int(id_proy_str)

            exito = self.d.asignar_empleado_proyecto(rut, id_proy)
            if exito:
                print("¡Empleado asignado al proyecto con éxito!")
            else:
                print("No se pudo asignar. Verifique que el RUT y el ID del proyecto existan.")
            system("pause")
            self.menuAsignacion()
        except Exception as e:
            print(f"Error: {e}")
            system("pause")
            self.menuAsignacion()

    def reasignarEmpleadoAProyecto(self):
        try:
            from os import system
            system("cls")
            print("\n ==== REASIGNAR EMPLEADO A PROYECTO ====")
            
            # Pedimos los 3 datos clave
            rut_emp = input("Ingrese el RUT del empleado: ")
            id_actual_str = input("Ingrese el ID del proyecto ACTUAL (del que saldrá): ")
            id_nuevo_str = input("Ingrese el ID del proyecto NUEVO (al que entrará): ")
            
            # Verificamos que los ID sean números
            if id_actual_str.isdigit() and id_nuevo_str.isdigit():
                id_actual = int(id_actual_str)
                id_nuevo = int(id_nuevo_str)
                
                # Llamamos a nuestro nuevo método del DAO
                exito = self.d.reasignar_empleado_proyecto(rut_emp, id_actual, id_nuevo)
                
                if exito:
                    print(f"\n¡Éxito! El empleado con RUT '{rut_emp}' fue movido al proyecto {id_nuevo}.")
                else:
                    print(f"\nError: No se encontró al empleado '{rut_emp}' asignado al proyecto {id_actual}.")
                    print("Revise los datos e intente nuevamente.")
            else:
                print("\nError: Los ID de los proyectos deben ser números enteros.")
                
            print("\n")
            system("pause")
            self.menuAsignacion() # Regresa a tu menú de opciones
            
        except Exception as e:
            print(f"Error en el menú de reasignación: {e}")
            system("pause")
            self.menuAsignacion()

   