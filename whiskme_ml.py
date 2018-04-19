
# coding: utf-8

# In[106]:

from flask import Flask
from flask import request
from flask import jsonify
import pprint
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

#create scaler instance
scaler=MinMaxScaler()


# In[3]:


#Import data
whiskey = pd.read_csv('content/data/whisky_subset_ml.csv')



# In[103]:

@app.route("/hello")
def hello():
    name = request.args.get('name', '')
    pref1 = request.args.get('pref1')
    pref2 = request.args.get('pref2')
    return "Hello " + name + ".  You like: " + pref1 + " " + pref2

@app.route("/whiskme")
def whiskme_ws():
    whiskey = request.args.get('whiskey', '')
    pref1 = request.args.get('pref1')
    pref2 = request.args.get('pref2')
    whiskme_result = whiskme(whiskey, pref1, pref2)
    pprint.pprint(whiskme_result)

    #result = {
    #    'input_whiskey': whiskey,
    #    'pref1': pref1,
    #    'pref2': pref2,
    #    'result': str(whiskme_result)
    #}
    return jsonify(whiskme_result)

def whiskme(input_bottle,pref1,pref2,whiskey_db=whiskey,KNN=False):
        
    #Create numeric df and drop unused fields, create a reference table for ID and distiller
    whis=whiskey_db.drop(['Distillery','Postcode','Latitude','Longitude'],axis=1).iloc[:,1:].add(1)
    w_ref=whiskey_db[['Distillery','RowID']]
    input_idx=w_ref[w_ref['Distillery']==input_bottle].index

    #Find consistency weights, grab indices
    pr_idx=[w_ref[w_ref['Distillery']==pref1].index,w_ref[w_ref['Distillery']==pref2].index]

    weight_temp=(whis.iloc[pr_idx[0],:].values-whis.iloc[pr_idx[1],:].values)
    #Compute dispersion ('entropy') amongst preferences
    weight=(weight_temp.reshape(12,))*10+1
    #.abs().mul(10,axis=0).add(1,axis=0))

    #Compute weighted input values
    #broadcast values
    #arr1=np.transpose(weight)
    #S1=pd.Series(weight)
    w_in_up=whis.mul(weight)
    w_in_dn=whis.div(weight)

    
    #Compute the new Preference match columns, individuals
    temp=w_in_dn.iloc[pr_idx[0],:].sum(axis=1).values.reshape(1,)
    temp2=pd.DataFrame(w_in_dn.sum(axis=1).values/temp).add(-1,axis=0).abs().add(.1,axis=0)
    w_pref1_perc=temp2
    w_pref1_perc.columns=['Pref1']
    #Compute the new Preference match columns, individuals
    temp1=w_in_dn.iloc[pr_idx[1],:].sum(axis=1).values.reshape(1,)
    temp3=pd.DataFrame(w_in_dn.sum(axis=1).values/temp1).add(-1,axis=0).abs().add(.1,axis=0)
    w_pref2_perc=temp3
    w_pref2_perc.columns=['Pref2']

    #Rescale the preference match cols
    w_pref1_trans=pd.DataFrame(scaler.fit_transform(np.log(w_pref1_perc)), index=w_pref1_perc.index).add(-1,axis=0).abs()
    w_pref2_trans=pd.DataFrame(scaler.fit_transform(np.log(w_pref2_perc)), index=w_pref2_perc.index).add(-1,axis=0).abs()

    #Combine and avg the pref cols
    #join new preference % to table
    w_pref_avg=pd.DataFrame(pd.concat([w_pref1_trans,w_pref2_trans],axis=1).mean(axis=1))
    w_pref_avg.columns=['Preference_Match']
    whiskey_full=pd.concat([whiskey_db,w_pref_avg],axis=1)

    output={'Input_Bottle':w_ref['Distillery'].iloc[input_idx].iloc[0],
            'Output_Score':float(np.round(whiskey_full['Preference_Match'].iloc[input_idx].multiply(100),1)),
            'Recommended':[whiskey_full.sort_values('Preference_Match',ascending=False)['Distillery'].iloc[1],whiskey_full.sort_values('Preference_Match',ascending=False)['Distillery'].iloc[2] ],
            'Input_Pref':[ w_ref['Distillery'].iloc[pr_idx[0]].iloc[0], w_ref['Distillery'].iloc[pr_idx[1]].iloc[0] ]
            }
    return output
    #if KNN==False:
    #return: Preferred Match Value, Bottle1, Bottle2, Bottle3
    #return w_ref['Distillery'].iloc[input_idx],np.round(whiskey_full['Preference_Match'].iloc[input_idx].multiply(100),1), whiskey_full.sort_values('Preference_Match',ascending=False)['Distillery'].iloc[1],whiskey_full.sort_values('Preference_Match',ascending=False)['Distillery'].iloc[2] 



#pprint.pprint(whiskme('Aberlour','Ardmore','Tomatin'))

