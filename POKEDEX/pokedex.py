import requests

def get_pokemons(url='https://pokeapi.co/api/v2/pokemon-form', offset=0, limit=20):
	
	args = {'offset': offset, 'limit' : limit}
	respuesta = requests.get(url, params=args)


	if respuesta.status_code == 200:
		# Obtiene el json y lo pasa a diccionario
		payload=respuesta.json()

		# Busca en el diccionario la clave results y en caso de no existir debuelve una lista vacia
		lista_pokemon = payload.get('results', [])

		# Si la lista tiene algun elemento,
		if lista_pokemon:
			for pokemon in lista_pokemon:
				print(pokemon['name'])

		continuar = input('Deseas continuar [Y/N] = ').lower()
		if continuar == 'y':
			get_pokemons(offset=offset+20)



get_pokemons()