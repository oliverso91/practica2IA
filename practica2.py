#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import json
from FileManagement import File
from Logistic_Regression.Model import Model
from Logistic_Regression.Data import Data
from Logistic_Regression import Plotter
import numpy as np
import base64

def ejecutar():
    
    #y = json.dumps(parametroU)
    #m = json.loads(y)
    #parametro = m["universidad"]

    ONLY_SHOW = False #Veo si quiero mostrar una imagen del conjunto de datos

    #Cargando conjuntos de datos
    train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = File.load_dataset("Mariano")

    if ONLY_SHOW:
        #index = 14 #Gato
        index = 100 #No Gato
        index = 54 #Gato
        Plotter.show_picture(train_set_x_orig[index])
        print(classes[train_set_y[0][index]])
        exit()

    # Convertir imagenes a un solo arreglo
    train_set_x = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
    test_set_x = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

    #print(train_set_x)

    #Vemos cómo queda ahora la estructura de una imagen
    #(12288, 209) En este caso tiene 209 registros y cada registro tiene 12288 valores
    #En el caso de las notas cada registro tenía solo 3 valores, que eran las 3 notas
    #Por lo tanto, nuestro modelo va a tener 12288 + 1 Coeficientes, el + 1 es por B0
    #print(train_set_x.shape)

    # Vean la diferencia de la conversion
    print('Original: ', train_set_x_orig.shape)
    print('Con reshape: ', train_set_x.shape)

    #print('tamaño train_set_x_orig: ', len(train_set_x_orig))
    #print('tamaño train_set_x: ', len(train_set_x))

    #temp = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1)
    #print('Prueba: ', temp.shape)

    #print('train_set_x')
    #print(train_set_y)
    #exit()


    # Definir los conjuntos de datos
    train_set = Data(train_set_x, train_set_y, 255)
    test_set = Data(test_set_x, test_set_y, 255)

    # Se entrenan los modelos
    model1 = Model(train_set, test_set, reg=False, alpha=0.0001, lam=310, maxi=1000)
    model1.training()

    model2 = Model(train_set, test_set, reg=True, alpha=0.0002, lam=210, maxi=1050) #Se puede ver en la gráfica que hay SOBRE-AJUSTE
    model2.training()
    model3 = Model(train_set, test_set, reg=True, alpha=0.00005, lam=250, maxi=2000) #Aquí también se puede ver sobre-ajuste
    model3.training()

    model4 = Model(train_set, test_set, reg=True, alpha=0.0003, lam=300, maxi=3100) #Se ajusta mejor con la regulariación de 300, pero se tarda más
    model4.training()
    model5 = Model(train_set, test_set, reg=False, alpha=0.00008, lam=150, maxi=1200) #Baja más quitandole la regularización
    model5.training()
    #model2.training()

    # Se grafican los entrenamientos
    #Plotter.show_Model([model1, model2])
    Plotter.show_Model([model1, model2, model3, model4, model5])
    #Plotter.show_Model([model2])
    #return 1
 
def guardarImage(jso):
    
    #print(jso)
    y = json.dumps(jso)
    m = json.loads(y)
    #print(m[])
    for i in range(0,len(m)):
        base = m[i]["base"]
       # print(base[23:])
        imgdata = base64.b64decode(base[23:])
        filename = m[i]["nombre"]  # I assume you have a way of picking unique filenames
        with open('iprueba/'+filename, 'wb') as f:
            f.write(imgdata)


app = Flask(__name__)

@app.route("/cuerpo",  methods = ['POST'])
def cuerpo():
    ejecutar()
    #print(request.get_json())
    guardarImage(request.get_json())
    #p = ejecutar(request.get_json())
    return json.dumps({'success':'si'}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run()