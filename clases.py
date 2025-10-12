class ServidorCorreo (object):
    def __init__(self):
        self.usuarios_registrados = []
        self.estado = False
        self.usuario_activo = []
        self.mensaje_para_enviar = []
        

        
    def log_in(self): #El metodo log_in permite verificar que siempre a realizar una accion, haya un usuario logeado (Esto para autocompletar directamente quien es el que envia un mensaje a otro usuario)
        user = input("ingrese su usuario: ")
        if self.estado == False:
            for us in self.usuarios_registrados:
                if us.nombre == user:
                    password = input("Ingrese su contraseña: ")
                    if password == us.contraseña:
                        self.estado = True
                        
                        self.usuario_activo.append(us)
                    
    def crear_usuario(self):
        nuevo_usuario = Usuario()
        nuevo_usuario.set_nombre()
        nuevo_usuario.set_contraseña()
        self.usuarios_registrados.append(nuevo_usuario)
    
    def enviar_mensaje(self):
        nuevo_mensaje = Mensaje()
        nuevo_mensaje.set_remitente(self.usuario_activo[0])
        nuevo_mensaje.set_destinatario(self)
        nuevo_mensaje.set_asunto()
        nuevo_mensaje.set_cuerpo()
        self.mensaje_para_enviar.append(nuevo_mensaje)
    
    def recibir_mensaje(self):
        if self.mensaje_para_enviar[0].destinatario.carpetas.len() == 0:
            carpeta_nueva = Carpeta()
            self.mensaje_para_enviar[0].destinatario.carpetas.append(carpeta_nueva)
            carpeta_nueva.set_nombre_sin_leer("Mensajes sin leer")
            carpeta_nueva.agregar_mensaje(self.mensaje_para_enviar[0])
            self.mensaje_para_enviar.pop(0)
        else:
            for carp in self.mensaje_para_enviar[0].destinatario.carpetas:
                if carp.nombre == "Mensajes sin leer":
                    carp.agregar_mensaje(self.mensaje_para_enviar[0])
                    self.mensaje_para_enviar.pop(0)

class Usuario(object):
    def __init__(self):
        self.nombre = None
        self.contraseña = None
        self.carpetas = []
    def __str__(self):
        return f"Usuario: {self.nombre}."
        
    def set_nombre (self):
        nuevo_nombre = input("Ingrese un nombre de usuario: ")
        self.nombre = nuevo_nombre
        
    def get_nombre (self):
        return self.nombre
    
    def set_contraseña(self):
        nueva_contraseña = input("ingrese una contraseña: ")
        self.contraseña = nueva_contraseña
        
    def get_contraseña(self):
        return self.contraseña
    
class Mensaje (object):
    def __init__(self):
        self.remitente =  None
        self.destinatario = None
        self.asunto = None
        self.cuerpo = None
        self.leido = False
        
    def set_remitente (self, usuario):
        self.remitente = usuario
    
    def get_remitente (self):
        return self.remitente
    
    def set_destinatario (self, servidor): #Este metodo para setear el destinatario exije el argumento de servidor para poder buscar automaticamente en los usuarios la coincidencia con el del input
        destinatario = input("Ingrese el destinatario: ")
        for us in servidor.usuarios_registrados:
            if destinatario == us.nombre:
                self.destinatario = us
        
            
    
    def get_remitente (self):
        return self.remitente
    
    def set_asunto(self):
        asunto = input("Ingrese el asunto: ")
        self.asunto = asunto
        
    def get_asunto(self):
        return self.asunto
    
    def set_cuerpo(self):
        cuerpo = input("Ingrese el cuerpo del mensaje: ")
        self.cuerpo = cuerpo

    def get_cuerpo(self):
        return self.cuerpo    
        
        
    def marcar_leido(self):
        if self.leido == False:
            self.leido = True

class Carpeta (object):
    def __init__(self):
        self.nombre = None
        self.mensajes = []
    def set_nombre_sin_leer(self, nombre):
        self.nombre = nombre
    
    def set_nombre(self):
        nombre_carpeta =input("Ingrese el nombre de su nueva carpeta: ")
        self.nombre = nombre_carpeta
        
    def get_nombre(self):
        return self.nombre
    
    def agregar_mensaje (self,mensaje):
        if mensaje is type(Mensaje):
            self.mensajes.insert(0,mensaje)
            
    def quitar_mensaje (self, mensaje):
        if mensaje is type(Mensaje):
            indice = mensaje.index()
            self.mensajes.pop(indice)
            
    def lista_mensajes(self):
        for men in self.mensajes:
            print(f"""
De:{men.remintente}
Asunto: {men.asunto}
""")
            
