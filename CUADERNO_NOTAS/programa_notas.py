




import os, glob, time
from io import *

ruta = os.getcwd()+"\\"

# Crea el archivo de datos que almacena los nombre de las notas si no existe
# Contiene dos lineas de placeholder
if not os.path.exists('datos.txt'):
	archivo_datos = open('datos.txt', 'w')
	archivo_datos.write("Nombres de las notas \n\n")
	archivo_datos.close()



# ---------------------------------------------------------------------------

def contar_notas():
	"""
		CUENTA LA CANTIDAD DE ARCHIVOS.TXT EN LA CARPETA NOTAS
	"""
	return len(glob.glob(ruta+"notas/*.txt"))

# --------------------------------------------------------------------------
def lista_notas():

	"""
		Crea una lista con un indice y el nombre de la nota
		nº.- nombre_nota
	"""

	# Obtiene una lista con las lineas
	archivo_datos = open('datos.txt', 'r')
	lineas = archivo_datos.readlines()
	archivo_datos.close()

	# Contador que sirve para mostrar el indice de una nota
	contador=0
	
	for i in lineas[2:]:
		contador+=1
		# i[:-2] imprime desde el principia hasta los dos ultimos caracteres
		print(' 			{}.- {}'.format(contador, i[:-1]))

	# Traemos solo las lineas que necesitamos, obiamos las de placeholder
	lineas2 = lineas[2:]
	lineas3 = []
	for i in lineas2:
		# Esto es para que no se añada a la lista el \n osea que elimina los 2 ultimos caracteres
		lineas3.append(i[:-1])

	return lineas3



# --------------------------------------------------------------------------
def inicio():
	"""
		CREA UNA LISTA DE OPCIONES (VISUAL)
		
	"""


	

	lista_opciones = ['CREAR NOTA', 'VER NOTA', 'RENOMBRAR NOTA', 'ELIMINAR NOTA', 'SALIR']
	print('''
			
			#############################################
			#                                           #
			#             CUADERNO DE NOTAS             #
			#                                           #
			#############################################

				NOTAS: {}
			
			====================NOTAS===================='''.format(contar_notas()))
	print()
	lista_notas()

	print('''
			=============================================

				1.- {0[0]}
				2.- {0[1]}
				3.- {0[2]}
				4.- {0[3]}
				5.- {0[4]}

		'''.format(lista_opciones))

	opcion=""
	while opcion not in ("1", "2", "3", "4", "5"):
		opcion = input("\n 		Elige una opcion --> ")

	return int(opcion)



# ---------------------------------------------------------------------------------- 
def existe_nota(nombre):
	
	"""
		COMPRUEBA SI UNA NOTA EXISTE EN EL ARCHIVO NOTAS
	"""

	if os.path.exists("notas/"+nombre+".txt"):
		return True
	else:
		return False




# -------------------------------------------------------------------------------------
def crear_nota():
	
	# Mientra no haya nombre
	nombre=None
	while nombre==None:
		
		nombre = input("\n		Nombre de la nota: ")
		# Si el nombre NO existe
		if not existe_nota(nombre):
			
			texto = print("\n 		*Deje una linea en blanco y luego intro para guardar*\n 		Indique el contenido:\n")
			# Crea una lista con cada linea de la nota para luego justarlas en un documento
			lista_lineas = []

			# Se inicia un bucle y se para cuando se elija la opcion de guardar
			guardado = False
			while guardado==False:
				# Se obtiene la linea y se almacena
				linea = input(" 			")

				# Para guardarlos se pedira que se deje una linea vacia
				# Comprobamos si ha dejado la linea vacia
				if linea=="":
					
					# Si la ha dejado preguntamos si quiere guardar
					pregunta = ""
					while pregunta!="s" and pregunta!="n":
						pregunta = input("\n 			Desea guardar los cambios [s/n] --> ").lower()
					
					# Si quiere guardar
					if pregunta == "s":
						# Cremaos el archivo con el nombre
						nueva_nota = open("notas/" + nombre + ".txt", "w")
						# Insertamos los elementos de la lista como lineas
						nueva_nota.writelines(lista_lineas)
						nueva_nota.close()

						# Abrimos el archivo datos
						append_nombre = open('datos.txt', 'a')
						# Añadimos la nota a la lista
						append_nombre.write(nombre+"\n")
						append_nombre.close()
						os.system('cls')
						# Seleccionamos que quiere guardar para cerrar el bucle
						guardado=True
						return "\n 		Nota creada con exito - NOMBRE: " + nombre

					# Si no quiere guardar volvemos al menu sin guardar
					if pregunta =="n":
						os.system('cls')
						return "\n 		Cambios no guardados"

				# Si la linea tiene contenido la añadimos a la lista de las lineas
				else:
					lista_lineas.append(linea+"\n")

		# Si el nombre ya existe
		else:
			os.system('cls')
			print( "\n 		***El nombre ya existe***")
			nombre=None



	
# -------------------------------------------------------------------------------------------

