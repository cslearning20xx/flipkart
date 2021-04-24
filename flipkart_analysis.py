# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 12:14:51 2021

@author: 91998
"""


import pandas as pd
import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt



df_full = []
for i in range(5649):
    filename = "C:/Users/91998/Flipkartnew/flipkart_data_" + str(i) + ".csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        df_full.append(df)
df_full = pd.concat(df_full, sort = True, ignore_index = True)
df_full.head()

df1 = df_full[['Name', 'Price', 'Rating', 'CountRating', 'CountReview', 'Size', 'Style', 'Type', 'Material', 'Ccolor','CSize' ]]

df1.rename(columns = {'Ccolor':'Color', 'CSize': 'Size Category'}, inplace = True)
df1.drop(df1[df1.Name.isnull()].index, inplace=True)
df1.drop_duplicates([ 'Name', 'Size', 'Type', 'Material', 'Color'],inplace = True)

def getarea(r):
    try:
        dim = r.strip().split(" ")
        area = int(dim[0])*int(dim[3])
    except:
        area = np.nan
    return area

def getUnitPrice(r):
    return(r['Price']/r['Area']) *10000

df1['Area']= df1['Size'].apply( getarea)
df1['UnitPrice'] = df1.apply(getUnitPrice, axis =1)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

df2 = df1[(df1.Material == " Cotton") | (df1.Material == ' Polyester') ]
df2 = df1[(df1.Material == " Cotton") | (df1.Material == ' Polyester') ]
sns.catplot(x="Type", y="UnitPrice", hue = "Material", kind="swarm", data=df2)


fig,ax = plt.subplots(1,2, figsize = (12,5), sharex = True)
ax[0].set_title("Polyster")
ax[1].set_title("Cotton")

sns.scatterplot( x = 'Area', y = 'UnitPrice', data = df1[(df1.Material == ' Polyester') ], hue = 'Type', ax = ax[0])
sns.scatterplot( x = 'Area', y = 'UnitPrice', data = df1[(df1.Material == ' Cotton') ], hue = 'Type', ax = ax[1])
sns.catplot( x="Size Category", y="Area",kind="swarm", data=df2)