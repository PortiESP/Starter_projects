import os, socket, re, time
# Este programa hace un ping a un ordenador en la red


# Creamos el archivo de las ip guardados si no existe ya
if not os.path.exists('lista_ip.txt'):
	with open('lista_ip.txt', 'w') as lista:
		pass





def menu_1():
	print()
	print()
	print(" 	+----------------------------------+")
	print(" 	|                                  |")
	print(" 	|             PING-IP              |")
	print(" 	|                                  |")
	print(" 	|----------------------------------|")
	print(" 	|                                  |")
	print(" 	|   1.- Hacer ping                 |")
	print(" 	|   2.- Ver mi ip                  |")
	print(" 	|   3.- Rastrear red               |")
	print(" 	|   4.- Indentificar ip guardada   |") 
	print(" 	|   5.- Desactiva conexion WIFI    |")	
	print(" 	|                                  |")
	print(" 	+----------------------------------+")


	opcion = ""
	while opcion not in ["1", "2", "3", "4", "5"]:
		opcion = input("\n 	--> ")

	return opcion







def menu_1_1():
	print()
	print(" 		Escriba la direccion una de la lista")
	print()
	print(" 		Direcciones guardadas")
	print()
	imprimir_direcciones()
	print()
	direccion = ""
	while direccion == "":
		direccion = input(" 		--> ")
		if direccion == 'q':
			return None
		resultado = comprobar_ip(direccion)
		if resultado == False:
			print()
			print(" 		***Direccion no encontrada***")
			direccion=""

	return direccion








def comprobar_ip(direccion):
	os.system('ping -n 1 -l 1 {} > log.txt'.format(direccion))
	with open('log.txt', 'r') as log:
		lineas = log.readlines()
	try:
		x = re.findall('bytes=1', lineas[2])
		if x:
			return True
		else: 
			return False
	except IndexError:
		return False









def imprimir_direcciones():
	for ip in lista_direcciones:
		datos = ip.strip().split(';')
		print(" 		" + datos[0] + " - " + datos[1])


def lista_ips():
	lista = []
	for i in lista_direcciones:
		lista.append(i.strip().split(';'))
	return lista




def hacer_ping(direccion):
	os.system('cls')
	print()
	paquetes = '0'
	print(" 		Selecciona la cantidad de paquetes (q = infinitos)")
	while paquetes == '0' and paquetes != "q" and paquetes != '':
		paquetes = input(" 		--> ")
	
	peso=''
	while peso == '' or int(peso) <= 1:
		peso = input(" 		Peso en bytes: ")

	os.system('cls')
	print()
	print(" 		PING  --->  {}".format(direccion))
	print()
	if paquetes == 'q':
		print(" 		Enviando paquetes...")
		os.system('ping -t {} > log.txt'.format(direccion))
	else:
		print(" 		Enviando paquetes...")
		os.system('ping -n {cantidad} -l {peso} {host} > log.txt'.format(cantidad=paquetes, peso=peso, host=direccion))

	print("\n 		PING finalizado")
	input(" 		Pulse enter para continuar...")





def obtener_ip_propia():
	nombreHost = socket.gethostname()
	miIP = socket.gethostbyname(nombreHost)
	return (nombreHost, miIP)


def menu_1_2():
	ip = obtener_ip_propia()
	print()
	print(" 		HOST: " + ip[0])
	print(" 		IP: " + ip[1])
	print()
	input(" 		ENTER para continuar")





def menu_1_3():
	print()
	print(" 		Ambito de la busqueda")
	respuesta = ''
	while respuesta == '':
		inicio = input(" 		Inicio: ")
		fin = input(" 		Fin: ")
		try:
			inicio = int(inicio)
			fin = int(fin)
			if inicio < fin and inicio >= 0 and fin <= 257:
				respuesta='ok'
		except ValueError:
			pass
	os.system('cls')
	ips = rastrear_red(inicio,fin)
	os.system('cls')
	print(" 		IPs en la red")
	print()
	for i in ips:
		print(" 		" + i[0] + " - '" + i[1] + "'")
	print(" 		--------------------------------")
	print()
	respuesta=''
	while respuesta not in ['s','n']:
		respuesta = input(" 		Desea guardar las direcciones encotradas [s/n]? --> ").lower()
	if respuesta == 's':
		with open('lista_ip.txt','w') as archivo:
			for i in ips:
				archivo.write(i[0]+";"+i[1]+'\n')
		input("\n 		Guardado...")


			




