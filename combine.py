import pandas as pd
s=pd.read_csv('r1.csv',index_col=0)
for i in range(2,17):
    name='r'+str(i)+'.csv'
    s['prob']+=pd.read_csv(name,index_col=0)['prob']
s['prob']/=16
s.to_csv('rf16_c16.csv')
