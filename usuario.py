from carpetas import Carpeta

class Usuario(object):
    def __init__(self):
        self.set_nombre()
        self.set_contraseña()
        self.carpetas = []
        self.filtros_automaticos = {}  # Diccionario de filtros automáticos
        self.cola_urgentes = []  # Cola de mensajes urgentes
        self._inicializar_carpetas_base()
        self._inicializar_filtros_predeterminados()  # Filtros por defecto
    
    def __str__(self):
        return "Usuario:" + self.get_nombre()
    
    def set_nombre(self):
        # Permite settear el nombre con una verificacion de que sea un STR
        nuevo_nombre = input("Ingrese su nuevo nombre de usuario: ")
        
        if isinstance(nuevo_nombre,str):
            self._nombre = nuevo_nombre
        else:
            raise TypeError ("El nombre debe ser una cadena de caracteres")
    
    def get_nombre(self):
        # Permite el acceso al nombre de usuario
        return self._nombre
    
    def set_contraseña(self):
        # Permite settear la contraseña con una verificacion de que sea un STR
        nueva_contraseña = input("Ingrese su nueva contraseña: ")
        
        if isinstance(nueva_contraseña,str):
            self._contraseña = nueva_contraseña
        else:
            raise TypeError ("La contraseña debe ser una cadena de caracteres")
    
    def get_contraseña(self):
        # Permite el acceso a la contraseña del usuario
        return self._contraseña
    
    def _inicializar_carpetas_base(self):
        # Inicializa las carpetas base del usuario con estructura recursiva
        carpeta_principal = Carpeta("Principal")
        self.carpetas.append(carpeta_principal)

        # Crea algunas subcarpetas por defecto para organizar mensajes
        carpeta_principal.agregar_subcarpeta("Trabajo")
        carpeta_principal.agregar_subcarpeta("Personal")
        carpeta_principal.agregar_subcarpeta("Importante")

        # Carpeta de mensajes sin leer
        carpeta_sin_leer = Carpeta("Mensajes sin leer")
        self.carpetas.append(carpeta_sin_leer)
    
    def _inicializar_filtros_predeterminados(self):
        # Inicializa filtros automáticos predeterminados
        self.filtros_automaticos = {
            "trabajo": {
                "criterio": "asunto",
                "valor": "reunión",
                "carpeta_destino": "Trabajo",
                "activo": True
            },
            "personal": {
                "criterio": "remitente",
                "valor": "familia",
                "carpeta_destino": "Personal", 
                "activo": True
            },
            "importante": {
                "criterio": "prioridad",
                "valor": "alta",
                "carpeta_destino": "Importante",
                "activo": True
            }
        }
    
    def buscar_carpeta(self, nombre):
        # Busca una carpeta por nombre en todas las carpetas del usuario (búsqueda recursiva)
        for carpeta in self.carpetas:
            if carpeta.get_nombre() == nombre:
                return carpeta
            # Buscar recursivamente en subcarpetas
            resultado = carpeta.buscar_subcarpeta_recursivo(nombre)
            if resultado:
                return resultado
        return None
    
    def crear_subcarpeta(self, nombre_carpeta_padre, nombre_nueva_carpeta):
        # Crea una subcarpeta dentro de una carpeta existente
        carpeta_padre = self.buscar_carpeta(nombre_carpeta_padre)
        if carpeta_padre:
            return carpeta_padre.agregar_subcarpeta(nombre_nueva_carpeta)
        raise ValueError(f"No se encontró la carpeta padre '{nombre_carpeta_padre}'")
    
    def buscar_mensajes_en_todas_carpetas(self, criterio, valor):
        # Busca mensajes en todas las carpetas del usuario
        resultados = []
        for carpeta in self.carpetas:
            resultados.extend(carpeta.buscar_mensajes_recursivo(criterio, valor))
        return resultados
    
    def mover_mensaje_entre_carpetas(self, mensaje, nombre_carpeta_origen, nombre_carpeta_destino):
        # Mueve un mensaje entre dos carpetas especificadas por nombre
        carpeta_origen = self.buscar_carpeta(nombre_carpeta_origen)
        carpeta_destino = self.buscar_carpeta(nombre_carpeta_destino)
        
        if carpeta_origen and carpeta_destino:
            return carpeta_origen.mover_mensaje(mensaje, carpeta_destino)
        return False
    
    def mover_mensaje_por_ruta(self, mensaje, ruta_destino):
        # Mueve un mensaje usando ruta completa de carpeta destino
        # Primero busca en qué carpeta está actualmente el mensaje
        carpeta_actual = None
        for carpeta in self.carpetas:
            if mensaje in carpeta.mensajes:
                carpeta_actual = carpeta
                break
            # Buscar recursivamente en subcarpetas
            for subcarpeta in carpeta.obtener_todas_subcarpetas():
                if mensaje in subcarpeta.mensajes:
                    carpeta_actual = subcarpeta
                    break
        
        if carpeta_actual:
            return carpeta_actual.mover_mensaje_por_ruta(mensaje, ruta_destino)
        return False
    
    def mostrar_estructura_carpetas(self):
        # Muestra toda la estructura de carpetas del usuario de forma jerárquica
        print("\n--- Estructura de Carpetas ---")
        for carpeta in self.carpetas:
            print(f"\n{carpeta.get_ruta()}:")
            carpeta.lista_subcarpetas(recursivo=True)
    
    def obtener_carpeta_principal(self):
        # Obtiene la carpeta principal del usuario
        for carpeta in self.carpetas:
            if carpeta.get_nombre() == "Principal":
                return carpeta
        return None
    
    def obtener_carpeta_sin_leer(self):
        # Obtiene la carpeta de mensajes sin leer
        for carpeta in self.carpetas:
            if carpeta.get_nombre() == "Mensajes sin leer":
                return carpeta
        return None

    def agregar_filtro_automatico(self, nombre, criterio, valor, carpeta_destino):
        # Agrega un nuevo filtro automático
        self.filtros_automaticos[nombre] = {
            "criterio": criterio,
            "valor": valor.lower(),
            "carpeta_destino": carpeta_destino,
            "activo": True
        }
        print(f"Filtro '{nombre}' agregado exitosamente")
    
    def eliminar_filtro_automatico(self, nombre):
        # Elimina un filtro automático
        if nombre in self.filtros_automaticos:
            del self.filtros_automaticos[nombre]
            print(f"Filtro '{nombre}' eliminado")
        else:
            print(f"Filtro '{nombre}' no encontrado")
    
    def activar_filtro(self, nombre):
        # Activa un filtro automático
        if nombre in self.filtros_automaticos:
            self.filtros_automaticos[nombre]["activo"] = True
            print(f"Filtro '{nombre}' activado")
        else:
            print(f"Filtro '{nombre}' no encontrado")
    
    def desactivar_filtro(self, nombre):
        # Desactiva un filtro automático
        if nombre in self.filtros_automaticos:
            self.filtros_automaticos[nombre]["activo"] = False
            print(f"Filtro '{nombre}' desactivado")
        else:
            print(f"Filtro '{nombre}' no encontrado")
    
    def listar_filtros(self):
        # Muestra todos los filtros automáticos
        if not self.filtros_automaticos:
            print("No hay filtros automáticos configurados")
            return
        
        print("\n--- FILTROS AUTOMÁTICOS ---")
        for nombre, config in self.filtros_automaticos.items():
            estado = "ACTIVO" if config["activo"] else "INACTIVO"
            print(f"• {nombre}: {config['criterio']}='{config['valor']}' → {config['carpeta_destino']} [{estado}]")
    
    def aplicar_filtros_automaticos(self, mensaje):
        # Aplica todos los filtros automáticos a un mensaje nuevo
        mensaje_movido = False
        
        for nombre, config in self.filtros_automaticos.items():
            if not config["activo"]:
                continue
                
            criterio = config["criterio"]
            valor = config["valor"]
            carpeta_destino_nombre = config["carpeta_destino"]
            
            # Buscar carpeta destino
            carpeta_destino = self.buscar_carpeta(carpeta_destino_nombre)
            if not carpeta_destino:
                continue
            
            # Aplicar filtro según criterio
            if criterio == "asunto" and valor in mensaje.get_asunto().lower():
                self._mover_mensaje_con_filtro(mensaje, carpeta_destino, nombre)
                mensaje_movido = True
                
            elif criterio == "remitente" and valor in str(mensaje.get_remitente()).lower():
                self._mover_mensaje_con_filtro(mensaje, carpeta_destino, nombre)
                mensaje_movido = True
                
            elif criterio == "prioridad" and valor == mensaje.get_prioridad():
                self._mover_mensaje_con_filtro(mensaje, carpeta_destino, nombre)
                mensaje_movido = True
                
            elif criterio == "etiqueta" and mensaje.tiene_etiqueta(valor):
                self._mover_mensaje_con_filtro(mensaje, carpeta_destino, nombre)
                mensaje_movido = True
        
        return mensaje_movido
    
    def _mover_mensaje_con_filtro(self, mensaje, carpeta_destino, nombre_filtro):
        # Mueve un mensaje aplicando un filtro automático
        carpeta_actual = None
        for carpeta in self.carpetas:
            if mensaje in carpeta.mensajes:
                carpeta_actual = carpeta
                break
        
        if carpeta_actual and carpeta_actual != carpeta_destino:
            carpeta_actual.mover_mensaje(mensaje, carpeta_destino)
            print(f"✓ Filtro '{nombre_filtro}' movió mensaje a '{carpeta_destino.get_nombre()}'")
    
    def agregar_a_cola_urgentes(self, mensaje):
        # Agrega un mensaje urgente a la cola de prioridades
        if mensaje.es_mensaje_urgente() and mensaje not in self.cola_urgentes:
            self.cola_urgentes.append(mensaje)
            # Ordenar por prioridad (urgente primero)
            self.cola_urgentes.sort(key=lambda m: m.get_prioridad() == "urgente", reverse=True)
    
    def obtener_siguiente_urgente(self):
        # Obtiene el siguiente mensaje urgente de la cola
        if self.cola_urgentes:
            return self.cola_urgentes[0]
        return None
    
    def procesar_siguiente_urgente(self):
        # Procesa y remueve el siguiente mensaje urgente
        if self.cola_urgentes:
            mensaje_urgente = self.cola_urgentes.pop(0)
            print(f" MENSAJE URGENTE: De {mensaje_urgente.get_remitente()} - {mensaje_urgente.get_asunto()}")
            return mensaje_urgente
        else:
            print("No hay mensajes urgentes en la cola")
            return None
    
    def mostrar_cola_urgentes(self):
        # Muestra la cola de mensajes urgentes
        if not self.cola_urgentes:
            print("No hay mensajes urgentes en la cola")
            return
        
        print("\n--- COLA DE MENSAJES URGENTES ---")
        for i, mensaje in enumerate(self.cola_urgentes, 1):
            print(f"{i}. De: {mensaje.get_remitente()} - Asunto: {mensaje.get_asunto()} - Prioridad: {mensaje.get_prioridad()}")
    
    def contar_urgentes(self):
        # Cuenta cuantos mensajes urgentes hay en la cola
        return len(self.cola_urgentes)
        
