from usuario import Usuario
from carpetas import Carpeta
from mensaje import Mensaje

class ServidorCorreo(object):
    def __init__(self):
        self.usuarios_registrados = [] #En  la lista se encontraran todos los usuarios registrados en el servidor de mensajeria
        self.estado = False #Atributo que permite verificar si hay o no un usuario logeado
        self.usuario_activo = [] #Esta lista permite verificar cual es el usuario activo
        self.mensaje_para_enviar = [] #lugar donde se guarda el mensaje antes de ser enviado a la carpeta destino
        
    def log_in(self): #El metodo log_in permite verificar que siempre a realizar una accion, haya un usuario logeado
        user = input("Ingrese su usuario: ")
        
        if self.estado == False: #Verifica que no haya alguien loggeado
            for usuario in self.usuarios_registrados:
                if usuario.get_nombre() == user: #Busca la coincidencia con los usuarios registrados
                    password = input("Ingrese su contraseña: ") #Si existe coincidencia, pide contraseña
                    if password == usuario.get_contraseña():
                        self.estado = True #Si encuentra coincidencia, pasa el estado a True
                        self.usuario_activo.append(usuario) #Agrega el usuario a la lista de usuario activo
                        print(f"Bienvenido {usuario.get_nombre()}!")
                        return
            print("Usuario o contraseña incorrectos")
        else:
            print("Ya hay un usuario logueado")
                        
    def crear_usuario(self):
        nuevo_usuario = Usuario() #Crea una instancia de la clase Usuario()
        self.usuarios_registrados.append(nuevo_usuario) #Lo agrega a la lista de usuarios registrados en el servidor
    
    def enviar_mensaje(self):
        if not self.usuario_activo:  # Verifica si la lista está vacía
            print("ERROR: No hay usuario activo. Debe hacer login primero.")
            return
        
        nuevo_mensaje = Mensaje()
        nuevo_mensaje.set_remitente(self.usuario_activo[0]) #Toma de remitente al usuario que se encuentra loggeado
        nuevo_mensaje.set_destinatario(self) #Recibe de parametro self, para buscar dentro del mismo servidor el usuario al que se quiera enviar el mensaje
        nuevo_mensaje.set_asunto() #Permite agregar el asunto
        nuevo_mensaje.set_cuerpo() #Permite agregar el cuerpo
        self.mensaje_para_enviar.append(nuevo_mensaje) #Manda el mensaje 
        print("Mensaje enviado exitosamente!")
    
    def recibir_mensaje(self):
        if len(self.mensaje_para_enviar[0].destinatario.carpetas) == 0: #Verifica si hay o no carpetas creadas en el usuario
            carpeta_nueva = Carpeta() #Si no existe crea una
            carpeta_nueva.set_nombre("Mensajes sin leer") #Le asigna el nombre de "Mensajes sin leer"
            self.mensaje_para_enviar[0].destinatario.carpetas.append(carpeta_nueva) 
            carpeta_nueva.agregar_mensaje(self.mensaje_para_enviar[0]) #Le agrega el mensaje
            self.mensaje_para_enviar.pop(0) #Quita el mensaje de la lista de mensaje por enviar
        else:
            for carp in self.mensaje_para_enviar[0].destinatario.carpetas: #si habia al menos una carpeta
                if carp.get_nombre() == "Mensajes sin leer": #Busca la que sea "Mensajes sin leer"
                    carp.agregar_mensaje(self.mensaje_para_enviar[0]) #Agrega el mensaje
                    self.mensaje_para_enviar.pop(0) #Lo quita de la lista de mensaje por enviar
