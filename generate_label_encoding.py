import json
import os
import random
import pandas
from pandas.io.json._normalize import nested_to_record

result = []

folder_path = "./client/public/vega_examples"

accepted_marks = [	'area','bar','boxplot',
					'circle','errorband','errorbar',
					'line','point','rect',
					'rule','tick']

accepted_channels = [ 	'x','y','row','column',
						'color','size','shape']

# add all example specs to list
for file in os.listdir(folder_path):
	with open(folder_path + '/' + file, 'r') as fr:
		try:
			content = fr.read()
			specs = eval(content)

			mark = specs["mark"]
			channels = list(specs["encoding"].keys())
			
			if mark not in accepted_marks:
				continue

			all_channels_accepted = True
			for c in channels:
				if c not in accepted_channels:
					all_channels_accepted = False

			if not all_channels_accepted:
				continue

			current_spec = specs["encoding"]
			current_spec["mark"] = "mark_" + mark
			current_spec["filename"] = file

			result.append(nested_to_record(current_spec, sep='.'))

		except Exception as e:
			continue

# create a dataframe of specs
df = pandas.DataFrame(result)

df = df.fillna('none')

columns = list(df)

accepted_columns = ['filename','x.field','x.type','x.aggregate','x.channel',
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
					'text.channel','text.bin','text.maxbins','text.scale']

# drop columns that are not in the range of our study
for col in columns:
	if col not in accepted_columns:
		df = df.drop(columns=[col])

new_columns = list(df)

all_labels = {}

for new_col in new_columns:
	if new_col == 'filename': continue
	col_labels = {}

	col_values = list(df[new_col].unique())

	for v in col_values:
		if 'field' in new_col:
			col_labels[v] = 0 if v == 'none' else 1
		else:
			label = random.randint(0, 100)
			col_labels[v] = label

	all_labels[new_col] = col_labels

for new_col in new_columns:
	if new_col == 'filename': continue
	df[new_col] = df[new_col].map(all_labels[new_col])

df = df.set_index('filename')

# do not un-comment the following unless you wish to rewrite the label mappings
# current labels are saved under label_encoding_mapping.json

# df.to_csv('./client/public/specs_label_encoding.csv')
# with open('./label_encoding_mapping.json', 'w') as fw:
# 	json.dump(all_labels, fw)
