import socket, os, time, re, pickle
from datetime import *



class Client():

	def __init__(self):
		self.host = '192.168.1.60'
		self.port = 5200
		if not os.path.exists('client_saves.txt'):
			os.system('echo.>client_saves.txt')
		with open('client_saves.txt', 'rb') as file: 
			self.ruta_descargas = file.read().decode('utf-8')

		if not os.path.exists(self.ruta_descargas):
			while True:
				print('***OJO, la ruta de descargas no ha sido encontrada, cambiala para evitar errores')
				ruta_nueva = input('\tNueva ruta: ')
				if os.path.exists(ruta_nueva):
					with open('client_saves.txt', 'wb') as file:
						file.write(ruta_nueva.encode('utf-8'))
					self.ruta_descargas = ruta_nueva
					break
				else:
					print('\tNueva no encontrada')
		recon = input("\tReconectar al ultimo servidor? [s/n]: ").lower()
		if recon == 'n':
			self.conectar()
		else:
			if not os.path.exists('client_last.txt'):
				with open('client_last.txt', 'w'):
					pass
			with open('client_last.txt', 'r') as file:
				datos = file.read()
				if len(datos) > 1:
					self.conectar(datos_acceso = datos)
				else:
					self.conectar()

		self.ruta_descargas += '\\'
		self.chunk_length = 10000
		self.lista_usuarios = ()



	def conectar(self, datos_acceso = ""):
		"""
			Conecta con el servido,

			Pregunta la ip del servido, el puerto esta predeterminado
		"""
		ip_flag = False
		while not ip_flag:
			os.system('cls')
			if datos_acceso == "":
				datos_acceso = input(f'\n\tIntroduca la ip de servidor y el puerto, ejm: 192.168.1.1 , 8000: ')
			
			ip, port = datos_acceso.split(',')
			self.host = ip.strip()
			self.port = int(port.strip())
			os.system('cls')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				print()
				print('\tConectando...')
				s.connect((self.host, self.port))
				os.system('cls')
				print()
				input('\n\tConexion realizada con exito, Enter para entar...')
				# s.setblocking(False)
				ip_flag = True
				with open('client_last.txt', 'w') as file:
					file.write(datos_acceso)
			except socket.gaierror:
				input('***Ip del servidor no encontrada...***')
			except TimeoutError:
				input('***Ip del servidor no encontrada, tiempo limite superado...***')
			except ConnectionRefusedError:
				input('***El servidor denego el acceso...')

			datos_acceso = ''
			

		os.system('cls')


		self.server = s
		return s

	def ask_username(self):

		os.system('cls')
		print()
		intentos = 3
		self.lista_usuarios = pickle.loads(self.recive_data(archivo=True))
		os.system('cls')

		while True:
			nombre = input("\tNombre de ususario: ")
			if  4 < len(nombre) < 20:
				if nombre not in self.lista_usuarios:
					return nombre
				else:
					print('\t***Nombre ocupado***')
			else:
				print('\t***Nombre no valido***')
				nombre = ''
				intentos -= 1
			if intentos == 0:
				from random import randint
				num = ''
				for i in range(6):
					num += str(randint(1, 10))
				input()
				nombre = 'Invitado'+num
				return nombre
		print('fuera del bucle')

	def progress_bar(self, current, total, progreso):
		os.system('cls')

		porcentage = (len(current)/total)*100
		print()
		print("\tDescargando archivo")
		resto = int(porcentage%4)
		if resto == 0:
			sign = '\u2588'
			progreso = sign*int((porcentage/4))
			sign = ''
		elif resto == 1:
			sign = '\u2591'
		elif resto == 2:
			sign = '\u2592'
		elif resto == 3:
			sign = '\u2593'
		print(f"\t|{f'{progreso+sign}':<25}|  {int(porcentage)}% {f'( {len(current):>10,} / {total:>10,} ) bytes':>40}")
		print()
		return progreso

	def recive_data(self, archivo = False):
		try:
			msg_header = self.server.recv(8).decode('utf-8')
			bytes_totales = int(msg_header.strip())
		except ConnectionResetError:
			print('El servidor se ha cerrado')
		chunk = bytes_totales
		if chunk == 0:
			print("\tEl servidor no encontro la peticion")
			return False
		data = b""
		progreso = ''
		try:
			while chunk > 0:
				if chunk > self.chunk_length:
					msg = self.server.recv(self.chunk_length)
					data += msg
					chunk -= len(msg)
					if archivo:
						progreso = self.progress_bar(data, bytes_totales, progreso)
					
				else:
					msg = self.server.recv(chunk)
					data += msg
					chunk -= len(msg)  
					if archivo:
						progreso = self.progress_bar(data, bytes_totales, progreso)
		except KeyboardInterrupt:
			os.system('cls')
			print()
			print("\t***Descarga cancelada por el usuario")
			return False


		if archivo == False:
			return data.decode('utf-8')
		else:
			return data

	def make_header(self, msg):
		len_msg = len(msg)
		header = "{:08}".format(len_msg)

		return header

	def send_data(self, msg, archivo = False):
		
		header = self.make_header(msg)
		if archivo == False:
			self.server.send(bytes(header + msg, 'utf-8'))
		else:
			self.server.send(bytes(header, 'utf-8') + msg)

		return True

	def descargar_archivo_del_server(self, archivo):
		print("\t$ Solicitando archivo: " + archivo)
		self.send_data("descargar" + archivo)
		nombre_archivo = 'descarga_' + archivo
		data = self.recive_data(archivo=True)
		if not data:
			return
		print("\t$ Recivido: " + archivo )
		with open(self.ruta_descargas + nombre_archivo, 'wb') as file:
			file.write(data)
		print('\t$ Guardado en ' + self.ruta_descargas)

	def subir_archivo_al_servidor(self, archivo):
		ruta = archivo.replace('subir ', '')
		if os.path.exists(ruta) and os.path.isfile(ruta):
			nombre = os.path.basename(archivo)
			self.send_data('subir ' + nombre)
			data = b''
			with open(ruta, 'rb') as file:
				data += file.read()
			self.send_data(data, archivo=True)
			estado = self.recive_data()
			print('\tEstado de la subida: ' + estado)
			return estado
		else:
			print('\tLa ruta especificada no existe :(')
			return False


	def cambiar_ruta_descargas(self, ruta):
		nueva_ruta = ruta.replace('ruta =', '').strip()
		if os.path.exists(nueva_ruta):
			self.ruta_descargas = nueva_ruta
			return nueva_ruta
		else:
			print('\t***La ruta no existe***')
			return False

		






