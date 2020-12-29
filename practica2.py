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
import matplotlib.pyplot as plt
import glob
import os

def ejecutar(universidad):

    #y = json.dumps(parametroU)
    #m = json.loads(y)
    #parametro = m["universidad"]
    modelos = []
    selModelo = []
    nModelo = 0;


    #Cargando conjuntos de datos con for para hacer todos los modelos de una vez 
    
    train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, uni, classes = File.load_dataset(universidad)
    

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
    print('universidad: ' + uni)

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
    nModelo = 1;
    model1 = Model(train_set, test_set, reg=False, alpha=0.001, lam=310, maxi=1000, univ=uni, mod=nModelo)
    modelo1 = model1.training()
    
    selModelo.append(["model1", modelo1])
    
    nModelo =2;
    model2 = Model(train_set, test_set, reg=True, alpha=0.0002, lam=410, maxi=1050, univ=uni, mod=nModelo)
    modelo2 = model2.training()
    
    selModelo.append(["model2", modelo2])
    
    nModelo =3;
    model3 = Model(train_set, test_set, reg=True, alpha=0.00005, lam=250, maxi=1200, univ=uni, mod=nModelo)
    modelo3 = model3.training()
    
    selModelo.append(["model3", modelo3])
    
    nModelo = 4;
    model4 = Model(train_set, test_set, reg=True, alpha=0.0003, lam=300, maxi=1600, univ=uni, mod=nModelo)
    modelo4 = model4.training()
    
    selModelo.append(["model4", modelo4])
    
    nModelo = 5;
    model5 = Model(train_set, test_set, reg=False, alpha=0.00008, lam=150, maxi=1200, univ=uni, mod=nModelo)
    modelo5 = model5.training()
    
    selModelo.append(["model5", modelo5])
    


    Plotter.show_Model([model1, model2, model3, model4, model5], uni)
    modelos = np.array([modelo1, modelo2, modelo3, modelo4, modelo5])
    
    masAlto = np.max(modelos)
    
    for i in range(0, 5):
        if(selModelo[i][1] == masAlto):
            print("el mejor modelo es: " + str (selModelo[i][0]))
          
            p = []
            datosF = []
            contador = 0
            denominador = 0
            coincidencias = 0
            path = "iprueba/"
            data_path = os.path.join(path,'*g')
            files = glob.glob(data_path)
            for f1 in files: 
                    #print(f1)
                    #print(f1.find("Mariano"))
                    coincidencias = f1.find(uni)
                    if(coincidencias > 1):
                        denominador +=1
                        
                    image = plt.imread(f1)
                    p.append(image)
                    
            #print('p: ', p)
            grades = np.array(p)
            #print('grades: ', grades)
            result = model1.predecir(grades)
            print('----' + str(result))
            
            datosF = np.array(result)
            #print(len(np.where(datosF == 1)[0]))
            #print(len(datosF))
            
            contador = len(np.where(datosF == 1)[0])
            #denominador = len(np.where(datosF == 1)[0]) + len(np.where(datosF == 0)[0])
            exactitud = (contador / denominador) *100
            
            print("la exactitud es: " + str(exactitud))
            
            return exactitud
            break
        
    #Plotter.show_Model([model1], uni)
    
   
 
def guardarImage(jso):
    
    #print(jso)
    y = json.dumps(jso)
    m = json.loads(y)
    #print(m[])
    for i in range(0,len(m)):
        base = m[i]["base"]
       # print(base[23:])
        imgdata = base64.b64decode(base[23:])
        filename = m[i]["nombre"] 
        with open('iprueba/'+filename, 'wb') as f:
            f.write(imgdata)



app = Flask(__name__)

@app.route("/cuerpo",  methods = ['POST'])
def cuerpo():
    datos = []
    guardarImage(request.get_json())
    universidades = ['Mariano', 'USAC', 'Landivar', 'Marroquin']
    for i in range(0, len(universidades)):
        exactitud = ejecutar(universidades[i])
        datos.append([universidades[i], exactitud])
    print(datos)
    
    #predecir()
    #p = ejecutar(request.get_json())
    return json.dumps({'success': datos}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run()