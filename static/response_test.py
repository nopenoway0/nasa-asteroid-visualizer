from NASAObjects import NasaMeteor
import json

def get_test_meteors():
	meteors = []
	with open('static/example_response.json', 'r') as f:
		response = json.load(f)
		for meteor in response['near_earth_objects']:
			try:
				meteor = NasaMeteor(json=meteor)
				print(meteor)
				meteors.append(meteor)
			except:
				pass
	return meteors
