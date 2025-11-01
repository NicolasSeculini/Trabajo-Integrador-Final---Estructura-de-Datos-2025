class Carpeta(object):
    def __init__(self, nombre=None, padre=None):
        self.nombre = nombre
        self.padre = padre
        self.mensajes = []
        self.subcarpetas = []  # Lista para subcarpetas (estructura recursiva)
        self._ruta_cache = None
        
    def set_nombre(self, nombre): #Sirve para que el servidor pueda crear la carpeta de mensajes sin leer
        if self.nombre is None:
            self.nombre = nombre
        else:
            raise ValueError("El nombre ya fue agregado")
    
    def cambiar_nombre(self, nuevo_nombre=None): #Este es el que sirve para cambiar el nombre de una carpeta
        if self.get_nombre() != "Mensajes sin leer": #Utiliza la verificacion para impedir que no deje de existir la carpeta de Mensajes sin leer
            if nuevo_nombre is None:
                nuevo_nombre = input("Ingrese el nuevo nombre de la carpeta: ")
            self.nombre = nuevo_nombre
            self._ruta_cache = None
        else:
            raise ValueError("La carpeta Mensajes sin leer no puede modificar su nombre")
        
    
    def get_nombre(self):
        return self.nombre
    
    def get_ruta(self):
        # Calcula la ruta completa de la carpeta (padre/hijo)
        if self._ruta_cache is None:
            if self.padre is None:
                self._ruta_cache = self.nombre
            else:
                self._ruta_cache = f"{self.padre.get_ruta()}/{self.nombre}"
        return self._ruta_cache
    
    def agregar_subcarpeta(self, nombre_subcarpeta):
        # Crea y agrega una nueva subcarpeta a esta carpeta
        if self.buscar_subcarpeta(nombre_subcarpeta):
            raise ValueError(f"Ya existe una subcarpeta con el nombre '{nombre_subcarpeta}'")
        
        nueva_carpeta = Carpeta(nombre_subcarpeta, self)
        self.subcarpetas.append(nueva_carpeta)
        return nueva_carpeta
    
    def buscar_subcarpeta(self, nombre):
        # Busca una subcarpeta por nombre (solo en subcarpetas directas)
        for carpeta in self.subcarpetas:
            if carpeta.get_nombre() == nombre:
                return carpeta
        return None
    
    def buscar_subcarpeta_recursivo(self, nombre):
        # Busca una subcarpeta por nombre en todo el árbol de carpetas
        if self.nombre == nombre:
            return self
            
        for subcarpeta in self.subcarpetas:
            resultado = subcarpeta.buscar_subcarpeta_recursivo(nombre)
            if resultado:
                return resultado
        return None
    
    def obtener_todas_subcarpetas(self):
        # Obtiene todas las subcarpetas recursivamente (incluyendo esta carpeta)
        todas = [self]
        for subcarpeta in self.subcarpetas:
            todas.extend(subcarpeta.obtener_todas_subcarpetas())
        return todas
    
    def buscar_mensajes_recursivo(self, criterio, valor):
        resultados = []
        
        # Buscar en mensajes de esta carpeta
        for mensaje in self.mensajes:
            if criterio == 'asunto' and valor.lower() in mensaje.get_asunto().lower():
                resultados.append((mensaje, self))  # Guardar mensaje y carpeta donde se encontró
            elif criterio == 'remitente' and valor.lower() in str(mensaje.get_remitente()).lower():
                resultados.append((mensaje, self))
        
        # Busqueda recursiva en subcarpetas
        for subcarpeta in self.subcarpetas:
            resultados.extend(subcarpeta.buscar_mensajes_recursivo(criterio, valor))
        
        return resultados
    
    def mover_mensaje(self, mensaje, carpeta_destino):
        # Mueve un mensaje de esta carpeta a otra carpeta
        if mensaje in self.mensajes:
            self.mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            return True
        return False
    
    def mover_mensaje_por_ruta(self, mensaje, ruta_destino):
        # Mueve un mensaje a una carpeta destino especificada por ruta completa
        carpeta_destino = self._buscar_carpeta_por_ruta(ruta_destino)
        if carpeta_destino:
            return self.mover_mensaje(mensaje, carpeta_destino)
        return False
    
    def _buscar_carpeta_por_ruta(self, ruta):
        # Busca una carpeta por su ruta completa (ej: "Principal/Trabajo/Proyectos")
        if ruta == self.get_ruta():
            return self
            
        partes = ruta.split('/')
        if partes[0] != self.nombre:
            return None
            
        carpeta_actual = self
        for parte in partes[1:]:
            encontrado = False
            for subcarpeta in carpeta_actual.subcarpetas:
                if subcarpeta.get_nombre() == parte:
                    carpeta_actual = subcarpeta
                    encontrado = True
                    break
            if not encontrado:
                return None
        return carpeta_actual
    
    def agregar_mensaje(self, mensaje):
        #Agrega mensaje verificando primero que sea una instancia de Mensaje()
        if isinstance(mensaje, Mensaje):
            self.mensajes.insert(0,mensaje)  # Insertar al inicio para mensajes más recientes primero
        else:
            raise ValueError("No se pudo guardar el mensaje")
        
    def quitar_mensaje(self, mensaje):
        #Quita mensaje verificando primero que sea una instancia de Mensaje()
        if isinstance(mensaje, Mensaje):
            if mensaje in self.mensajes:
                self.mensajes.remove(mensaje)
    
    def lista_mensajes(self):
        # Imprime cada mensaje de la carpeta con su estado
        if not self.mensajes:
            print("No hay mensajes en esta carpeta")
            return
            
        for i, men in enumerate(self.mensajes):
            estado = "LEÍDO" if men.leido else "NO LEÍDO"
            print(f"{i+1}. mensaje de {men.get_remitente()}. Con asunto: {men.get_asunto()}. [{estado}]")
    
    def lista_subcarpetas(self, recursivo=False):
        # Lista las subcarpetas de esta carpeta
        if not self.subcarpetas:
            print("No hay subcarpetas")
            return
            
        if recursivo:
            # Lista recursiva de todas las subcarpetas
            todas_carpetas = self.obtener_todas_subcarpetas()
            for carpeta in todas_carpetas[1:]:  # Excluir esta carpeta
                print(f"- {carpeta.get_ruta()} ({len(carpeta.mensajes)} mensajes)")
        else:
            # Lista solo subcarpetas directas
            for carpeta in self.subcarpetas:
                print(f"- {carpeta.get_nombre()} (ruta: {carpeta.get_ruta()})")
    
    def estadisticas(self):
        # Muestra estadisticas de la carpeta y todas sus subcarpetas
        todas_carpetas = self.obtener_todas_subcarpetas()
        total_mensajes = sum(len(carpeta.mensajes) for carpeta in todas_carpetas)
        
        print(f"\n--- Estadísticas de '{self.get_ruta()}' ---")
        print(f"Mensajes en esta carpeta: {len(self.mensajes)}")
        print(f"Total mensajes en árbol: {total_mensajes}")
        print(f"Subcarpetas directas: {len(self.subcarpetas)}")
        print(f"Total subcarpetas: {len(todas_carpetas) - 1}")  # Excluye esta carpeta
        print(f"Profundidad máxima: {self._calcular_profundidad()}")
    
    def _calcular_profundidad(self):
        # Calcula la profundidad maxima del árbol de carpetas
        if not self.subcarpetas:
            return 1
        return 1 + max(subcarpeta._calcular_profundidad() for subcarpeta in self.subcarpetas)
    
    def eliminar_subcarpeta(self, nombre):
        # Elimina una subcarpeta y mueve sus mensajes a esta carpeta
        for i, subcarpeta in enumerate(self.subcarpetas):
            if subcarpeta.get_nombre() == nombre:
                # Mover mensajes a carpeta padre antes de eliminar
                for mensaje in subcarpeta.mensajes[:]:
                    self.agregar_mensaje(mensaje)
                # Eliminar subcarpeta
                return self.subcarpetas.pop(i)
        return None
