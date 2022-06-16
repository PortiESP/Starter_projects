from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class Navegador:
	def __init__(self, driver_path):
		self.driver_path = driver_path
		self.chrome_options = Options()
		self.chrome_options.add_argument("--kiosk")
		self.chrome_options.add_experimental_option("useAutomationExtension", False)
		self.chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
		self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.chrome_options)
		self.current_window_handler = None
		self.instruccion_index = 0
		self.instrucciones_viaje = []
		self.instrucciones_dict = {}
		self.xpaths = []
		self.xpaths_title = []
		self.cookie_accepted = False
		self.zoom_in_bt = None
		self.zoom_out_bt = None

		self.driver.get('https://www.google.es/maps')
		self.current_window_handler = self.driver.current_window_handle
		if not self.cookie_accepted:
			if self.__aceptar_privacidad(): self.cookie_accepted = True


	def direccion(self, origen, destino):
		origen = origen.replace(' ','+')
		destino = destino.replace(' ','+')
		url_map = 'https://www.google.es/maps/dir/'+origen+'/'+destino
		# self.driver.fullscreen_window()
		self.driver.get(url_map)

		self.current_window_handler = self.driver.current_window_handle
		

	def __aceptar_privacidad(self):
		wh = self.driver.current_window_handle
		WebDriverWait(self.driver, 20).until(lambda x: self.driver.find_element_by_tag_name('iframe'))
		caja_privacidad = self.driver.find_element_by_tag_name('iframe')
		self.driver.switch_to.frame(caja_privacidad)
		self.driver.find_element_by_id('introAgreeButton').click()
		self.driver.switch_to.window(wh)

	def __obtener_instrucciones(self):
		WebDriverWait(self.driver, 60).until(lambda x: self.driver.find_elements_by_class_name('directions-mode-group'))
		self.bloques_direcciones = self.driver.find_elements_by_class_name('directions-mode-group')
		for bloque in self.bloques_direcciones:
			lista = self.driver.find_elements_by_xpath(f'/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div/div/div[1]/div/div[2]/div[3]/div[1]/div[{len(self.instrucciones_dict)+2}]/div/div/div')		
			for x in range(len(lista)):
				self.xpaths.append(f'/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div/div/div[1]/div/div[2]/div[3]/div[1]/div[{len(self.instrucciones_dict)+2}]/div/div/div[{x+1}]')
				self.xpaths_title.append(self.driver.find_element_by_xpath(f'/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div/div/div[1]/div/div[2]/div[3]/div[1]/div[{len(self.instrucciones_dict)+2}]/div/div/div[{x+1}]/div/div[1]/div[2]'))
			self.instrucciones_dict[bloque] = self.xpaths_title

		self.zoom_in_bt = self.driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[22]/div[1]/div[2]/div[7]/div/div[1]/button/div')
		self.zoom_out_bt = self.driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[22]/div[1]/div[2]/div[7]/div/button/div')

	def __style(self, xpath, **kw):
		for key, value in kw.items():
			self.driver.execute_script(f'document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.{key}="{value}"')

	def iniciar_viaje(self):

		self.__obtener_instrucciones()
		self.instruccion_index = 0
		for bloque, instrucciones in self.instrucciones_dict.items():
			bloque.click()
			for i in instrucciones:
				self.instrucciones_viaje.append(i)
			time.sleep(0.3)
		self.__style(self.xpaths[0], background='cornflowerblue', color='white', borderRadius='10px')
		self.actual_point = self.instrucciones_viaje[0]
		self.actual_point.click()

		

	def siguiente_instruccion(self):
		self.__style(self.xpaths[self.instruccion_index], background='white', color='black')
		self.instruccion_index += 1
		self.__style(self.xpaths[self.instruccion_index], background='cornflowerblue', color='white', borderRadius='10px')
		self.actual_point =  self.instrucciones_viaje[self.instruccion_index]
		self.actual_point.click()
		self.scroll(100)

	def anterior_instruccion(self):
		self.__style(self.xpaths[self.instruccion_index], background='white', color='black')
		self.instruccion_index -= 1
		self.__style(self.xpaths[self.instruccion_index], background='cornflowerblue', color='white', borderRadius='10px')
		self.actual_point = self.instrucciones_viaje[self.instruccion_index]
		self.actual_point.click()
		self.scroll(-100)

	def zoom_in(self):
		self.zoom_in_bt.click()

	def zoom_out(self):
		self.zoom_out_bt.click()

	def scroll(self, value):
		self.driver.execute_script(f'document.evaluate("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollBy(0,{value})')

	def select_instrucciones(self):
		for i in self.instrucciones_viaje:
			print(i)
			i.click()
			time.sleep(2)

			
	def pruebas(self):
		print('Sleeping...')
		time.sleep(1)
		self.__style(self.xpaths[1], background='black')

	def goto_step(self, step):
		step.click()

	def mini_nav(self):
		while 1:
			q = input('--> ')
			if q == 'next': self.siguiente_instruccion()
			elif q == 'prev': self.anterior_instruccion()
			elif q == '+': self.zoom_in()
			elif q == '-': self.zoom_out()
			elif q == 's': self.scroll(50)

	def exit(self):
		self.driver.quit()


if __name__ == '__main__':
	nav = Navegador('C:/Program Files (x86)/chromedriver.exe')
	nav.direccion('Boadilla del monte', 'Aluche')
	time.sleep(3)
	nav.direccion('aluche', 'Moncloa')
	nav.iniciar_viaje()
	# nav.pruebas()
	# nav.select_instrucciones()
	nav.mini_nav()