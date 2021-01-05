import sys
import os
import json
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import BallTree
import random

class knnModeler():
	def init(self):
		self.df = None
		pass

	def read_data(self, trainingData, testingData):
		self.trainingData = None
		self.testingData = None

		try:
			self.trainingData = pd.DataFrame(trainingData)
			print('training data ok...')
			self.testingData = pd.DataFrame(testingData)
			print('testing data ok...')
			df = pd.concat([self.trainingData, self.testingData]).reset_index(drop=True)
			self.df = df.fillna(0)
		except Exception as e:
			print('error reading dataframe ', e)
		return [self.df]

	def data_label_split(self, data, targetCol=''):
		y = data[targetCol]
		X = data.drop([targetCol], axis=1).to_numpy()

		return X, y

	def pre_processdata(self, data, mainCol=''):
		categorical = True
		try:
			data = data.drop([mainCol], axis=1)
		except Exception as e:
			pass
		data = data.apply(pd.to_numeric, errors='ignore')
		data = data.fillna(method='ffill')
		colData = data.columns.values
		if(categorical):
			data = self.one_hot_encode_category(data)
		else:
			data = data._get_numeric_data()
		return data, colData

	def one_hot_encode_category(self, X):
		X = pd.get_dummies(X)
		return X

	def build_model_knn(self, data):
		self.knn = BallTree(data, leaf_size=20)


