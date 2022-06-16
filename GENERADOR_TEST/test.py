"""
		PENDIENTE

		- Hacer modulos para menus
"""

import random,os, time
from io import *


def listar_usuarios():

	"""
		Esta funcion abrira un archivo de datos, leera sus lineas y las guardara en una lista,
		luego esa lista la recorrera para a cada uno de sus elementos hacerle: con strip() eliminamos
		los espacios y saltos de linea, con split(",") separaremos en otra sublista los elementos y el
		resultado los añaidremos como append a una nueva lista con listas dentro con los datos de todos 
		los usuarios, retornaremos esa lista para usarla mas tarde
		por lo que nos quedara una lista multidimensional
		!!!Los numeros vienen en tipo str y hay que pasarlos a int¡¡¡
	"""
	# archivo_datos = open("datos.txt", "r")
	# lineas_datos = archivo_datos.readlines()
	# archivo_datos.close()

	# Equivalente a lo de arriba
	with open("datos.txt", "r") as archivo_datos:
		lineas_datos = archivo_datos.readlines()


	lista_usuarios = []
	for linea in lineas_datos:
		lista_usuarios.append(linea.strip().split(","))

	return lista_usuarios


def menu_entrada():
	"""
		Menu visual del primer meu del programa con las opciones

			- Entrar al sistema
			- Darse de alta
			- Salir

		Comprobamos que opcion ha elegido (while not in [])
	"""	
	print()
	print(" 		GENERADOR DE TEST")
	print(" 		   |")

	print('''		   |
		   |-  1.- Entrar al sistema
		   |-  2.- Darse de alta
		   |-  3.- Salir

		''')

	opcion = ""
	while opcion not in ["j","1","2","3"]:
		
		opcion = input(" 		Elige una opcion: ")
	
	return opcion






def entrar_al_sistema(lista_usuarios):
	print("\n 		------------INICIAR SESION------------\n")
	nombre=input(" 		Introduzca su nombre: ")
	contraseña=input(" 		Introduza su contraseña: ")

	for usuario in lista_usuarios:
		if usuario[0]==nombre and usuario[1]==contraseña:
			return usuario

	else:
		return None


	"""
		Crea dos input para pedir el usuario y contraseña
		los comprueba recorriendo con un for la lista pasada como parametro
		el for comprueba se en cada linea si esa line contiene ese usuario y esa contraseña
		retorna la linea con la que coinciden los datos osea el usuario
		la variable usuario sera igual a lista_usuarios[usuario] por lo que usuario[0] == lista_usuario[usuario][0]

	"""

def darse_de_alta(lista_usuarios):

	"""
		Registra un usuario y contraseña, comprueba que:
		 el usuario mida mas de 4 caracteres,
		 no este repetido  
		 la contraseña mida mas de 4 caracteres, 
		 pedimos la contraseña dos veces 
		para comprobar que la ha escrito bien, si coinciden las contraseñas y el nombre es valido,
		añadimos a la lista de usuarios el nuevo usuario !!!Si vamos a guardar numeros en un documento deben ser str¡¡¡
		retornamos la nueva lista
	"""
	while True:
		nombre, contraseña, repetirContraseña =[""]*3
		while len(nombre)<4:
			os.system('cls')
			print("\n 		--------------RERGISTRO--------------\n")
			nombre = input("\n 		Debe tener al menos 4 caracteres*\n 		NOMBRE --> ").lower()
		for i in lista_usuarios:
			if i[0]==nombre:
				os.system('cls')
				print("\n 		***El nombre {} esta en uso***".format(nombre))
				input("\n 		Presione intro para continuar")
				break
		else:
			while len(contraseña)<4:
				os.system('cls')
				print("\n 		--------------RERGISTRO--------------\n")
				print("\n 		NOMBRE: " + nombre)
				print()
				contraseña = input("\n 		Debe tener al menos 4 caracteres\n 		CONTRASEÑA --> ")
				if len(contraseña)>=4:
					repetirContraseña=input(" 		REPETIR_CONTRASEÑA --> ")
					if contraseña==repetirContraseña:
						os.system('cls')
						print()
						confirmacion=""
						while confirmacion not in ["s", "n"]:
							confirmacion = input('''		 NUEVO USUARIO:


		+---------------+
		|  NOMBRE       | {nombre}
		+---------------+
		|  CONTRASEÑA   | {contra}
		+---------------+

					¿Estas seguro? [s/n] '''.format(nombre=nombre, contra=contraseña)).lower()

						if confirmacion=="s":
							datos_nuevo_usuario = [nombre, contraseña, "0", "0", "0.00"]
							nueva_linea = ",".join(datos_nuevo_usuario)
							with open("datos.txt", 'a') as archivo_datos:
								archivo_datos.write(nueva_linea+"\n")
							os.system('cls')
							return "\n 		Ususario "+nombre+" creado con exito"
						else:
							return
					else:
						contraseña=""


