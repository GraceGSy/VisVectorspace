import json
import os
import itertools
import copy
import random
import pandas
from pandas.io.json._normalize import nested_to_record

result = []

folder_path = "./client/public/vega_examples"

accepted_marks = [	'area','bar',
					'line','point',
					'rect','tick']

accepted_channels = ['x','y','color','size','shape']

accepted_aggregates = ['average','count',
					   'distinct','max',
					   'mean','median',
					   'none','sum']

accepted_types = ['quantitative', 'nominal']

accepted_channel_details = ['type', 'aggregate', 'field']

# add all example specs to list
for file in os.listdir(folder_path):
	with open(folder_path + '/' + file, 'r') as fr:
		try:
			content = fr.read()
			specs = eval(content)

			mark = specs["mark"]
			encoding = specs["encoding"]
			channels = list(encoding.keys())
			
			if mark not in accepted_marks:
				continue

			all_channels_accepted = True
			for c in channels:
				if c not in accepted_channels:
					all_channels_accepted = False
				channel_details = list(specs["encoding"][c].keys())
				for d in channel_details:
					if d not in accepted_channel_details:
						all_channels_accepted = False
					elif d == 'type':
						if specs["encoding"][c][d] not in accepted_types:
							all_channels_accepted = False
					elif d == 'aggregates':
						if specs["encoding"][c][d] not in accepted_aggregates:
							all_channels_accepted = False

			if not all_channels_accepted:
				continue

			current_spec = specs["encoding"]
			current_spec["mark"] = mark
			current_spec["filename"] = file

			result.append(nested_to_record(current_spec, sep='.'))

		except Exception as e:
			continue

# create a dataframe of specs
df = pandas.DataFrame(result)

df = df.fillna('none')

columns = list(df)

accepted_columns = ['x.field','x.type','x.aggregate','x.channel',
					'x.bin','x.maxbins','x.scale','y.field',
					'y.type','y.aggregate','y.channel','y.bin',
					'y.maxbins','y.scale','row.field','row.type',
					'row.aggregate','row.channel','row.bin','row.maxbins',
					'row.scale','column.field','column.type','column.aggregate',
					'column.channel','column.bin','column.maxbins','column.scale',
					'color.field','color.type','color.aggregate','color.channel',
					'color.bin','color.maxbins','color.scale','size.field',
					'size.type','size.aggregate','size.channel','size.bin',
					'size.maxbins','size.scale','shape.field','shape.type',
					'shape.aggregate','shape.channel','shape.bin','shape.maxbins',
					'shape.scale','text.field','text.type','text.aggregate',
					'text.channel','text.bin','text.maxbins','text.scale', 'mark']

# drop columns that are not in the range of our study
for col in columns:
	if col not in accepted_columns:
		df = df.drop(columns=[col])
	if 'none' in col:
		df = df.drop(columns=[col])

new_columns = list(df)

for new_col in new_columns:
	if new_col == 'filename': continue

	col_values = list(df[new_col].unique())

	if 'field' in new_col:
		col_labels = {}
		for v in col_values:
			col_labels[v] = 0 if v == 'none' else 1
		df[new_col] = df[new_col].map(col_labels)
	else:
		df = pandas.get_dummies(df, columns=[new_col], prefix=new_col)

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

	# allCombinations = list(itertools.product(*myArgs))

	# combinations = []

	# # Do not repeat variables
	# for c in allCombinations:
	# 	length = len(c)
	# 	uniqueLength = len(set(c))

	# 	if length == uniqueLength:
	# 		combinations.append(c)

	# specsWithFields = []

	# for c in combinations:
	# 	newSpec = copy.deepcopy(spec)
	# 	for i in range(len(c)):
	# 		newSpec[myFields[i]+'_'+c[i]] = 1

	# 	for vc in validChannels:
	# 		newSpec.pop(vc+'.field', None)

	# 	specsWithFields.append(newSpec)

	return [newSpec]

vegaSpecs = df.to_dict('records')

# The following is only to be used with the cars dataset
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

print(list(df))

# do not un-comment the following unless you wish to rewrite the specs file
df.to_csv('./client/public/specs_one_hot_encoding_1.csv')
