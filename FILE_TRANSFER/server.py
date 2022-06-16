"""
	PENDIENTE

	Notificar las salidas del sevidor
	Intercambio de archivos
"""


import socket, os, select, re, pickle

class Server():
	def __init__(self):
		# Nombre del host
		self.host = socket.gethostbyname(socket.gethostname())
		# Puerto del servido
		self.port = 6100
		# Objeto servidor
		self.server_socket = self.create()
		# Lista de sockets por objeto
		self.socket_list = [self.server_socket]
		# Dicionario usuarios por objeto, con [username] como valor
		self.users_list = {}
		# Alamacena los print para que no se pierdan al limpiar la pantalla
		self.log = []

		if not os.path.exists('ARCHIVOS_SERVIDOR/'):
			os.system('md ARCHIVOS_SERVIDOR')
		if not os.path.exists('lista_usuarios.txt'):
			os.system('copy nul lista_usuarios.txt')




	def create(self):
		"""
			Crea el objeto del servidor, lo asigna a la ip  y puerto
			- permite 5 conexion simultaneas
		"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		except socket.error as err:
			pritn('Error creating the host:\n' + err)
		s.bind((self.host, self.port))
		s.listen(10)


		return s


	def accept_sockets(self, server_socket):
		"""
			Acepta peticiones de acceso al servidor
		"""
		clientsocket, address = server_socket.accept()

		return clientsocket, address

	def make_header(self, data):
		"""
			Se encarga de hacer el header de un msg
		"""
	
		len_data = len(data)
		header = '{:08}'.format(len_data)

		return header


	def send_data(self, client, data, archivo = False):

		"""
			Envia mensages al cliente seleccionado

			PARAMETROS
				- Cliente / destinatario
				- Mensage
				- Header del mensage
						Si no se pasa ningun header, la funcion lo hace
		"""
		header = self.make_header(data)
		try:
			if archivo == False:
				client.send(bytes(header + data, 'utf-8'))
			else:
				client.send(bytes(header, 'utf-8') + data)
		except ConnectionResetError:
			return False


		return True

		
	def recive_data(self, client, archivo = False):
		"""
			Recive informacion del cliente seleccionado, si vamos a recivir un header el tamaño
			del buffer se ajusta a 8

			PARAMETROS
				- Cliente del que recivir los datos
				- Tamaño del buffer (default: 1024)


			RETURN
				Retorna el mensage
		"""
		try:
			msg_header = client.recv(8).decode('utf-8')
			chunk = int(msg_header.strip())
			if chunk == '':
				return False
			data = b""
			while chunk > 0:
				if chunk > 1024:
					msg = client.recv(1024)
					data += msg
					chunk -= len(msg)
				else:
					msg = client.recv(chunk)
					data += msg
					chunk -= len(msg) 
		except:	
			return False

		if archivo == False:
			return data.decode('utf-8')
		else:
			return data


	def print_interface(self):
		os.system('cls')
		esq_sup_izq = '\u2554'
		arm_sup = '\u2566'
		esq_sup_dech = '\u2557'
		esq_centro_izq ='\u2560'
		arm_centro = '\u256c'
		esq_centro_dech = '\u2563'
		esq_inf_izq = '\u255A'
		arm_inf = '\u2569'
		esq_inf_dech = '\u255D'
		vert = '\u2551'
		horiz = '\u2550'



		print(f'''\n\t{esq_sup_izq + '-'*28 + arm_sup + '-'*28 + arm_sup + '-'*28 + esq_sup_dech}'''.replace('-', horiz))
		print(f'''\t|{'Servidor iniciado':^28}|{f"IP: {s.host:>20}":^28}|{f"PORT: {s.port:>18}":^28}|'''.replace('|', vert))
		print(f'''\t{esq_centro_izq + '-'*28 + arm_centro + '-'*28 + arm_centro + '-'*28 + esq_centro_dech}'''.replace('-', horiz))
		print(f'''\t|{f'Usuarios en linea{len(s.users_list):>5}':^28}|{f'Archivos disponibles{len(os.listdir("ARCHIVOS_SERVIDOR/")):4}':^28}|{'':28}|'''.replace('|', vert))
		print(f'''\t{esq_inf_izq + '-'*28 + arm_inf + '-'*28 + arm_inf + '-'*28 + esq_inf_dech}'''.replace('-', horiz))

		print("\n\tLOG:\n\t" + '\u2501'*88 + '\n')
		for i in self.log:
			print(i)


	def send_file(self, cliente, nombre):
		if os.path.exists('ARCHIVOS_SERVIDOR/'+ nombre):
			datos = b''
			with open('ARCHIVOS_SERVIDOR/' + nombre, 'rb') as file:
				datos += file.read()

			self.send_data(cliente, datos, archivo=True)
			return True
		else:
			self.send_data(cliente, '')
			return False

	def upload_file(self, cliente, nombre):
		nombre = nombre.replace('subir ', '')
		try:
			data = self.recive_data(cliente, archivo=True)
		except OSError:
			return
		with open('ARCHIVOS_SERVIDOR/' + nombre, 'wb') as file:
			file.write(data)
		self.send_data(cliente, 'Completada!')
		self.print_log(f'\t[$] El usuario: {self.users_list[cliente]}, ha subido el archivo: {nombre}')
		


	def print_log(self, text):
		print(text)
		self.log.append(text)



##################################################
s = Server()


while True:
	s.print_interface()
	with open('lista_archivos.txt', 'w') as file:
		cont = 0
		lista_archivos = []
		for i in os.listdir('ARCHIVOS_SERVIDOR/'):
			cont += 1
			if i not in lista_archivos:
				lista_archivos.append(str(cont)+','+i+'\n')
		file.writelines(lista_archivos)

	with open('lista_usuarios.txt', 'w') as file:
		for user in s.users_list.values():
			file.write(user+'\n')
	# El select permite identificar las solicitudes entrantes al servidor y solo para una lista con los sockets que hacen una peticion
	r_socket, _, excep_socket = select.select(s.socket_list, [], s.socket_list)
	# Lista de sockets conectados al servidor + el servidor
	# Notificacion es el objeto que esta enviando una datos al servidor
	for notification in r_socket:
		# Cada iteracion con el servidor
		if notification == s.server_socket:
			clientsocket, address = s.accept_sockets(s.server_socket)
			s.send_data(clientsocket, pickle.dumps(list(s.users_list.values())), archivo=True)
			try:
				username = s.recive_data(clientsocket)
				if username == False:
					clientsocket.close()
					continue
			except ConnectionResetError:
				clientsocket.close()
				continue
			s.print_log(f"\t[+] Conexion con {address[0]}, Usuario: {username}")
			s.socket_list.append(clientsocket)
			s.users_list[clientsocket] = username

			bienvenida = f"Bienvenido {username}"
			s.send_data(clientsocket, bienvenida)
			serial_files_list = pickle.dumps(lista_archivos)
			s.send_data(clientsocket, serial_files_list, archivo=True)

		else:
			peticion = s.recive_data(notification)
			if not peticion:
				s.print_log(f'\t[-] Conexion cerrada con {s.users_list[notification]}')
				s.socket_list.remove(notification)
				del s.users_list[notification]
				continue

			if re.match("descargar", peticion):
				nombre_archivo = peticion.replace("descargar", '').strip()
				
				if s.send_file(notification, nombre_archivo):
					s.print_log(f'\t[$] Enviado: {nombre_archivo} a {s.users_list[notification]}')

			elif re.match('subir', peticion):
				nombre_archivo = peticion.replace('subir ', '').strip()
				s.upload_file(notification, peticion)







