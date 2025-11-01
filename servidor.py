from mensaje import Mensaje
from usuario import Usuario

class ServidorCorreo(object):
    def __init__(self):
        self.usuarios_registrados = []
        self.usuario_actual = None

    def crear_usuario(self):
        # Crea un nuevo usuario y lo agrega a la lista de usuarios registrados
        nuevo_usuario = Usuario()
        self.usuarios_registrados.append(nuevo_usuario)
        print(f"Usuario {nuevo_usuario.get_nombre()} creado exitosamente")
        return nuevo_usuario

    def log_in(self):
        # Permite a un usuario iniciar sesión
        nombre = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")
        
        for usuario in self.usuarios_registrados:
            if usuario.get_nombre() == nombre and usuario.get_contraseña() == contraseña:
                self.usuario_actual = usuario
                print(f"Bienvenido {nombre}!")
                return usuario
        
        print("Nombre de usuario o contraseña incorrectos")
        return None

    def enviar_mensaje(self):
        # Permite al usuario actual enviar un mensaje
        if self.usuario_actual is None:
            print("Debe iniciar sesión primero")
            return
        
        mensaje = Mensaje()
        mensaje.set_remitente(self.usuario_actual)
        
        try:
            mensaje.set_destinatario(self)
            mensaje.set_asunto()
            mensaje.set_cuerpo()
            
            # Encuentra el usuario destinatario y agrega el mensaje a su carpeta sin leer
            destinatario = mensaje.get_destinatario()
            carpeta_sin_leer = destinatario.obtener_carpeta_sin_leer()
            if carpeta_sin_leer:
                carpeta_sin_leer.agregar_mensaje(mensaje)
                print("Mensaje enviado exitosamente")
            else:
                print("Error: No se pudo encontrar la carpeta de mensajes sin leer del destinatario")
                
        except ValueError as e:
            print(f"Error al enviar mensaje: {e}")

    def recibir_mensaje(self):
        # Simula la recepción de un mensaje
        if self.usuario_actual is None:
            print("Debe iniciar sesión primero")
            return
        
        if len(self.usuarios_registrados) < 2:
            print("Se necesitan al menos 2 usuarios para enviar mensajes")
            return
        
        # Enviar mensaje desde otro usuario al usuario actual
        remitente = None
        for usuario in self.usuarios_registrados:
            if usuario != self.usuario_actual:
                remitente = usuario
                break
        
        if remitente:
            mensaje = Mensaje()
            mensaje.set_remitente(remitente)
            mensaje.destinatario = self.usuario_actual  # Asignar directamente para testing
            mensaje.asunto = "Mensaje de prueba"
            mensaje.cuerpo = "Este es un mensaje de prueba automático"
            
            carpeta_sin_leer = self.usuario_actual.obtener_carpeta_sin_leer()
            if carpeta_sin_leer:
                carpeta_sin_leer.agregar_mensaje(mensaje)
                print(f"Mensaje de prueba recibido de {remitente.get_nombre()}")
            else:
                print("Error: No se pudo encontrar la carpeta de mensajes sin leer")
        else:
            print("No hay otros usuarios para enviar mensajes")

    def menu_principal(self):
        # Menú principal del sistema de correo
        while True:
            print("\n--- SISTEMA DE CORREO ---")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Enviar mensaje")
            print("4. Recibir mensaje (test)")
            print("5. Gestión de carpetas")
            print("6. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.log_in()
            elif opcion == "3":
                self.enviar_mensaje()
            elif opcion == "4":
                self.recibir_mensaje()
            elif opcion == "5":
                if self.usuario_actual:
                    self.menu_gestion_carpetas(self.usuario_actual)
                else:
                    print("Debe iniciar sesión primero")
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida")

    def menu_gestion_carpetas(self, usuario):
        # Menú principal para gestionar la estructura recursiva de carpetas
        while True:
            print("\n--- GESTIÓN DE CARPETAS RECURSIVAS ---")
            print("1. Mostrar estructura de carpetas")
            print("2. Crear subcarpeta")
            print("3. Buscar mensajes en todas las carpetas")
            print("4. Mover mensaje entre carpetas")
            print("5. Ver estadísticas de carpeta")
            print("6. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                # Mostrar toda la estructura de carpetas del usuario
                usuario.mostrar_estructura_carpetas()
            elif opcion == "2":
                # Crear una nueva subcarpeta dentro de una carpeta existente
                nombre_padre = input("Ingrese nombre de carpeta padre: ")
                nombre_nueva = input("Ingrese nombre de nueva subcarpeta: ")
                try:
                    nueva_carpeta = usuario.crear_subcarpeta(nombre_padre, nombre_nueva)
                    print(f"Subcarpeta '{nombre_nueva}' creada en '{nombre_padre}'")
                except ValueError as e:
                    print(f"Error: {e}")
            elif opcion == "3":
                # Búsqueda recursiva de mensajes en todas las carpetas
                self.buscar_mensajes_recursivo(usuario)
            elif opcion == "4":
                # Mover mensajes entre diferentes carpetas
                self.mover_mensaje_entre_carpetas(usuario)
            elif opcion == "5":
                # Ver estadísticas detalladas de una carpeta específica
                nombre_carpeta = input("Ingrese nombre de carpeta para estadísticas: ")
                carpeta = usuario.buscar_carpeta(nombre_carpeta)
                if carpeta:
                    carpeta.estadisticas()
                else:
                    print("Carpeta no encontrada")
            elif opcion == "6":
                # Vuelve al menú principal del servidor
                break
            else:
                print("Opción inválida")

    def buscar_mensajes_recursivo(self, usuario):
        # Interfaz para búsqueda recursiva de mensajes por asunto o remitente
        print("\n--- BÚSQUEDA RECURSIVA DE MENSAJES ---")
        print("1. Buscar por asunto")
        print("2. Buscar por remitente")
        
        opcion = input("Seleccione criterio de búsqueda: ")
        
        if opcion in ["1", "2"]:
            valor = input("Ingrese texto a buscar: ")
            criterio = "asunto" if opcion == "1" else "remitente"
            
            # Realiza una búsqueda recursiva en todas las carpetas
            resultados = usuario.buscar_mensajes_en_todas_carpetas(criterio, valor)
            
            if resultados:
                print(f"\nSe encontraron {len(resultados)} mensajes:")
                for mensaje, carpeta in resultados:
                    estado = "LEÍDO" if mensaje.leido else "NO LEÍDO"
                    print(f"- De: {mensaje.get_remitente()}, Asunto: {mensaje.get_asunto()}")
                    print(f"  Carpeta: {carpeta.get_ruta()}, Estado: {estado}")
            else:
                print("No se encontraron mensajes con ese criterio")
        else:
            print("Opción inválida")

    def mover_mensaje_entre_carpetas(self, usuario):
        # Interfaz para mover mensajes entre diferentes carpetas
        print("\n--- MOVER MENSAJE ENTRE CARPETAS ---")
        
        # Obtener carpeta principal donde están los mensajes
        carpeta_principal = usuario.obtener_carpeta_principal()
        if not carpeta_principal.mensajes:
            print("No hay mensajes para mover")
            return
            
        # Mostrar mensajes disponibles en carpeta principal
        print("Mensajes disponibles:")
        carpeta_principal.lista_mensajes()
        
        try:
            # Seleccionar mensaje a mover
            indice = int(input("Seleccione número de mensaje a mover: ")) - 1
            if 0 <= indice < len(carpeta_principal.mensajes):
                mensaje = carpeta_principal.mensajes[indice]
                
                # Mostrar estructura de carpetas destino disponibles
                print("Carpetas disponibles:")
                usuario.mostrar_estructura_carpetas()
                
                # Seleccionar carpeta destino
                carpeta_destino_nombre = input("Ingrese nombre de carpeta destino: ")
                carpeta_destino = usuario.buscar_carpeta(carpeta_destino_nombre)
                
                if carpeta_destino:
                    # Realizar el movimiento del mensaje
                    if usuario.mover_mensaje_entre_carpetas(mensaje, "Principal", carpeta_destino_nombre):
                        print("Mensaje movido exitosamente")
                    else:
                        print("Error al mover mensaje")
                else:
                    print("Carpeta destino no encontrada")
            else:
                print("Número de mensaje inválido")
        except ValueError:
            print("Debe ingresar un número válido")

    def menu_filtros_automaticos(self, usuario):
        # Menú para gestionar filtros automáticos
        while True:
            print("\n--- FILTROS AUTOMÁTICOS ---")
            print("1. Listar filtros")
            print("2. Agregar filtro")
            print("3. Eliminar filtro") 
            print("4. Activar/Desactivar filtro")
            print("5. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                usuario.listar_filtros()
            elif opcion == "2":
                self.agregar_nuevo_filtro(usuario)
            elif opcion == "3":
                nombre = input("Ingrese nombre del filtro a eliminar: ")
                usuario.eliminar_filtro_automatico(nombre)
            elif opcion == "4":
                self.gestionar_estado_filtro(usuario)
            elif opcion == "5":
                break
            else:
                print("Opción inválida")
    
    def agregar_nuevo_filtro(self, usuario):
        # Interfaz para agregar un nuevo filtro automático
        print("\n--- AGREGAR NUEVO FILTRO ---")
        nombre = input("Nombre del filtro: ")
        
        print("Criterios disponibles: asunto, remitente, prioridad, etiqueta")
        criterio = input("Criterio del filtro: ")
        
        valor = input("Valor a buscar: ")
        
        print("Carpetas disponibles:")
        usuario.mostrar_estructura_carpetas()
        carpeta_destino = input("Carpeta destino: ")
        
        usuario.agregar_filtro_automatico(nombre, criterio, valor, carpeta_destino)
    
    def gestionar_estado_filtro(self, usuario):
        # Interfaz para activar/desactivar filtros
        usuario.listar_filtros()
        nombre = input("Ingrese nombre del filtro: ")
        
        if nombre in usuario.filtros_automaticos:
            actual = usuario.filtros_automaticos[nombre]["activo"]
            if actual:
                usuario.desactivar_filtro(nombre)
            else:
                usuario.activar_filtro(nombre)
        else:
            print("Filtro no encontrado")
    
    def menu_cola_urgentes(self, usuario):
        # Menú para gestionar la cola de mensajes urgentes
        while True:
            print("\n--- COLA DE MENSAJES URGENTES ---")
            print(f" Mensajes urgentes en cola: {usuario.contar_urgentes()}")
            print("1. Mostrar cola de urgentes")
            print("2. Procesar siguiente urgente")
            print("3. Marcar mensaje como urgente")
            print("4. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                usuario.mostrar_cola_urgentes()
            elif opcion == "2":
                usuario.procesar_siguiente_urgente()
            elif opcion == "3":
                self.marcar_mensaje_urgente(usuario)
            elif opcion == "4":
                break
            else:
                print("Opción inválida")
    
    def marcar_mensaje_urgente(self, usuario):
        # Interfaz para marcar un mensaje como urgente
        carpeta_principal = usuario.obtener_carpeta_principal()
        if not carpeta_principal.mensajes:
            print("No hay mensajes disponibles")
            return
        
        print("Mensajes disponibles:")
        carpeta_principal.lista_mensajes()
        
        try:
            indice = int(input("Seleccione número de mensaje a marcar como urgente: ")) - 1
            if 0 <= indice < len(carpeta_principal.mensajes):
                mensaje = carpeta_principal.mensajes[indice]
                mensaje.marcar_urgente()
                usuario.agregar_a_cola_urgentes(mensaje)
                print("✓ Mensaje marcado como URGENTE y agregado a la cola")
            else:
                print("Número de mensaje inválido")
        except ValueError:
            print("Debe ingresar un número válido")
    
    def enviar_mensaje_con_filtros(self):
        # Versión mejorada de enviar_mensaje que aplica filtros automáticos
        if self.usuario_actual is None:
            print("Debe iniciar sesión primero")
            return
        
        mensaje = Mensaje()
        mensaje.set_remitente(self.usuario_actual)
        
        try:
            mensaje.set_destinatario(self)
            mensaje.set_asunto()
            mensaje.set_cuerpo()
            
            # Opción de prioridad
            print("Prioridades: normal, alta, urgente")
            prioridad = input("Prioridad del mensaje (default: normal): ") or "normal"
            mensaje.set_prioridad(prioridad)
            
            # Opción de etiquetas
            etiquetas = input("Etiquetas (separadas por coma): ")
            if etiquetas:
                for etiqueta in etiquetas.split(','):
                    mensaje.agregar_etiqueta(etiqueta.strip())
            
            destinatario = mensaje.get_destinatario()
            carpeta_sin_leer = destinatario.obtener_carpeta_sin_leer()
            
            if carpeta_sin_leer:
                # Agregar mensaje a carpeta sin leer
                carpeta_sin_leer.agregar_mensaje(mensaje)
                
                # Aplicar filtros automáticos
                filtros_aplicados = destinatario.aplicar_filtros_automaticos(mensaje)
                
                # Si es urgente, agregar a cola de urgentes
                if mensaje.es_mensaje_urgente():
                    destinatario.agregar_a_cola_urgentes(mensaje)
                    print(" Mensaje URGENTE enviado y agregado a cola de prioridades")
                else:
                    print("✓ Mensaje enviado exitosamente")
                    
                if filtros_aplicados:
                    print("✓ Filtros automáticos aplicados al mensaje")
                    
            else:
                print("Error: No se pudo encontrar la carpeta de mensajes sin leer del destinatario")
                
        except ValueError as e:
            print(f"Error al enviar mensaje: {e}")
    
    def menu_principal_mejorado(self):
        # Menú principal mejorado con nuevas funcionalidades
        while True:
            print("\n--- SISTEMA DE CORREO MEJORADO ---")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Enviar mensaje (con filtros)")
            print("4. Recibir mensaje (test)")
            print("5. Gestión de carpetas")
            print("6. Filtros automáticos")
            print("7. Cola de mensajes urgentes")
            print("8. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.log_in()
            elif opcion == "3":
                self.enviar_mensaje_con_filtros()  # Usa la versión con filtros
            elif opcion == "4":
                self.recibir_mensaje()
            elif opcion == "5":
                if self.usuario_actual:
                    self.menu_gestion_carpetas(self.usuario_actual)
                else:
                    print("Debe iniciar sesión primero")
            elif opcion == "6":
                if self.usuario_actual:
                    self.menu_filtros_automaticos(self.usuario_actual)
                else:
                    print("Debe iniciar sesión primero")
            elif opcion == "7":
                if self.usuario_actual:
                    self.menu_cola_urgentes(self.usuario_actual)
                else:
                    print("Debe iniciar sesión primero")
            elif opcion == "8":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida")

    # Usa el menú principal mejorado
    servidor.menu_principal_mejorado()
