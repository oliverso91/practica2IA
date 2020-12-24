#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import cv2 
import glob
import numpy as np
import matplotlib.pyplot as plt
import os
import random
source = None

def read_file(path):
    data = []
    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    result = np.array(data)
    np.random.shuffle(result)
    result = result.astype(float).T
    # Se separa el conjunto de pruebas del de entrenamiento
    slice_point = int(result.shape[1] * 0.7)
    train_set = result[:, 0: slice_point]
    test_set = result[:, slice_point:]

    # Se separan las entradas de las salidas
    train_set_x_orig = train_set[0: 3, :]
    train_set_y_orig = np.array([train_set[3, :]])

    #test_set_x_orig = test_set[0: 3, :]
    #test_set_y_orig = np.array([test_set[3, :]])

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, ['Perdera', 'Ganara']


def load_dataset(uni):
    print(uni)
    data = []
    
    pathM = "imagen/Mariano/"
    pathU = "imagen/USAC/"
    pathL = "imagen/Landivar/"
    pathF = "imagen/Marroquin/"
    
    #univerisades
    univerisades = ['Mariano', 'USAC', 'Landivar', 'Marroquin']
    
    for univerisad in univerisades:
        path = "imagen/" + univerisad + "/"
        data_path = os.path.join(path,'*g')
        files = glob.glob(data_path)
        for f1 in files: 
            train_dataset = plt.imread(f1)
            if(univerisad ==  uni):
                data.append([train_dataset, 1])
            else:
                data.append([train_dataset, 0])
                
    
    random.shuffle(data)
    
    slice_point = int(len(data) * 0.8)
    train_set = data[:slice_point]
    test_set = data[slice_point:]
    
    train_set_x = []
    train_set_y = []
    
    for i in range(0, len(train_set)):
        train_set_x.append(train_set[i][0])
        train_set_y.append(train_set[i][1])
    
    #train_set_x_orig = train_set[0][1]
    #print(len(train_set_x_orig))
    #train_set_y_orig = train_set

    #print(train_set_x_orig.shape[0])
    test_set_x = []
    test_set_y = []
    for i in range(0, len(test_set)):
        test_set_x.append(test_set[i][0])
        test_set_y.append(test_set[i][1])
        

    train_set_x_orig = np.array(train_set_x)
    train_set_y_orig = np.array(train_set_y)
     
    test_set_x_orig = np.array(test_set_x)
    test_set_y_orig = np.array(test_set_y)
    
    #print(test_set_x_orig)

    #for i in range(0, test_set_x_orig.shape[0]):
       # test_set_y.append(random.randrange(2))
    

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, ['No Gato', 'Gato']