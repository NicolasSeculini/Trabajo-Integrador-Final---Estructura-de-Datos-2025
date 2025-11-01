from carpetas import Carpeta

class Mensaje(object):
    def __init__(self):
        self.remitente = None
        self.destinatario = None
        self.asunto = None
        self.cuerpo = None
        self.leido = False
        self.prioridad = "normal"  # normal, alta, urgente
        self.etiquetas = []  # etiquetas para filtros automáticos
        self.fecha = None  # fecha de creación del mensaje
        self.es_urgente = False  # marcador de urgencia
        
    def set_remitente(self,usuario):
        self.remitente = usuario
    
    def get_remitente (self):
        return self.remitente
    
    def set_destinatario(self,servidor):
        #Permite settear el destinatario 
        destinatario = input("Ingrese el destinatario: ")
        for us in servidor.usuarios_registrados:
            #Aqui busca la coincidencia entre el nombre ingresado y el atributo nombre de cada usuario registrado en el servidor
            if destinatario == us.get_nombre():
                self.destinatario = us
                return 
        raise ValueError ("No se encontro un usuario con ese nombre")
        #Si la coindicion se cumple, setteara el usuario, sino mostrara el error
        
    def get_destinatario(self):
        return self.destinatario
    
    def set_asunto(self):
        #Settea el asunto
        asunto = input("ingrese el asunto: ")
        self.asunto = asunto
        
    def get_asunto(self):
        return self.asunto
    
    def set_cuerpo(self):
        #settea el cuerpo
        cuerpo = input("Ingrese el cuerpo: ")
        self.cuerpo = cuerpo
        
    def get_cuerpo(self):
        return self.cuerpo
    
    def marcar_leido(self):
        #Cambia el estado de leido
        if self.leido ==False:
            self.leido = True

    def set_prioridad(self, prioridad):
        # Permite establecer la prioridad del mensaje
        prioridades_validas = ["normal", "alta", "urgente"]
        if prioridad in prioridades_validas:
            self.prioridad = prioridad
            self.es_urgente = (prioridad == "urgente")
        else:
            raise ValueError("Prioridad debe ser: normal, alta o urgente")
    
    def get_prioridad(self):
        return self.prioridad
    
    def marcar_urgente(self):
        # Marca el mensaje como urgente
        self.prioridad = "urgente"
        self.es_urgente = True
    
    def es_mensaje_urgente(self):
        # Verifica si el mensaje es urgente
        return self.es_urgente
    
    def agregar_etiqueta(self, etiqueta):
        # Agrega una etiqueta al mensaje para filtros automáticos
        if etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)
    
    def quitar_etiqueta(self, etiqueta):
        # Remueve una etiqueta del mensaje
        if etiqueta in self.etiquetas:
            self.etiquetas.remove(etiqueta)
    
    def get_etiquetas(self):
        # Retorna las etiquetas del mensaje
        return self.etiquetas
    
    def tiene_etiqueta(self, etiqueta):
        # Verifica si el mensaje tiene una etiqueta específica
        return etiqueta in self.etiquetas
    
    def set_fecha(self, fecha):
        # Establece la fecha del mensaje
        self.fecha = fecha
    
    def get_fecha(self):
        # Retorna la fecha del mensaje
        return self.fecha

