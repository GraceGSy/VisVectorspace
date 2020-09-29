import copy
import itertools
import pandas

accepted_marks = ['mark_area','mark_bar',
				  'mark_line','mark_point',
				  'mark_rect','mark_tick']

accepted_channels = ['x','y','color','size','shape']

accepted_aggregates = ['aggregate_average','aggregate_count',
					   'aggregate_distinct','aggregate_max',
					   'aggregate_mean','aggregate_median',
					   'aggregate_none','aggregate_sum']

accepted_types = ['type_quantitative', 'type_nominal']

data = []

# First add all possible marks
marks_template = {}
for m in accepted_marks:
	marks_template[m] = 0

for m in accepted_marks:
	new_row = copy.deepcopy(marks_template)
	new_row[m] = 1
	data.append(new_row)

# Add fields(channels)
accepted_fields = []

for c in accepted_channels:
	accepted_fields.append(c + '.field')

permutations1 = list(itertools.combinations(accepted_fields, 1))
permutations2 = list(itertools.combinations(accepted_fields, 2))
permutations3 = list(itertools.combinations(accepted_fields, 3))

possible_permutations = permutations1 + permutations2 + permutations3

all_permutations = []

for p in possible_permutations:
	if len(p) == 1:
		if p[0] != "x.field" or p[0] != "y.field": continue
		else: all_permutations.append(p)
	if len(p) == 2:
		if (p[0] == "x.field" and p[1] == "y.field") or (p[1] == "x.field" and p[0] == "y.field"):
			all_permutations.append(p)
	if len(p) == 3:
		hasX = False
		hasY = False
		for i in p:
			if i == "x.field": hasX = True
			if i == "y.field": hasY = True
		if hasX and hasY:
			all_permutations.append(p)

fields_template = {}
for f in accepted_fields:
	fields_template[f] = 0

new_data = []

for row in data:
	for p in all_permutations:
		# The shape channel can only be used with the point mark
		if (not row["mark_point"] == 1) and ("shape.field" in p):
			continue

		# The size channel can only be used with the point mark
		if (not row["mark_point"] == 1) and ("size.field" in p):
			continue

		# point mark must have x and y channels
		if len(p) == 1 and row["mark_point"] == 1:
			continue

		# area mark must have x and y channels
		if len(p) == 1 and row["mark_area"] == 1:
			continue

		# line mark must have x and y channels
		if len(p) == 1 and row["mark_line"] == 1:
			continue

		new_permutation = copy.deepcopy(fields_template)

		for f in p:
			new_permutation[f] = 1

		new_row = copy.deepcopy(row)

		new_row.update(new_permutation)

		new_data.append(new_row)

data = new_data

# Add types
all_types = []

for c in accepted_channels:
	for t in accepted_types:
		# size channel can only be used with a quantitative variable
		if c == 'size':
			all_types.append('size.type_quantitative')
		# shape channel can only be used with a quantitative variable
		elif c == 'shape':
			all_types.append('shape.type_nominal')
		else:
			channel_type = c + '.' + t
			all_types.append(channel_type)

types_template = {}

for t in all_types:
	types_template[t] = 0

new_data = []

def get_type_permutations(fields):

	my_args = []
	for f in fields:
		channel = f.replace('.field', '')
		relevant = list(filter(lambda x: x.startswith(channel), all_types))
		my_args.append(relevant)

	all_possible = list(itertools.product(*my_args))

	type_permutations = []

	# only 1 nominal variable per set
	# either x or y channel must be in the set
	for p_set in all_possible:
		nominal_count = 0
		has_xy = False
		for f in p_set:
			if 'nominal' in f:
				nominal_count += 1
			if f.startswith('x') or f.startswith('y'):
				has_xy = True

		# Only one nominal variable allowed
		if nominal_count < 2 and has_xy:
			type_permutations.append(p_set)

	return type_permutations

for row in data:
	valid_fields = list(filter(lambda x: 'field' in x and row[x] == 1, list(row.keys())))
	
	type_permutations = get_type_permutations(valid_fields)

	for p in type_permutations:
		new_permutation = copy.deepcopy(types_template)

		for f in p:
			new_permutation[f] = 1

		new_row = copy.deepcopy(row)

		new_row.update(new_permutation)

		new_data.append(new_row)

# def getOptions(spec, attrByType):
# 	validChannels = ['x','y','color','size','shape']

# 	myArgs = []
# 	myFields = []

# 	for c in validChannels:
# 		if spec[c+'.field'] == 1:
# 			myFields.append(c+'.field')
# 			if (c+'.type_quantitative' in spec) and spec[c+'.type_quantitative'] == 1:
# 				myArgs.append(attrByType['number'])
# 			elif (c+'.type_nominal' in spec) and spec[c+'.type_nominal'] == 1:
# 				myArgs.append(attrByType['string'])

# 	allCombinations = list(itertools.product(*myArgs))

# 	combinations = []

# 	# Do not repeat variables
# 	for c in allCombinations:
# 		length = len(c)
# 		uniqueLength = len(set(c))

# 		if length == uniqueLength:
# 			combinations.append(c)

# 	specsWithFields = []

# 	for c in combinations:
# 		newSpec = copy.deepcopy(spec)
# 		for i in range(len(c)):
# 			newSpec[myFields[i]+'_'+c[i]] = 1

# 		for vc in validChannels:
# 			newSpec.pop(vc+'.field', None)

# 		specsWithFields.append(newSpec)

# 	return specsWithFields

def getOptions(spec, attrByType):
	validChannels = ['x','y','color','size','shape']

	myArgs = []
	myFields = []

	for c in validChannels:
		if spec[c+'.field'] == 1:
			myFields.append(c+'.field')
			if (c+'.type_quantitative' in spec) and spec[c+'.type_quantitative'] == 1:
				myArgs.append(attrByType['number'])
			elif (c+'.type_nominal' in spec) and spec[c+'.type_nominal'] == 1:
				myArgs.append(attrByType['string'])

	newSpec = copy.deepcopy(spec)

	for i in range(len(myFields)):
		field = myFields[i]
		args = myArgs[i]
		for a in args:
			newSpec[field+'_'+a] = 0

	return [newSpec]

vegaSpecs = new_data

# The following is only to be used with the cars dataset
# types = {'name': 'number', 'mfr': 'string', 'type': 'string', 'calories': 'number', 'protein': 'number', 'fat': 'number', 'sodium': 'number', 'fiber': 'number', 'carbo': 'number', 'sugars': 'number', 'potass': 'number', 'vitamins': 'number', 'shelf': 'number', 'weight': 'number', 'cups': 'number', 'rating': 'number'}
types = {'mfr': 'string', 'type': 'string', 'calories': 'number', 'protein': 'number', 'fat': 'number', 'sodium': 'number', 'carbo': 'number', 'sugars': 'number', 'vitamins': 'number', 'shelf': 'number'}

attrByType = {"string": [], "number": []}

for attr in types.keys():
	attrByType[types[attr]].append(attr)

specsWithFields = []

for spec in vegaSpecs:
	specsWithFields = specsWithFields + getOptions(spec, attrByType)

df = pandas.DataFrame(specsWithFields)
df = df.fillna(0)

df.index.names = ['index']

df['label'] = 0

# do not un-comment the following unless you wish to rewrite the specs file
df.to_csv('./client/public/manual_specs_one_hot_encoding_3.csv')
