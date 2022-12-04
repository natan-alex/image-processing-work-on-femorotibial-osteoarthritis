from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cv2
import os
import time

start= time.time()
#carregamento e pre-processamento de dados para treinamento
cls_dir=os.listdir("train")
X=[]
y=[]
for cls in cls_dir:
    cls_img= os.listdir("train/"+cls)
    for image in cls_img:
        img=cv2.imread("train/"+cls+"/"+image, cv2.IMREAD_GRAYSCALE)
        img=cv2.resize(img, (150,200), cv2.INTER_AREA)
        feature=np.reshape(img, (img.shape[0]*img.shape[1]))
        X.append(feature)
        y.append(cls)

X=np.array(X).reshape(len(X), -1)
y=np.array(y)

#divisao de dados para treinamento e testes
x_train, x_test, y_train , y_test = train_test_split(X,y)

#parametros configurados para RadomizedSearchCV
#param_dist={ "n_estimators": [100,150,200],
                #'criterion': ['gini', 'entropy'],
                #'max_depth': range(2,20,1),
                #'min_samples_leaf': range(1,10,1),
                #'min_samples_split': range(1,10,1),
                #'max_features':['sqrt','log2']
#}

#instaciamento do medelo RandomForest
model = RandomForestClassifier(n_estimators=200, min_samples_split=6, min_samples_leaf=8, max_features= 'sqrt', max_depth=19, criterion= 'entropy')
#uso do RandomizedSearchCV para ver qual a melhor combinacao de parametros nas opcoes pra programadas no param_dist
#model_cv = RandomizedSearchCV(model, param_dist,cv=5)
#treinameto do modelo
model.fit(X,y)
#predicao dos testes
y_pred=model.predict(x_test)

#best score e paramters do RandomizedSearchCV
#print("Melhores parametros")
#print(model_cv.best_params_)
#print("Best score")
#print(model_cv.best_score_)

#Accuracy, Classification report e cinfusion matrix do Random Foreste
#print("Accuracy")
#print(accuracy_score(y_pred, y_test))
#print("Classification report")
#print(classification_report(y_pred,y_test))
#print("Confusion Matrix")
#print(confusion_matrix(y_pred,y_test))

#resultados dos testes
#print(y_pred)

#binarizacao dos resultados 
H=[]
for i in y_pred:
    if i=='0':
        H.append("Nao")
    elif i=='1':
        H.append("Nao")
    elif i=='2':
        H.append("Sim")
    elif i=='3':
        H.append("Sim")
    else:
        H.append("Sim")

#resultados em binario(sim ou nao)
#print(H)
executionTime= time.time() - start
print("Tempo do execucao")
print(executionTime)