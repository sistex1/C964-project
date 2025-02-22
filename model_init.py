import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

RFC = None
metrics = []

def train_model():
    df = pd.read_csv('glass.csv')
    df.dropna(inplace=True)

    x = df.values[:, 0:9]
    y = df.values[:, 9]

    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=40)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    global RFC
    RFC = RandomForestClassifier(class_weight="balanced", random_state=40)
    RFC.fit(X_train, Y_train)

    predict = RFC.predict(X_test)

    accuracy = accuracy_score(Y_test, predict)
    precision = precision_score(Y_test, predict, average='weighted', zero_division=0)
    recall = recall_score(Y_test, predict, average='weighted', zero_division=0)
    f1 = f1_score(Y_test, predict, average='weighted')

    metrics.clear()

    metrics.append(accuracy)
    metrics.append(precision)
    metrics.append(recall)
    metrics.append(f1)

def input_predict(submit):
    submit=np.array(submit).reshape(1,-1)
    prediction = RFC.predict(submit)
    return int(prediction[0])
    print(f"Prediction: {prediction}")

'''
RI: Refractive Index
Na: Sodium (weight %)
Mg:Magnesium (weight %)
Al:Aluminum (weight %)
Si: Silicon (weight %)
K: Potassium (weight %)
Ca: Calcium (weight %)
Ba:Barium (weight %)
Fe: Iron (weight %)
Type: Glass Type (Target variable)

Glass Type Classification
The dataset contains different categories of glass, which may include:

1: Building Windows (Float Processed)
2: Building Windows (Non-Float Processed)
3: Vehicle Windows
4: Containers
5: Tableware
6: Headlamps
'''