def menu_principal(nombre_usuario):

	"""
		Menu visual al entrar al sistema donde se elige entre 

			- Hacer test
			- Puntuaciones
			- Salir

		El parametro nombre es para mostrarlo en el menu 
	"""

	print()
	print(" 		-------------------------------")
	print(" 		  Sesion iniciada {}".format(nombre_usuario[0]))
	print(" 		-------------------------------")
	print('''
			1.- Hacer test
			2.- Puntuaciones
			3.- Cerrar sesion
			''')
	opcion = ""
	# En este caso retornamos un str con un numero 
	while opcion not in ["1", "2", "3"]:
		opcion = input(" 		Seleccione una opcion: ")
	return opcion



def guardar_datos(lista_usuarios):	

	"""
		Esta funcion abre el documento datos y lo reescribe de nuevo con los cambios
	"""

	with open('datos.txt', 'w') as archivo_datos:
		for i in lista_usuarios:

			archivo_datos.write(i[0]+","+i[1]+","+i[2]+","+i[3]+","+i[4]+"\n")
	return None


def test(usuario):

	"""
		Crea un test de matematicas que obtendra cuantas respuestas acerto, las preguntas son
		operaciones generadas aleatoriamente y si acierta suma un punto
		al final retorna la puntuacion

		numero1 = random.randint((1*dificultad), (10*dificultad))
		numero2 = random.randint((1*dificultad), (10*dificultad))
	"""
	dificultad=1
	media = float(usuario[4])
	if media>=4: dificultad = 2
	if media>=6: dificultad = 3
	if media>=8: dificultad = 4
	lista_str = ["+", "-", "x", "/"]

	if dificultad==1:
			limite=5
	else:		
		limite=5+dificultad




	print()
	print(" 		TEST DE MATEMATICAS")
	print()
	print(" 		USUARIO: " + usuario[0]+"\n")
	print(" 		-----------------------------\n")
	print(f" 		Dificultad: {dificultad}")
	print(f" 		Preguntas:  {limite}")
	print(f" 		Media actual:  {usuario[4]}")
	print(" 		Las numeros seran entre "+ str(1*dificultad) + " y " + str(10*dificultad))
	print(" 		Tipos de operaciones: ", end=" ")
	try:
		for i in lista_str[0:dificultad]:
			print("["+i+"]", end=" ")
	except IndexError:
		for i in lista_str:
			print("["+i+"]", end=" ")

	print("\n")

	input(" 		Presiona enter para comenzar...")

	pregunta=0
	aciertos=0

	jugando=True
	while jugando:
		os.system('cls')
		pregunta+=1
		print('''
			 ----------------------
			   Pregunta {}
			 ----------------------
		'''.format(pregunta))

		
		numero1 = random.randint((1*dificultad), (10*dificultad))
		numero2 = random.randint((1*dificultad), (10*dificultad))
		try:
			signo = random.choice(lista_str[0:dificultad])
		except IndexError:
			signo = random.choice(lista_str)

		
		print(" 			 {} {} {} =".format(numero1, signo, numero2), end=" ")
		resultado=""
		while resultado=="":
			resultado = input()
			try:
				float(resultado)
			except ValueError:
				resultado=""
				print(" 		Introduzca numeros", end=" = ")
		
		if signo=="+":
			
			if int(resultado) == (numero1 + numero2):
				aciertos+=1
				print("\n 		Correcto!!!")
				input("\n 		Enter para la siguiente pregunta")
			else:
				print("\n 		Error, el resutado es: " + str(numero1 + numero2))
				input("\n 		Enter para la siguiente pregunta")

		if signo=="-":
			
			if int(resultado) == (numero1 - numero2):
				aciertos+=1
				print("\n 		Correcto!!!")
				input("\n 		Enter para la siguiente pregunta")
			else:
				print("\n 		Error, el resutado es: " + str(numero1 - numero2))
				input("\n 		Enter para la siguiente pregunta")

		if signo=="x":
			
			if int(resultado) == (numero1 * numero2):
				aciertos+=1
				print("\n 		Correcto!!!")
				input("\n 		Enter para la siguiente pregunta")
			else:
				print("\n 		Error, el resutado es: " + str(numero1 * numero2))
				input("\n 		Enter para la siguiente pregunta")

		if signo=="/":
			
			if int(resultado) == (round(numero1 / numero2), 2):
				aciertos+=1
				print("\n 		Correcto!!!")
				input("\n 		Enter para la siguiente pregunta")
			else:
				print("\n 		Error, el resutado es: " + str(round((numero1 / numero2),2)))
				input("\n 		Enter para la siguiente pregunta")

		

		if pregunta==limite:
			jugando=False

	os.system('cls')
	print()
	print(" 		Fin del test enhorabuena")
	print()
	print('''
			+-------------+-----+
			| PUNTUACION  |  {}  |
			+-------------+-----+ 
		'''.format(aciertos))

	input("\n 		Enter para continuar...")
	return aciertos


			




