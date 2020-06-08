from flask import Flask, send_from_directory, request
from classifier import Modeler
import random
import json

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
	print (val)
	return str(15)

@app.route("/read", methods=['POST'])
def readFile():
	# filepath = request.args['param1'][5:]
	# print('data', request.data)
	# f = open('./file.csv', 'wb')
	# f.write(request.data)
	# f.close()
	# print(send_from_directory('/', filepath))
	# try:
	# 	with open('./file.csv') as f:
	# 		content = f.read()
	# 		print(content)
	# except Exception as e:
	# 	print(e)
	return

# Call the classifier
@app.route("/classifier", methods=['POST'])
def classify():
	dataset = json.loads(request.data)

	mainCol = 'filename'
	targetCol = 'label'

	outobj = {}
	m = Modeler()
	m.read_data(dataset)
	df, colData = m.pre_processdata(m.df, mainCol)
	X_train, X_test, y_train, y_test = m.train_test_split(df, targetCol)

	accTrain, accTest, feat_arr_wt, metric = m.build_model_classif(X_train, X_test, y_train, y_test)
	outobj['model_name'] = 'Classifier'
	outobj['acc_train'] = str(accTrain)
	outobj['acc_test'] = str(accTest)
	outobj['col_names'] = str(','.join(colData))
	outobj['feature_wts'] = feat_arr_wt

	print(type(json.dumps(outobj, sort_keys=True)))
	return (json.dumps(outobj, sort_keys=True))

if __name__ == "__main__":
	app.run(debug=True)
