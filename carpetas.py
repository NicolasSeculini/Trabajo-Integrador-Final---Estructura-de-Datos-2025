from mensaje import Mensaje


class Carpeta(object):
    def __init__(self):
        self.nombre = None
        self.mensajes = []
        
    def set_nombre(self, nombre): #sirve para que el servidor pueda creear la carpeta de mensajes sin leer
        if self.nombre is None:
            self.nombre = nombre
        else:
            raise ValueError("El nombre ya fue agregado")
    
    def cambiar_nombre(self): #Este es el que sirve para cambiar el nombre de una carpeta
        if self.get_nombre() != "Mensajes sin leer": #Utiliza la verificacion para impedir que no deje de existir la carpeta de Mensajes sin leer
            nuevo_nombre = input("Ingrese el nuevo nombre de la carpeta: ")
            self.nombre = nuevo_nombre
        else:
            raise ValueError("La carpeta Mensajes sin leer no puede modificar su nombre")
        
    
    def get_nombre(self):
        return self.nombre
    
    def agregar_mensaje(self, mensaje):
        #Agrega mensaje verificando primero que sea una instancia de Mensaje()
        if isinstance(mensaje, Mensaje):
            self.mensajes.insert(0,mensaje)
        else:
            raise ValueError("No se pudo guardar el mensaje")
        
    def quitar_mensaje(self, mensaje):
        #Quita mensaje verificando primero que sea una instancia de Mensaje()
        if isinstance(mensaje,Mensaje):
            indice = self.mensajes.index(mensaje) #Adquiere el indice donde se encuentra el mensaje
            self.mensajes.pop(indice) #Luego lo quita
    
    def lista_mensajes(self):
        for men in self.mensajes: #Imprime cada mensaje de la carpeta
            print("mensaje de " + men.get_remitente() + ". Con asunto: " + men.get_asunto() + ".")