def rastrear_red(inicio, fin):
	print(' 		Ctrl+c para interrumpir la busqueda')
	ips = []
	strx = '192.168.1.'
	for i in range(inicio,fin):
		ip = strx+str(i)
		print(' 		Comprobando...'+ip)
		if comprobar_ip(strx+str(i)):
			if ip == '192.168.1.1':
				host = ('Rooter',[])
			else:
				try:
					host = socket.gethostbyaddr(ip)
				except socket.herror:
					host = ['No name found', []]
			print(" 		Encontrado..."+ip+" - "+host[0])
			ips.append((ip, host[0]))
	return ips


def menu_1_4():

	print()
	print(" 		IPs guardadas:")
	print()
	imprimir_direcciones()
	print(" 		---------------------------")
	print()
	while True:
		direccion = input(" 		Introduce una direccion --> ")
		for i in lista_ips():
			if direccion in i or direccion == 'q':
				return direccion
			


		
		

	
def nombrar_ip(direccion):
	print()
	nuevaLista = []
	for i in lista_ips():
		if i[0] == direccion:
			nombre = input(" 		Nombre: ")
			i[1]=nombre
		nuevaLista.append(i[0] + ';' + i[1]+'\n')

	with open('lista_ip.txt', 'w') as archivo:
		archivo.writelines(nuevaLista)
	print(" 		Renombrado con exito")
	




def menu_1_5():
	print()
	print(" 		Desconectar conexiones:")
	print()
	print(" 		1.- Hasta reactivacion manual")
	print(" 		2.- Limite de tiempo")
	print()
	opcion = ""
	while opcion not in ['1', '2']:
		opcion = input(" 		--> ")
	if opcion == '1':
		os.system('cls')
		print()
		input(" 		Pulsa ENTER para desactivar")
		os.system('ipconfig/release > log.txt')

		os.system('cls')
		os.system('color 0c')
		print()
		print(" 		***CONEXION DESACTIVADA***")
		input(" 		Pulsa ENTER para activar")
		os.system('ipconfig/renew > log.txt')


		os.system('cls')
		os.system('color 0a')
		print()
		print(" 		***CONEXION ACTIVADA***\n")
		input(" 		Pulsa ENTER para continuar...")
		os.system('color 07')

		return None

	elif opcion == '2':
		os.system('cls')
		print()
		tiempo = input(" 		Tiempo de desconexion --> ")
		input(" 		{} segundos de desconexion, enter para aceptar...".format(tiempo))
		tiempo = int(tiempo)
		
		os.system('cls')
		os.system('ipconfig/release > log.txt')
		os.system('color 0c')
		restantes = tiempo
		for i in range(tiempo):
			os.system('cls')
			print()
			print(" 		***CONEXION DESACTIVADA***")
			print()
			print(" 		{} segundos restantes".format(str(restantes)))
			restantes-=1
			time.sleep(1)

		os.system('cls')
		os.system('ipconfig/renew > log.txt')
		os.system('color 0a')
		print()
		print(" 		CONEXION ACTIVADA")
		print()
		input(" 		Pulsa ENTER para continuar")
		os.system('color 07')

		return None












######################FLUJO DEL PROGRAMA####################
while True:

	with open('lista_ip.txt', 'r') as archivo:
		lista_direcciones = archivo.readlines()

	# Menu de inicio
	os.system('cls')
	opcion_menu_1 = menu_1()

	if opcion_menu_1 == "1":
		os.system('cls')
		opcion_menu_1_1 = menu_1_1()
		if opcion_menu_1_1 != None:
			hacer_ping(opcion_menu_1_1)

	elif opcion_menu_1 == "2":
		os.system('cls')
		menu_1_2()

	elif opcion_menu_1 == "3":
		os.system('cls')
		menu_1_3()

	elif opcion_menu_1 == "4":
		os.system('cls')
		direccion = menu_1_4()
		if direccion != 'q':
			nombrar_ip(direccion)

	elif opcion_menu_1 == "5":
		os.system('cls')
		menu_1_5()



############################################################
	





input("Saliendo del programa...")