###########################
os.system('cls')
# Conexion con el servidor
cliente = Client()
# Introducion y envio de usuario al servidor
username = cliente.ask_username()
cliente.send_data(username)

os.system('cls')
bienvenida = cliente.recive_data()
json_archivos = pickle.loads((cliente.recive_data(archivo=True)))
lista_archivos = list()
for i in json_archivos:
	i = i.strip()
	elemento = i.split(',')
	lista_archivos.append(elemento)
os.system('cls')
print("\n\t" + bienvenida)

while True:
	ask_option = input('\t> ')

	if ask_option == 'exit':
		cliente.server.close()
		print('\t Adios...')
		break
	
	elif re.match('descargar', ask_option):
		nombre_archivo = ask_option.replace('descargar', '').strip()
		for i in lista_archivos:
			if i[0] == nombre_archivo:
				nombre_archivo = i[1]
		cliente.descargar_archivo_del_server(nombre_archivo)

	elif re.match('subir', ask_option):
		cliente.subir_archivo_al_servidor(ask_option)


	elif re.match('ruta', ask_option):
		if re.match('ruta *=', ask_option):
			nueva_ruta = cliente.cambiar_ruta_descargas(ask_option)
			if nueva_ruta: print("\tRuta cambiada a " + nueva_ruta)
		else:
			print('\tRuta de descarga actual: ' + cliente.ruta_descargas)

	elif ask_option == 'prueba':
		cliente.send_data('prueba')
		msg = cliente.recive_data()
		print(msg + str(len(msg)))

	elif re.match('buffer', ask_option):
		if re.match('buffer *=', ask_option):
			cliente.chunk_length = int(re.sub('buffer *=', '', ask_option).strip())
		print('\tEl tamaño del buffer actual es ' + str(cliente.chunk_length))

	elif re.match('lista_archivos', ask_option):
		print()
		for i in lista_archivos:
			print('\t'+ i[0] + ' - ' + i[1])

	elif re.match('lista_usuarios', ask_option):
		for i in self.lista_usuarios:
			print('\n\t - ' + i)

