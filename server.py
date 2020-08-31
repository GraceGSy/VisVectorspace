from flask import Flask, send_from_directory, request
from classifier import Modeler
import random
import json
import pandas as pd
from pandas.io.json._normalize import nested_to_record

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

def flatten(training, testing):
	allFlattened = []
	for t in training:
		allFlattened.append(nested_to_record(t, '.'))
	df = pd.DataFrame(allFlattened).fillna(0)

	allCols = list(df)

	for c in allCols:
		if ('label' in c): continue
		elif ('zero' in c): df = df.drop(columns=[c])
		else: df[c] = df[c].apply(lambda x: 1 if x != 0 else 0)
	
	testingCols = testing[0].keys()

	for tc in testingCols:
		if tc not in allCols:
			df[tc] = 0

	newAllCols = list(df)

	for nac in newAllCols:
		if nac not in testingCols:
			df = df.drop(columns=[nac])

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
	dataset = json.loads(request.data)

	testingData = dataset['testing']
	trainingData = flatten(dataset['training'], testingData)

	mainCol = 'filename'
	targetCol = 'label'

	outobj = {}
	m = Modeler()
	m.read_data(trainingData, testingData)
	dfTraining, colDataTrain = m.pre_processdata(m.trainingData, mainCol)
	dfTesting, colDataTest = m.pre_processdata(m.testingData, mainCol)

	X_train, y_train = m.data_label_split(dfTraining, targetCol)
	X_test, y_test = m.data_label_split(dfTesting, targetCol)

	# print(y_train, y_test)

	accTrain, accTest, feat_arr_wt, metric, predTest = m.build_model_classif(X_train, X_test, y_train, y_test)
	outobj['model_name'] = 'Classifier'
	outobj['acc_train'] = str(accTrain)
	outobj['acc_test'] = str(accTest)
	# outobj['col_names'] = str(','.join(colData))
	outobj['feature_wts'] = feat_arr_wt

	# print(getPreferred(predTest, testingData))
	return json.dumps(predTest)
	# return (json.dumps(outobj, sort_keys=True))

if __name__ == "__main__":
	app.run(debug=True)
