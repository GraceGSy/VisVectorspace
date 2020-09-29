import sys
import os
import json
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix, precision_score, recall_score
import random

class Modeler():
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
        except Exception as e:
            print('error reading dataframe ', e)
        return [self.trainingData, self.testingData]

    def data_label_split(self, data, targetCol=''):
        y = data[targetCol]
        X = data.drop([targetCol], axis=1)

        return X, y

    def train_test_split(self, data, targetCol=''):
        y = data[targetCol]
        X = data.drop([targetCol], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.22, random_state=15)
        # print ('train test shape ', X_train.shape, X_test.shape)
        return X_train, X_test, y_train, y_test

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

    def build_model_classif(self, train, test, targetTrain, targetTest):
        clf = RandomForestClassifier(max_depth=20,
                                     min_samples_split=4,
                                     min_samples_leaf=5,
                                     #  bootstrap=,
                                     #  criterion=space['criterion']
                                     criterion='gini',
                                     random_state=1
                                     )
        clf.fit(train, targetTrain)

        print('building classifier...')

        predTrain = clf.predict(train)
        predTest = clf.predict(test)

        # feature wt compute
        feat_wts = [round(x, 3) for x in clf.feature_importances_]
        feat_names = train.columns.values
        feat_dict = dict(zip(feat_names, feat_wts))
        feat_arr_wt = sorted(
            feat_dict.items(), key=lambda kv: kv[1], reverse=True)  # [:5]
        feat_arr_wt = [(str(x[0]), str(x[1])) for x in feat_arr_wt if abs(x[1]) > 0]

        metric = 'Acc'
        accTrain = accuracy_score(targetTrain, predTrain, normalize=True)
        accTest = accuracy_score(targetTest, predTest, normalize=True)

        print('accuracy...', accTrain, accTest)
        return accTrain, accTest, feat_arr_wt, metric, predTest


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# inpdir = sys.argv[1]
# baseMod = sys.argv[2]
# currentDirectory = os.getcwd()
# the path can also be an input as inpdir above
# path = currentDirectory + '/public/data/specs_binary.csv'
# change these col names as needed 
# path = './client/public/data/specs_binary.csv'
# mainCol = 'filename'
# targetCol = 'label'

# outobj = {}
# m = Modeler()
# m.read_data(path)
# df, colData = m.pre_processdata(m.df, mainCol)
# X_train, X_test, y_train, y_test = m.train_test_split(df, targetCol)

# accTrain, accTest, feat_arr_wt, metric = m.build_model_classif(X_train, X_test, y_train, y_test)
# outobj['model_name'] = 'Classifier'
# outobj['acc_train'] = str(accTrain)
# outobj['acc_test'] = str(accTest)
# outobj['col_names'] = str(','.join(colData))
# outobj['feature_wts'] = feat_arr_wt

# print(json.dumps(outobj, sort_keys=True))

