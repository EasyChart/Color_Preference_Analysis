# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 14:32:38 2019

@author: Jie Zhang
"""

import math
import re  
import os
import pandas as pd
import numpy as np
from plotnine import *
#from plotnine.data import *
import matplotlib.pyplot as plt 
from pandas.api.types import CategoricalDtype


file = open('Solid_Color.csv')
Color_mydata=pd.read_csv(file)
Colnames=Color_mydata.columns.values.tolist()

Color_theme=[]
for i in range(0,len(Color_mydata)):
    rgb =(int(Color_mydata['R'][i]),int(Color_mydata['G'][i]), int(Color_mydata['B'][i]))
    Color_theme.append(f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')
    
#---------------------------------------------------------------------------------------------
#mydata=pd.read_csv(u"样本衬衫.csv",encoding = "gb18030")
#mydata=pd.read_csv(u"样本衬衫.csv",encoding = "gb18030")
file = open('Shirts.csv')
mydata=pd.read_csv(file,encoding = "utf-8")

Colnames=mydata.columns.values.tolist()

#------------------------------male-------------------------------------------
Mean_mydata_Total=mydata.groupby('Group').mean()#[(mydata['Job']=='颜色科学') | (mydata['Job']=='服装设计')]
#Mean_mydata_Total=Mean_mydata_Total.set_index('Group')

Mean_mydata_Total=pd.merge(Mean_mydata_Total,Color_mydata,left_index=True,right_index=True)
Colnames=Mean_mydata_Total.columns.values.tolist()[:11]
# =============================================================================
df_data  = pd.DataFrame(columns=['x','y','Group1','Group2','ID'])
Sub_data = pd.DataFrame(columns=['x','y','Group1','Group2','ID'])
list_corr=[]
Group1=[]
Group2=[]
Step=0.2
division= np.arange(-2,2+Step,Step)
for i in range(0,len(Colnames)): 
    for j in range(0,len(Colnames)):
        Sub_data['y']=Mean_mydata_Total[Colnames[i]].copy()
        if i!=j :
            Sub_data['x']=Mean_mydata_Total[ Colnames[j]]
            Sub_data['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
            Sub_data['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
            Sub_data['ID']=list(range(0,len(Mean_mydata_Total)))
         
            data_Corr=Sub_data.loc[:,['x','y']].corr()    
            list_corr.append('R: ' +str(round(data_Corr.values[0][0],2)))
            Group1.append(Colnames[i])
            Group2.append(Colnames[j])
        else:
            #count, division = np.histogram(Sub_data['y'], bins =np.arange(-2,2,0.2)) 
            division= np.arange(-2,2.1,0.2)
            Hist_x=[]
            Hist_y=[]
            Record_count=np.ones([1,len(division)])
            for k in range(0,len(Sub_data['y'])):
                x=Sub_data['y'][k]
                if (x<-2): x=-2
                if (x>2.1): x=2
                for h in range(0,len(division)):
                    if (x>=division[h]) & (x<division[h]+0.2):
                        xx=division[h].copy()
                        if (division[h]<-2):
                            xx=-2
                        elif (division[h]>2):
                            xx=2
                        Hist_x.append(xx+0.3)
                        Hist_y.append((Record_count[0,h].copy())*0.35-2)
                        Record_count[0,h]=Record_count[0,h]+1
            Sub_data['y']=list(Hist_y.copy())
            Sub_data['x']=list(Hist_x.copy()) 
            
        Sub_data['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
        Sub_data['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
        Sub_data['ID']=list(range(0,len(Mean_mydata_Total)))
         
        df_data=df_data.append(Sub_data)

cat_type = CategoricalDtype(categories= np.array(mydata.columns.values.tolist()[4:15]), ordered=False)
df_data['Group1']=df_data['Group1'].astype(cat_type)
df_data['Group2']=df_data['Group2'].astype(cat_type)

mydata_label2=pd.DataFrame(columns=['Corr','Group1','Group2','x','y'])
mydata_label2['Corr']=list_corr
mydata_label2['Group1']=pd.Categorical(Group1, categories=np.array(mydata.columns.values.tolist()[4:15]),ordered=False)
mydata_label2['Group2']=pd.Categorical(Group2, categories=np.array(mydata.columns.values.tolist()[4:15]),ordered=False)
mydata_label2['x']=-1.8
mydata_label2['y']=-1.5
          
base_plot=(ggplot() 
#其气泡的颜色填充由Class映射，大小由age映射
+geom_point(df_data, aes(x = 'x', y = 'y', fill= 'factor(ID)'),colour="black",stroke=0.25,alpha=1,size=4,show_legend=False) 
#设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
+geom_text(mydata_label2,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
+scale_fill_manual(values=Color_theme)                          
+facet_grid( 'Group1~ Group2',scales='free')  #类别Class为列变量,
+ylim(-2,2)
+xlim(-2,2)
+theme_matplotlib()
+theme(
    #text=element_text(size=15,face="plain",color="black"),
    axis_title=element_text(size=12,face="plain",color="black"),
    axis_text = element_text(size=14,face="plain",color="black"),
    strip_text=element_text(size=12,face="plain",color="black"),
    strip_background=element_blank(),
    #legend_position='none',
    #legend_position = c(0.88,0.88),
    figure_size = (20, 20),
    dpi = 50
))
print(base_plot)       
base_plot.save('Figure10_scatterplot_matrix.pdf')   