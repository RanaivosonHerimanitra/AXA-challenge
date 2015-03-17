import os
import numpy as np
import pandas as pd
from random import random
from xgb_classifier import *
def findstart(x,y):
    x=np.array(x)
    y=np.array(y)
    for i,j in zip(x,y):
        if i!=0 or j!=0:
            return i**2+j**2  
def findeverystart(x,y):
    x=np.array(x)
    y=np.array(y)
    xx=[]
    yy=[]
    prei=0
    prej=0
    stop=False
    c=0
    for i,j in zip(x,y):
        if i!=prei or j!=prej:
            if stop:
                xx.append( (i-prei)**2+(j-prej)**2)
                """
                if c+5<len(x):
                    yy.append( (i-x[c+5])**2+(j-y[c+5])**2)
                else:
                    yy.append( (i-x[-1])**2+(j-y[-1])**2)
                """
            prei=i
            prej=j
            stop=False
        else:
            stop=True
        c+=1
    if len(xx)==0:
        return [0]*12            
    sdist=[np.percentile(np.array(xx),per*10) for per in range(0,11)]
    sdist.append(len(xx))
    #sdist+=[np.percentile(np.array(yy),per*20) for per in range(0,6)]
    #sdist=[np.mean(xx)]
    return sdist
def findeverystop(x,y):
    x=np.array(x)
    y=np.array(y)
    xx=[]
    prei=0
    prej=0
    
    run=False
    c=0
    for i,j in zip(x,y):
        if i==prei and j==prej:            
            if run:
                xx.append( (i-x[c-2])**2+(j-y[c-2])**2)
            run=False
        else:
            run=True
        c+=1
        prei=i
        prej=j
    if len(xx)==0:
        return [0]*12       
    sdist=[np.percentile(np.array(xx),per*10) for per in range(0,11)]
    sdist.append(len(xx))
    #sdist=[np.mean(xx)]
    return sdist
             
def speeddist(trip,lag):
    
    #rate=3.6*sqrt((np.diff(trip['x']))^2+(np.diff(trip['y']))^2)/20
    ind=range(0,trip.shape[0],lag)
    x=trip['x'][ind]
    y=trip['y'][ind]
    rate=3.6*((np.diff(x))**2+(np.diff(y))**2)**0.5/20
    sdist=[np.percentile(rate,per*5) for per in range(0,21)]
    #sdist.append(findstart(x,y))
    sdist+=findeverystart(x,y)
    sdist+=findeverystop(x,y)
    return sdist
    
def accelarationdist(trip,lag):
    ind=range(0,trip.shape[0],lag)
    x=trip['x'][ind]
    y=trip['y'][ind]
    rate=3.6*((np.diff(x))**2+(np.diff(y))**2)**0.5/20
    acce=np.diff(rate)#/20
    if len(acce)<=1:
        return [0]*21
    adist=[np.percentile(acce,per*5) for per in range(0,21)]
    return adist

def speedyturningdist(trip,lag):
    #multiply rate with turning angle?
    ind=range(0,trip.shape[0],lag)
    x=trip['x'][ind]
    y=trip['y'][ind]
    rate=3.6*((np.diff(x))**2+(np.diff(y))**2)**0.5/20
    angle=np.arctan(np.divide(np.diff(x),np.diff(y)))
    angle=np.diff(angle)
    stdist=[np.percentile(angle,per*5) for per in range(0,21)]
    return stdist
def turningdist(trip,lag):
    #multiply rate with turning angle?
    ind=range(0,trip.shape[0],lag)
    x=trip['x'][ind]
    y=trip['y'][ind]
    rate=3.6*((np.diff(x))**2+(np.diff(y))**2)**0.5/20
    dx=np.diff(x)
    dy=np.diff(y)
    xx=[]
    dd=((dy**2+dx**2)**0.5)
    angle=(dy[1:]*dy[:-1]+dx[1:]*dx[:-1])/(dd[:-1]*dd[1:])
    if len(angle)<=1:
        return [0]*6 
    #angle=np.arctan(np.divide(np.diff(x),np.diff(y)))
    stdist=[np.percentile(angle,per*20) for per in range(0,6)]
    return stdist 
from random import shuffle
def extract_one_driver(driverPath,triplist=[],shuf=False,ratio=1.0,tx=None,tratio=100,sratio=-100):
    trips=[]
    if len(triplist)>0:
        trips+=[i+'.csv' for i in triplist]
        #print trips
    if tx!=None :#and len(trips)<len(os.listdir(driverPath))*tratio:
        driver=driverPath.split('/')[-1]
        for p in tx[driver]:
            if p>tratio or p<sratio:              
                trips.append(tx[driver][p]+'.csv')
            
    else:
        trips=os.listdir(driverPath)
    feature=[]
    ids=[]
    if shuf:
        shuffle(trips)
    for c,trip in enumerate(trips):
        if '.csv' not in trip:
            continue
        #print trip
        t=pd.read_csv(driverPath+'/'+trip)
        #fea=speeddist(t,lag=10)
        fea=np.hstack((speeddist(t,lag=1),accelarationdist(t,lag=1),turningdist(t,lag=1)))
        feature.append(fea)
        ids.append(trip[:-4])
        if c>len(trips)*ratio:
            break
    return np.array(feature) , ids     
 
path='../../data/driver2'
drivers=os.listdir(path)

import pickle

for driver in drivers:
    if '.' in driver:
        continue
    
    if True:
        print driver,'start'
        X,idX=extract_one_driver(driverPath=path+'/'+driver)
        pickle.dump(X,open('data2/'+driver+'.p','w'))
        pickle.dump(idX,open('data2/'+driver+'_id.p','w'))
        #print driver,'done'
 

 