def ver_nota():
	print()
	print("\n 		Lista de notas:\n")
	print(" 			0.- Volver al menu*")
	# Se imprime una lista de las notas numerada y se guarda la lista en otra lista
	lista_ver = list(lista_notas())
	mumero=""
	nombre=""
	# Si el numero de nota no existe
	while not existe_nota(nombre):
		try:
			# Introduce la nota que quiere ver
			numero = int(input("\n 		Introduzca el numero de nota: "))

			# Si pone 0, volvemos al menu
			if numero == 0:
				return
			# Buscamos el nombre en la lista pero restamos uno pq esta empieza por 0
			nombre = lista_ver[numero-1]
		except:
			pass



	os.system('cls')

	# Abrimos la nota
	nota_ver = open('notas/'+nombre+'.txt', 'r')
	nota_ver.seek(0)
	# Traemos sus lineas
	ver_lineas = nota_ver.readlines()
	nota_ver.close()

	# Imprimimos el nombre de la nota
	print("\n 		=========={}==================================\n".format(nombre.upper()))
	
	# Imprimimos las lineas
	for i in ver_lineas:
		print(" 		"+i, end="")


	pregunta = ""
	while pregunta!="s" and pregunta!="n":
		pregunta = input(" 			Desea ver otra nota [s/n]: ").lower()
	if pregunta == "s":
		os.system('cls')
		ver_nota()
	else:
		return


# ----------------------------------------------------------------------------------------

def renombrar_nota():
	print()
	print(" 			0.- Volver al menu*")
	renombrar_lista = list(lista_notas())
	numero = ""
	nombre = ""
	while not existe_nota(nombre):
		try:
			numero = int(input("\n 		Introduzca el numero de nota: "))
			if numero == 0:
				return
			nombre=renombrar_lista[numero-1]
		except:
			pass

	os.system('cls')

	nuevoNombre = ""
	# Si el nuevo nombre existe o no ha puesto nada
	while existe_nota(nuevoNombre) or nuevoNombre=="":
		nuevoNombre = input("\n 		Introduce el nuevo nombre --> ")

	# Renombra el archivo
	os.rename("notas/"+nombre+".txt", "notas/"+nuevoNombre+".txt")

	archivo_datos = open("datos.txt", "r")
	lista = archivo_datos.readlines()
	archivo_datos.close()

	# Busca el indice en la lista donde pone el nombre antigua de la nota
	indice = lista.index(nombre+"\n")
	lista[indice] = nuevoNombre+"\n"
	
	# Escribe los nuevos datos
	archivo_datos = open("datos.txt", "w")
	archivo_datos.writelines(lista)
	archivo_datos.close()


# -----------------------------------------------------------------------------------------

def eliminar_nota():
	print()
	print(" 		--------LISTA NOTAS--------\n")
	print(" 			0.- Volver al menu*")
	eliminar_lista = list(lista_notas())
	numero = ""
	nombre = ""
	
	while not existe_nota(nombre):
		try:
			numero = int(input("\n 		Introduzca el numero de nota: "))
			if numero == 0:
				return
			nombre=eliminar_lista[numero-1]
		except:
			pass

	os.system('cls')
	print()
	respuesta=""
	while respuesta!="s" and respuesta!="n":
		respuesta = input(" 		Estas seguro de que quiere borrar '{}', [s/n] --> ".format(nombre)).lower()
	
	# Si decide borrar la nota
	if respuesta=="s":
		for i in range(3): # Esparemos 1.5 segundos
			os.system('cls')
			print()
			print(" 		Borrando"+"."*(i+1))
			time.sleep(0.5)
		# Elimina el archivo
		os.remove("notas/"+nombre+".txt")

		# Trae el archivo datos
		archivo_datos = open("datos.txt", "r")
		lista = archivo_datos.readlines()
		archivo_datos.close()

		# Busca el indice con el archivo borrado
		indice = lista.index(nombre+"\n")
		# Lo borra de la lista
		lista.pop(indice)

		# Inserta la nueva lista
		archivo_datos = open("datos.txt", 'w')
		archivo_datos.writelines(lista)
		archivo_datos.close()

		os.system('cls')
		print("\n 		Borrado con exito")
		return
	else:
		return False





#####################################EJECUCION############################################

ejecucion=True
while ejecucion:

	# Menu de seleccionar opcion
	os.system('cls')
	opcion = inicio()
	os.system('cls')






	# Opcion crear
	if opcion==1:
		os.system('cls')
		print(crear_nota())
		input("\n 		Presione intro para continuar...")


	# Opcion ver
	if opcion==2:
		os.system('cls')
		ver_nota()
		input("\n 		Presione intro para continuar...")


	# Opcion renombrar
	if opcion==3:
		os.system('cls')
		renombrar_nota()
		input("\n 		Presione intro para continuar...")


	# Opcion eliminar
	if opcion==4:
		os.system('cls')
		eliminar_nota()
		input("\n 		Presione intro para continuar...")


	# Opcion salir
	if opcion==5:
		for i in range(3): # Esperamos 1.5 segundos
			os.system('cls')
			print("\n\n 			Saliendo"+"."*(i+1))
			time.sleep(0.5)
		os.system('cls')
		# Cerramos el bucle
		ejecucion=False

