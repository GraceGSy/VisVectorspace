import copy
import itertools
import pandas

accepted_marks = ['mark_area','mark_bar','mark_boxplot',
				  'mark_circle','mark_line','mark_point',
				  'mark_rect','mark_rule','mark_tick']

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

# Add fields
accepted_fields = []

for c in accepted_channels:
	accepted_fields.append(c + '.field')

permutations1 = list(itertools.combinations(accepted_fields, 1))
permutations2 = list(itertools.combinations(accepted_fields, 2))
permutations3 = list(itertools.combinations(accepted_fields, 3))

all_permutations = permutations1 + permutations2 + permutations3

fields_template = {}
for f in accepted_fields:
	fields_template[f] = 0

new_data = []

for row in data:
	for p in all_permutations:
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
		if c == 'size':
			all_types.append('size.type_quantitative')
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

data = new_data

# for row in data:
# 	if row['x.field'] == 1 and row['y.field'] == 1 and row["size.type_nominal"] == 1:
# 		print(row)

df = pandas.DataFrame(data)

df.index.names = ['index']

df['label'] = 0

# do not un-comment the following unless you wish to rewrite the specs file
df.to_csv('./client/public/manual_specs_one_hot_encoding.csv')
