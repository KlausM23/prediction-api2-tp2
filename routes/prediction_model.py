from fastapi import APIRouter
import joblib
from sklearn.calibration import LabelEncoder
from schemas.prediction import Prediction
import pandas as pd
import numpy as np

prediction = APIRouter()

posts = []

@prediction.get("/predictions")
def get_prediction():
    return posts

@prediction.get("/prediction/{id_}")
def get_prediction_id(id_ : int):
    for post in posts:
        if post["Id"] == id_:
            return post

    return "Data not found"

@prediction.post("/prediction")
def create_data(data_prediction: Prediction):
    modeloArbol = joblib.load('routes/DecisionTreeRegressor.pkl')

    data_prueba = {
        'Tipo_animal': data_prediction.animalType,
        'Sexo': data_prediction.sex,
        'Color' : data_prediction.color,
        'Raza' : data_prediction.breed
    }
    
    data_prueba['Tipo_animal'] = data_prueba['Tipo_animal'].lower()
    data_prueba['Sexo'] = data_prueba['Sexo'].lower()
    data_prueba['Color'] = data_prueba['Color'].lower()
    data_prueba['Raza'] = data_prueba['Raza'].lower()

    tp = sex = co = ra = 0

    if data_prueba['Tipo_animal'] == 'gato':
        tp = 0
    elif data_prueba['Tipo_animal'] == 'perro':
        tp = 1

    if data_prueba['Sexo'] == 'macho':
        sex = 1
    elif data_prueba['Sexo'] == 'hembra':
        sex = 0

    if data_prueba['Color'] == 'blanco':
        co = 0
    elif data_prueba['Color'] == 'gris':
        co = 1
    elif data_prueba['Color'] == 'marrón':
        co = 2
    elif data_prueba['Color'] == 'negro':
        co = 3
    elif data_prueba['Color'] == 'variado':
        co = 4

    if data_prueba['Raza'] == 'beagle':
        ra = 0
    elif data_prueba['Raza'] == 'bengala':
        ra = 1
    elif data_prueba['Raza'] == 'desconocido':
        ra = 2
    elif data_prueba['Raza'] == 'golden retriever':
        ra = 3
    elif data_prueba['Raza'] == 'labrador':
        ra = 4
    elif data_prueba['Raza'] == 'pastor alemán':
        ra = 5
    elif data_prueba['Raza'] == 'persa':
        ra = 6
    elif data_prueba['Raza'] == 'poodle':
        ra = 7
    elif data_prueba['Raza'] == 'schnauzer':
        ra = 8
    elif data_prueba['Raza'] == 'siamés':
        ra = 9
    elif data_prueba['Raza'] == 'yorkshire':
        ra = 10
    
    tp2 = tp
    sex2 = sex
    co2 = co
    ra2 = ra

    le = LabelEncoder()

    tp_animal = pd.Series(np.array(["Gato"]))
    le.fit(tp_animal)
    tp = le.transform(tp_animal)

    tpcolor = pd.Series(np.array(["Variado"]))
    le.fit(tpcolor)
    co = le.transform(tpcolor)

    tp_sex = pd.Series(np.array(["Macho"]))
    le.fit(tp_sex)
    sex = le.transform(tp_sex)

    tp_ra = pd.Series(np.array(["Bengala"]))
    le.fit(tp_ra)
    ra = le.transform(tp_ra)

    tp[0] = tp2
    sex[0] = sex2
    co[0] = co2
    ra[0] = ra2
    
    datos_a_predecir = {
    'Tipo_animal' : tp,
    'Sexo' : sex,
    'Color' : co,
    'Raza' : ra
    }

    datos_a_predecir = pd.DataFrame(datos_a_predecir)
    
    result1 = modeloArbol.predict_proba(datos_a_predecir)

    final_data = {
    'Id' : data_prediction.id,
    'Tipo_animal': data_prediction.animalType,
    'Sexo': data_prediction.sex,
    'Color' : data_prediction.color,
    'Raza' : data_prediction.breed,
    'Si_adoptado' : str(round(result1[0][1], 3)),
    'No_adoptado' : str(round(result1[0][0], 3))
    }

    #print(datos_a_predecir)
    #print(result1)
    posts.append(final_data)
    return final_data