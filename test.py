import itertools
import copy

def getOptions(spec, attrByType):
	validChannels = ['x','y','color','size','shape']

	myArgs = []
	myFields = []

	for c in validChannels:
		if spec[c+'.field'] == 1:
			myFields.append(c+'.field')
			if spec[c+'.type_quantitative'] == 1:
				myArgs.append(attrByType['number'])
			elif spec[c+'.type_nominal'] == 1:
				myArgs.append(attrByType['string'])

	allCombinations = list(itertools.product(*myArgs))

	combinations = []

	for c in allCombinations:
		length = len(c)
		uniqueLength = len(set(c))

		if length == uniqueLength:
			combinations.append(c)

	specsWithFields = []

	for c in combinations:
		newSpec = copy.deepcopy(spec)
		for i in range(len(c)):
			newSpec[myFields[i]+'_'+c[i]] = 1
			

		specsWithFields.append(newSpec)

	return specsWithFields

testSpec = {"color.field": 0,
			"color.type_nominal": 0,
			"color.type_quantitative": 0,
			'label': 0,
			'mark_area': 1,
			'mark_bar': 0,
			'mark_circle': 0,
			'mark_line': 0,
			'mark_point': 0,
			'mark_rect': 0,
			'mark_tick': 0,
			'shape.field': 0,
			'shape.type_nominal': 0,
			'size.field': 0,
			'size.type_quantitative': 0,
			'x.field': 1,
			'x.type_nominal': 0,
			'x.type_quantitative': 1,
			'y.field': 1,
			'y.type_nominal': 0,
			'y.type_quantitative': 1}

attrByType = {'number': ['protein', 'sodium', 'sugar', 'fiber', 'carbo'],
			  'string': ['mfr', 'type']}

print(getOptions(testSpec, attrByType))