class Mensaje(object):
    def __init__(self):
        self.remitente =  None
        self.destinatario = None
        self.asunto = None
        self.cuerpo = None
        self.leido = False
        
    def set_remitente(self,usuario):
        self.remitente = usuario
    
    def get_remitente (self):
        return self.remitente
    
    def set_destinatario(self,servidor):
        #Permite settear el destinatario 
        destinatario = input("Ingrese el destinatario: ")
        for us in servidor.usuarios_registrados:
            #Aqui busca la coincidencia entre el nombre ingresado y el atributo nombre de cada usuario registrado en el servidor
            if destinatario == us.nombre:
                self.destinatario = us
        else:
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