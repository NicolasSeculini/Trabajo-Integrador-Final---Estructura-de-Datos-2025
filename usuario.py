class Usuario(object):
    def __init__(self):
        self.set_nombre()
        self.set_contraseña()
        self.carpetas = []
    
    def __str__(self):
        return "Usuario:" + self.get_nombre()
    
    def set_nombre(self):
        #Permite settear el nombre con una verificacion de que sea un STR
        nuevo_nombre = input("Ingrese su nuevo nombre de usuario: ")
        
        if isinstance(nuevo_nombre,str):
            self._nombre = nuevo_nombre
        else:
            raise TypeError ("El nombre debe ser una cadena de caracteres")
    
    def get_nombre(self):
        #Permite el acceso al nombre de usuario
        return self._nombre
    
    def set_contraseña(self):
        #Permite settear la contraseña con una verificacion de que sea un STR
        nueva_contraseña = input("Ingrese su nueva contraseña: ")
        
        if isinstance(nueva_contraseña,str):
            self._contraseña = nueva_contraseña
        else:
            raise TypeError ("La contraseña debe ser una cadena de caracteres")
    
    def get_contraseña(self):
        #Permite el acceso a la contraseña del usuario
        return self._contraseña
