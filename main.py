from servidor import ServidorCorreo

main = ServidorCorreo()
main.crear_usuario()
main.crear_usuario()
main.log_in()

main.enviar_mensaje()
main.recibir_mensaje()


#La idea es que se cree el servidor, crear 2 usuarios, loggear en uno. Desde ahi que permita enviar y recibir el mensaje
# y ver una forma de comprobar de que llego a la carpeta destino