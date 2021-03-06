from flask import Flask, send_from_directory, request
from classifier import Modeler
import random
import json
import pandas as pd
from pandas.io.json._normalize import nested_to_record
import itertools
import copy

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
	return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
	return send_from_directory('client/public', path)

# The following route is used for testing
@app.route("/rand/<val>")
def hello(val):
	print(val)
	return str(val)

# The following route is used for testing
@app.route("/read", methods=['POST'])
def readFile():
	print('data', request.data)
	return

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

	allCombinations = list(itertools.product(*myArgs))

	combinations = []

	# Do not repeat variables
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

		for vc in validChannels:
			newSpec.pop(vc+'.field', None)

		specsWithFields.append(newSpec)

	return specsWithFields

# Create specs for user dataset
@app.route("/recombine", methods=['POST'])
def recombine():
	data = json.loads(request.data)

	vegaSpecs = data["vegaSpecs"]
	types = data["types"]

	print(types)

	attrByType = {"string": [], "number": []}

	for attr in types.keys():
		attrByType[types[attr]].append(attr)

	specsWithFields = []

	for spec in vegaSpecs:
		specsWithFields = specsWithFields + getOptions(spec, attrByType)

	df = pd.DataFrame(specsWithFields)
	df = df.fillna(0)

	print(df)

	return json.dumps(df.to_dict('records'))


def flatten_one_hot_encoding(training, testing):
	result = []

	for specs in training:
		current_spec = specs
		result.append(nested_to_record(current_spec, sep='.'))

	df = pd.DataFrame(result)

	df = df.fillna(0)

	new_columns = list(df)

	for new_col in new_columns:
		col_values = list(df[new_col].unique())

		if 'field' in new_col:
			df = pd.get_dummies(df, columns=[new_col], prefix=new_col)
		elif 'label' in new_col:
			continue
		elif 'mark' in new_col:
			continue
		else:
			df = pd.get_dummies(df, columns=[new_col], prefix=new_col)

	columns = list(df)

	accepted_columns = list(pd.read_csv('./client/public/manual_specs_one_hot_encoding_3.csv'))

	for col in columns:
		if 'label' in col:
			continue
		elif col not in accepted_columns:
			df = df.drop(columns=[col])

	for ac in accepted_columns:
		if ac not in columns:
			df[ac] = 0

	return df.to_dict('records')

def getPreferred(predictions, testing):
	result = []
	for i in range(len(predictions)):
		if predictions[i] == 1:
			result.append(testing[i])

	return result

# Call the classifier
@app.route("/classifier", methods=['POST'])
def classify():
	print("call ok...")
	dataset = json.loads(request.data)

	print("running...")

	testingData = dataset['testing']
	trainingData = flatten_one_hot_encoding(dataset['training'], testingData)

	mainCol = 'index'
	targetCol = 'label'

	outobj = {}
	m = Modeler()
	m.read_data(trainingData, testingData)
	dfTraining, colDataTrain = m.pre_processdata(m.trainingData, mainCol)
	dfTesting, colDataTest = m.pre_processdata(m.testingData, mainCol)

	X_train, y_train = m.data_label_split(dfTraining, targetCol)
	X_test, y_test = m.data_label_split(dfTesting, targetCol)

	accTrain, accTest, feat_arr_wt, metric, predTest = m.build_model_classif(X_train, X_test, y_train, y_test)
	outobj['model_name'] = 'Classifier'
	outobj['acc_train'] = str(accTrain)
	outobj['acc_test'] = str(accTest)
	# outobj['col_names'] = str(','.join(colData))
	outobj['feature_wts'] = feat_arr_wt

	# print(accTrain, accTest, feat_arr_wt, metric)

	print(predTest, len(getPreferred(predTest, testingData)))

	result = json.dumps({"pred": predTest.tolist(), "feature_wts": feat_arr_wt})
	return result

if __name__ == "__main__":
	app.run(debug=True)
