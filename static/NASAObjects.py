# contains objects that can deserialize objects from NASA's json api
import json

class JSONDeserializer:
	def deserialize(self, json):
		raise NotImplementedError()

class JSONSerializable:
	def serialize(self):
		raise NotImplementedError()

class NASAObject(JSONDeserializer, JSONSerializable):
	def __init__(self, Id=None, name=None):
		self.Id = Id
		self.name = name

class MeteorOrbitalData(NASAObject):
	def __init__(self, Id=None, name=None, json=None):
		NASAObject.__init__(self, Id, name)
		if json != None:
			self.deserialize(json)

	def init_variables(self, Id=None, orbit_determination_date=None, orbit_uncertainty=None, minimum_orbit_intersection=None, jupiter_tisserand_invariant=None, epoch_osculation=None,
					eccentricity=None,semi_major_axis=None, inclination=None, ascending_node_longitude=None,orbital_period=None,perihelion_distance=None,
					perihelion_argument=None, aphelion_distance=None,perihelion_time=None, mean_anomaly=None, mean_motion=None,equinox=None):
		self.Id, self.orbit_determination_date, self.orbit_uncertainty= Id, orbit_determination_date, orbit_uncertainty
		self.minimum_orbit_intersection, self.jupiter_tisserand_invariant, self.epoch_osculation = minimum_orbit_intersection, jupiter_tisserand_invariant, epoch_osculation
		self.eccentricity, self.semi_major_axis, self.inclination, self.ascending_node_longitude, self.orbital_period, self.perihelion_distance = eccentricity, semi_major_axis, inclination, ascending_node_longitude, orbital_period, perihelion_distance
		self.perihelion_argument, self.aphelion_distance, self.perihelion_time, self.mean_anomaly, self.mean_motion, self.equinox = perihelion_argument,aphelion_distance, perihelion_time, mean_anomaly, mean_motion, equinox

	def deserialize(self, json):
		self.init_variables(json['orbit_id'], json['orbit_determination_date'], json['orbit_uncertainty'], json['minimum_orbit_intersection'], json['jupiter_tisserand_invariant'],
							json['epoch_osculation'], json['eccentricity'], json['semi_major_axis'], json['inclination'], json['ascending_node_longitude'], json['orbital_period'],
							json['perihelion_distance'], json['perihelion_argument'], json['aphelion_distance'], json['perihelion_time'], json['mean_anomaly'], json['equinox'])

	def serialize(self):
		serializeable_fields = ['Id', 'orbit_determination_date', 'orbit_uncertainty', 'minimum_orbit_intersection', 'jupiter_tisserand_invariant', 'epoch_osculation',
								'eccentricity', 'semi_major_axis', 'inclination', 'ascending_node_longitude', 'orbital_period', 'perihelion_distance',
								'perihelion_argument', 'aphelion_distance', 'perihelion_time', 'mean_anomaly', 'mean_motion', 'equinox']
		serialized = {}
		for field in serializeable_fields:
			serialized[field] = getattr(self, field)
		return serialized

	def __str__(self):
		fields = ['Id', 'eccentricity', 'semi_major_axis', 'inclination', 'ascending_node_longitude', 'orbital_period', 'perihelion_distance', 'aphelion_distance']
		string = 'Orbital Data: ' + '['
		for field in fields:
			string += field + ':' + str(getattr(self, field)) + ','
		return string + ']'

class NasaMeteor(NASAObject):
	def __init__(self, Id=None, name=None, json=None):
		NASAObject.__init__(self, Id, name)
		self.init_variables()
		if json != None:
			self.deserialize(json)

	def init_variables(self, absolute_magnitude_h=None, estimated_diameter=None, hazardous=None, relative_velocity=None, orbiting_body=None, miss_distance=None, orbital_data=None):
		self.absolute_magnitude_h, self.estimated_diameter, self.hazardous, self.relative_velocity,self.orbiting_body, self.miss_distance = absolute_magnitude_h, estimated_diameter, hazardous, relative_velocity, orbiting_body, miss_distance
		self.orbital_data = orbital_data

	def deserialize(self, json, units='imperial'):
		unit_measurements = ['meters', 'kilometers_per_hour', 'kilometers'] if units != 'imperial' else ['feet', 'miles_per_hour', 'miles']
		approach_data = json['close_approach_data'][0]
		self.init_variables(json['absolute_magnitude_h'], {'amount':(json['estimated_diameter'][unit_measurements[0]]['estimated_diameter_min'] + json['estimated_diameter'][unit_measurements[0]]['estimated_diameter_max']) / 2, 'unit': unit_measurements[0]},
							json['is_potentially_hazardous_asteroid'], {'amount':approach_data['relative_velocity'][unit_measurements[1]], 'unit': unit_measurements[1]},
							approach_data['orbiting_body'], {'amount': approach_data['miss_distance'][unit_measurements[2]], 'unit': unit_measurements[2]})
		if 'orbital_data' in json:
			self.orbital_data = MeteorOrbitalData(json=json['orbital_data'])

	def serialize(self):
		serializeable_fields = ['Id', 'absolute_magnitude_h', 'estimated_diameter', 'hazardous', 'relative_velocity', 'orbiting_body', 'miss_distance', 'orbital_data']
		serialized = {}
		for field in serializeable_fields:
			attr = getattr(self, field)
			if attr != None and field == 'orbital_data':
				serialized[field] = attr.serialize()
			else:
				serialized[field] = attr
		return serialized

	def __str__(self):
		return 'Meteor [%s, %s, %s, %s, %s, %s, %s, %s]' % (self.Id, self.name, self.absolute_magnitude_h, self.estimated_diameter, self.hazardous, self.relative_velocity,self.orbiting_body, self.miss_distance)
		