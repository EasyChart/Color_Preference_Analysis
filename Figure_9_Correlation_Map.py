# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 14:52:58 2018

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
import scipy.stats as stats
from pandas.api.types import CategoricalDtype


def score(a,b,dimension):       
# a is predict, b is actual. dimension is len(train[0]).
#n为样本数量，p为特征数量。即样本为n个[x1,x2,x3, … ,xp,y]
    aa=a.copy(); bb=b.copy()
    if len(aa)!=len(bb):
        print('not same length')
        return np.nan

    cc=aa-bb
    SSE=sum(cc**2)

    # RR means R_Square
    RR=1-sum((bb-aa)**2)/sum((bb-np.mean(bb))**2)

    n=len(aa); p=dimension
    Adjust_RR=1-(1-RR)*(n-1)/(n-p-1)
    # Adjust_RR means Adjust_R_Square

    return SSE,RR,Adjust_RR

N_Sample=41
file = open('Solid_Color.csv')
Color_mydata=pd.read_csv(file)
Colnames=Color_mydata.columns.values.tolist()

Color_theme=[]
for i in range(0,len(Color_mydata)):
    rgb =(int(Color_mydata['R'][i]),int(Color_mydata['G'][i]), int(Color_mydata['B'][i]))
    #np.array(mydata[i:i+1][['R', 'G', 'B']])
    #strs = "#"  
    #for j in range (0, rgb.shape[1]): 
    #    num = int(rgb[0,j]) 
    #    strs += str(hex(num))[-2:]  #每次转换之后只取0x7b的后两位，拼接到strs中 
        #print("转换后的16进制值为：" + strs) 
        
    Color_theme.append(f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')
    
# base_plot=(ggplot()
# +geom_point(Color_mydata,aes('a','b',fill='factor(ID)'),size=10,colour="black",show_legend=False)
# +geom_text(Color_mydata,aes('a','b',label='ID'),size=15,ha='left',va='top',colour="black",nudge_x=2)
# +scale_fill_manual(values=Color_theme)   
# +theme_matplotlib()
# +theme(
#     #text=element_text(size=15,face="plain",color="black"),
#     axis_title=element_text(size=18,face="plain",color="black"),
#     axis_text = element_text(size=15,face="plain",color="black"),
#     #legend_position='none',
#     #legend_position = (0,0),
#     figure_size = (10, 10),
#     dpi = 50
# ))
# print(base_plot)


# myColor_theme=pd.DataFrame({'y':np.repeat(0,N_Sample), 
#                             'ID':range(0,N_Sample)})

# base_plot=(ggplot(myColor_theme, aes(x = 'factor(ID)', y = 'y', fill = 'factor(ID)')) 
# + geom_tile(colour="black",show_legend=False) 
# +xlab('')
# +ylab('Mean value')
# #+geom_text(size=3,colour="white")
# +coord_equal()
# +scale_fill_manual(values=Color_theme)                   
# +theme_matplotlib()
# #+xlim(-0.5,42.5)
# +theme(
#     #text=element_text(size=15,face="plain",color="black"),
#     plot_background=element_rect(size=0.001),
#     axis_title=element_text(size=13,face="plain",color="black"),
#     axis_text = element_text(size=9,face="plain",color="black"),
#     legend_title = element_text(size=13,face="plain",color="black"),
#     legend_text= element_text(size=14,face="plain",color="black"),
#     legend_direction='horizontal',
#     legend_key=element_rect(color='black'),
#     #legend_title_align='bottom',
#     legend_position = (0.82,2),
#     figure_size = (10, 10),
#     dpi = 50
# ))
# print(base_plot)
#base_plot.save('Color_theme.pdf')  
#---------------------------------------------------------------------------------------------
#mydata=pd.read_csv(u"样本衬衫.csv",encoding = "gb18030")
file = open('Shirts.csv')
mydata=pd.read_csv(file,encoding = "utf-8")

Colnames=mydata.columns.values.tolist()

Mean_mydata_Total=mydata.groupby('Group').mean()
Mean_mydata_Total=pd.merge(Mean_mydata_Total,Color_mydata,left_index=True,right_index=True)


Color_theme2= pd.DataFrame(Color_theme)
Color_theme2=list((Color_theme2.append(Color_theme2)).values.T.flatten())

mydata_label=pd.DataFrame(columns=['Corr','Group','x','y'])
Mean_mydata_TotalDispaly=pd.DataFrame(columns=['Evaluation','Lch_L','C','H','a','b','Group','ID'])
sub_data=pd.DataFrame(columns=['Evaluation','Lch_L','C','H','a','b','Group','ID'])
Colnames=Mean_mydata_Total.columns.values.tolist()[:11]

Str_Feature='Lch_L'  #select 'Lch_L','C','H' 

list_corr=[]
for i in range(0,11):
    sub_data['Evaluation']=Mean_mydata_Total[Colnames[i]]
    sub_data.loc[:,['Lch_L','C','H','a','b','ID']]=Mean_mydata_Total.loc[:,['Lch_L','C','H','a','b','ID']]
    sub_data['Group']=list(np.repeat(Colnames[i],len(sub_data)))
    
    
    data_Corr=sub_data.loc[:,['Evaluation',Str_Feature]].corr()
    
    list_corr.append('R: ' +str(round(data_Corr.values[0][1],2)))
    
    Mean_mydata_TotalDispaly=Mean_mydata_TotalDispaly.append(sub_data)
    
mydata_label['Corr']=list_corr
mydata_label['Group']=pd.Categorical(np.array(mydata.columns.values.tolist()[4:15]), categories=np.array(mydata.columns.values.tolist()[4:15]),ordered=False)
mydata_label['x']=np.min(Mean_mydata_TotalDispaly[Str_Feature])
mydata_label['y']=-1.8

cat_type = CategoricalDtype(categories=  np.array(mydata.columns.values.tolist()[4:15]), ordered=False)
Mean_mydata_TotalDispaly['Group']=Mean_mydata_TotalDispaly['Group'].astype(cat_type)

base_plot=(ggplot()
+geom_point(Mean_mydata_TotalDispaly,aes(Str_Feature,'Evaluation',fill='factor(ID)'),stroke=0.25,size=5,show_legend=False)#size='Feature'
+geom_text(mydata_label,aes('x','y',label='Corr'),size=14,ha='left',va='top',colour="black",nudge_x=2)
+scale_fill_manual(values= Color_theme2)   
#+xlab("CIELAB Chroma (C*)") 
#+xlab("CIELAB Lightness (L*)") 
+xlab("CIELAB hue angle (hab)") 
+facet_wrap('~Group',nrow=1) 
+theme_matplotlib()
+theme(
       strip_background=element_rect(color="black"),
    strip_text=element_text(size=12,face="plain",color="black"),
    axis_title=element_text(size=15,face="plain",color="black"),
    axis_text = element_text(size=12,face="plain",color="black"),
    figure_size = (25, 2.5), 
    dpi = 50
))

base_plot.save('Figure_9_Correlation_Map_' + Str_Feature + '.pdf')
print(base_plot)