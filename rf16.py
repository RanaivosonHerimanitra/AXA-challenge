import os
import numpy as np
import pandas as pd
from random import random
from sklearn.ensemble import RandomForestClassifier
   
 
path='../../data/drivers'
drivers=os.listdir(path)
f=open(sys.argv[1],'w')
f.write('driver_trip,prob\n')
f.close()
import pickle
def rf_train_predict(X,y,Xt):
    clf=RandomForestClassifier(n_estimators=150, criterion='entropy', max_depth=15,  n_jobs=1, min_samples_leaf=5,verbose=1)
    clf.fit(X,y)
    return clf.predict_proba(Xt).T[1]
for driver in drivers:
    if '.' in driver:
        continue
 
    #X,idX=extract_one_driver(path+'/'+driver)
    X,idX=pickle.load(open('../eachdriver/data2/'+driver+'.p')),pickle.load(open('../eachdriver/data2/'+driver+'_id.p'))
    y=np.ones(X.shape[0])
    rr=int(random()*(len(drivers)-1))
    while drivers[rr]==driver:
        rr=int(random()*(len(drivers)-1))
    DR=drivers[rr]
    XR=pickle.load(open('../eachdriver/data2/'+DR+'.p'))
    #XR=extract_one_driver(path+'/'+DR)[0]
    for i in range(6):
        rr=int(random()*(len(drivers)-1))
        while drivers[rr]==driver:
            rr=int(random()*(len(drivers)-1))

        DR=drivers[rr]
        XR=np.vstack((XR,pickle.load(open('../eachdriver/data2/'+DR+'.p'))))
        #XR=np.vstack((XR,extract_one_driver(path+'/'+DR)[0]))
   
    yr=np.zeros(XR.shape[0])
    X=np.nan_to_num(X)
    XR=np.nan_to_num(XR)
    ypred=rf_train_predict(np.vstack((X,XR)),np.concatenate((y,yr)),X)

    print 'driver',driver,'done'
    for c,i in enumerate(ypred):
        f=open(sys.argv[1],'a')
        f.write(driver+'_'+idX[c]+','+str(i)+'\n')
        f.close()
 

 