def actualizar_puntuacion(usuario, puntos):

	"""
		Se obtiene los datos de usuario donde pone nº partidas (int), mejor partida (int) y la media (float)
		-incrementamos el numero de partidas		
		-Si sus puntos han si mayores que su mejor puntuacion ponemos que ese indice se los puntos actuales
		-Si es su primera partida ponemos que la media se los puntos actuales
			Si no es su primera partida, sumamos su media y sus puntos actuales y dividimos entre 2

		Convertimos los nuevos datos otra vez a str y la media la redondeamos a 2 decimales con round(numero, decimales)
	"""
	npartidas = int(usuario[2])
	mejor = int(usuario[3])
	media = float(usuario[4])

	npartidas+=1
	if puntos > mejor:
		mejor = puntos
	if npartidas == 1:
		media = puntos
	else:
		media = (media + puntos)/2

	usuario[2] = str(npartidas)
	usuario[3] = str(mejor)
	usuario[4] = str(round(media, 2))

	return usuario


def mostrar_puntuacion(usuario):
	
	"""
		Muestra las puntuaciones del usuario pasado por parametros
	"""

	print()
	print('''

		+----------+------------------+---------+
		| Partidas | Mejor puntuacion | Media   |
		+----------+------------------+---------+
		     {}             {}             {} 
		
		'''.format(usuario[2], usuario[3], usuario[4]))

	input(" 		Enter para continuar...")


##############################FLUJO DEL PROGRAMA###################################
"""
- Creacion del archivo datos si no existe

- Bucle principal del programa
	- Establecemos que el test no se ha iniciado
	- Obtenemos lista de usuarios con listar usuarios
	- Comprobamos si quiere iniciar sesion o darse de alta o salir

		- Si inicia sesion, comprobamos credenciales con la lista retornada de listar usuarios y 
			-si sus credenciales son correctas retornara el usuario que lo asignaremos a una variable
			y permitiremos que se habra otro bucle con el siguiente menu 
			habrimos el siguiente menu de jugar o puntuaciones
			-si no acierta el usuario retornara none e imprimiremos un mensage de error 

				Si usuario es correcto
					- Si elegimos hacer test, se llama a la funcion test, al finalizar 
						llamamos a actualizar puntuacion con el usuario y la puntuacion del test
						y guardamos los datos

					- Se elegimos puntuacion, llamamos a la variable de ver puntuacion

					- Si elegimos salis cerramos el bucle que abre el menu principal y volvemos al
						iniciar sesion


		- Si se da de alta, se llama a la funcion darse_de_alta() y esta retorna la lista de usuarios 
			con el nuevo usuario por lo que debemos asignar la variable lista_usuarios a lo que retorne 
			esta funcion y guardamos los combios en el archivo datos con la funcion guardar_datos()

		- Se quiere salir cerramos el bucle con un break
	
"""
if not os.path.exists("datos.txt"):
	archivo_datos = open('datos.txt', 'w')
	archivo_datos.close()

while True:

	# Todavia no se ha iniciado sesion
	iniciada_sesion = False

	# Traemos lista multidimensional de los usuarios y sus datos
	lista_usuarios = listar_usuarios()

	os.system('cls')

	# Desplegamos el menu de inicio_sesion/darse_de_alta
	menu_1 = menu_entrada()

	os.system('cls')

	# Si elige iniciar sesion en menu_entrada
	if menu_1 == "1":
		
		# Recibimos el usuario
		usuario = None
		while usuario==None:
			os.system('cls')
			usuario = entrar_al_sistema(lista_usuarios)
			if usuario == None:
				print("\n\n 			***Credenciales incorrectas***")
				input("\n 		Enter para continuar")
			else:
				iniciada_sesion = True






	# Si elige darse de alta en menu_entrada
	elif menu_1 == "2":
		os.system('cls')
		print(darse_de_alta(lista_usuarios))
		input("\n 		Enter para continuar")

	# Si elige salir en menu_entrada
	elif menu_1 == "3":
		os.system('cls')
		print("\n 		Saliendo...")
		time.sleep(1)
		os.system('cls')
		break

	






	while iniciada_sesion:
		os.system('cls')
		menu_2 = menu_principal(usuario)

		# Para no tener que transformar a int ponemos que esperamos un 1 de tipo str
		if menu_2=="1":
			os.system('cls')
			puntos = test(usuario)
			actualizar_puntuacion(usuario, puntos)
			guardar_datos(lista_usuarios)

		elif menu_2=="2":
			os.system('cls')
			mostrar_puntuacion(usuario)

		elif menu_2 == "3":
			iniciada_sesion = False


		



	

