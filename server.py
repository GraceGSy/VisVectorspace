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

def flatten_one_hot_encoding(training, testing):
	result = []

	for specs in training:
		current_spec = specs
		result.append(nested_to_record(current_spec, sep='.'))

	df = pd.DataFrame(result)

	df = df.fillna('none')

	new_columns = list(df)

	for new_col in new_columns:
		col_values = list(df[new_col].unique())

		if 'field' in new_col:
			col_labels = {}
			for v in col_values:
				col_labels[v] = 0 if v == 'none' else 1
			df[new_col] = df[new_col].map(col_labels)
		elif 'label' in new_col:
			continue
		elif 'mark' in new_col:
			continue
		else:
			df = pd.get_dummies(df, columns=[new_col], prefix=new_col)

	columns = list(df)

	accepted_columns = list(pd.read_csv('./client/public/manual_specs_one_hot_encoding.csv'))

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

	# print(y_train, y_test)

	accTrain, accTest, feat_arr_wt, metric, predTest = m.build_model_classif(X_train, X_test, y_train, y_test)
	outobj['model_name'] = 'Classifier'
	outobj['acc_train'] = str(accTrain)
	outobj['acc_test'] = str(accTest)
	# outobj['col_names'] = str(','.join(colData))
	outobj['feature_wts'] = feat_arr_wt
	# print(json.dumps(getPreferred(predTest, testingData)))

	# print(getPreferred(predTest, testingData))

	result = json.dumps(predTest.tolist())
	return result

if __name__ == "__main__":
	app.run(debug=True)
