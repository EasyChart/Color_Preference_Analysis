#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 17:09:06 2018

@author: peter
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
from scipy.optimize import curve_fit   
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
    Color_theme.append(f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}')

#---------------------------------------------------------------------------------------------
#mydata=pd.read_csv(u"样本衬衫.csv",encoding = "gb18030")
N_Sample=41
file = open('Shirts.csv')
mydata=pd.read_csv(file,encoding = "utf-8")
#mydata.to_csv('Shirts2.csv', encoding='utf_8_sig')

mydata['Gender'][mydata["Gender"]=='男']=1
mydata['Gender'][mydata["Gender"]=='女']=0

Mean_mydata_Total=mydata.groupby('Group').mean()
Mean_mydata_Total=pd.merge(Mean_mydata_Total,Color_mydata,left_index=True,right_index=True)
#=========================================================Curve-Fitting==============================================
Fitting_data = pd.DataFrame(columns=['Evaluation','Fitting Value','ID','Group'])
label_data=pd.DataFrame(columns=['R-squared','Group','x','y'])
#===================================================Cold:Warm=========================================================
 
def func_Cold_Warm(X,a,b,c,d,e):
    x,y = X
    return a+b*pow(x,c)*np.cos((y-d)/180*math.pi)

y=Mean_mydata_Total['Cold:Warm'].values
C=Mean_mydata_Total['C'].values
H=Mean_mydata_Total['H'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7.,50,.9
popt, pcov = curve_fit(func_Cold_Warm, (C,H), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
d=popt[3]
e=popt[4]
yvals=func_Cold_Warm((C,H),a,b,c,d,e)

#Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y)))})
Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('Cold:Warm',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]
print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR))

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'Cold:Warm'},index=[0])
label_data=label_data.append(mydata_label)

# =============================================================================
# base_plot=(ggplot()
# +geom_point(Sub_Fitting_data,aes('Evaluation','Fitting Value',fill='factor(ID)'),size=10,colour="black",show_legend=False)
# #+geom_text(PC,aes('PCA1','PCA2',label='ID'),size=15,ha='left',va='top',colour="black",nudge_x=0.1)
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
# =============================================================================

#========================================Heavy:Light=========================================================
def func_Heavy_Light(X,a,b,c):
    x,y = X
    return a+b*x+c*y

y=Mean_mydata_Total['Heavy:Light'].values
Lch_L=Mean_mydata_Total['Lch_L'].values
C=Mean_mydata_Total['C'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7.
popt, pcov = curve_fit(func_Heavy_Light, (Lch_L,C), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
#d=popt[3]
yvals=func_Heavy_Light((Lch_L,C),a,b,c)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('Heavy:Light',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'Heavy:Light'},index=[1])
label_data=label_data.append(mydata_label)

#========================================Passive:Active========================================================
def func_Passive_Active(X,a,b):
    x = X
    return a+b*x

y=Mean_mydata_Total['Passive:Active'].values
Lch_L=Mean_mydata_Total['Lch_L'].values
C=Mean_mydata_Total['C'].values
# initial guesses for a,b,c:
p0 = 8., 2.
popt, pcov = curve_fit(func_Passive_Active, C, y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]

yvals=func_Passive_Active(C,a,b)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('Passive:Active',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]
print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'Passive:Active'},index=[2])
label_data=label_data.append(mydata_label)
 
#========================================FatL:SlimL========================================================
Mean_mydata_Gender=mydata.groupby(['Gender','Group'],).mean().reset_index()
#Mean_mydata_Gender = Mean_mydata_Gender.reset_index()  
#Mean_mydata_Gender['Gender']=Mean_mydata_Gender.index.names[0]
#Mean_mydata_Gender['ID']=Mean_mydata_Gender['Group'].copy()
#Mean_mydata_Gender.drop(columns=['Group'])
Mean_mydata_Gender=Mean_mydata_Gender.rename(columns = {'Group':'ID'})

Feature='FatL:SlimL'
data_FatL_SlimL= pd.DataFrame(columns=['Evaluation',Feature,'ID','Group','Gender'])
Subdata_FatL_SlimL= pd.DataFrame(columns=['Evaluation',Feature,'ID','Group','Gender'])

Colnames=Mean_mydata_Gender.columns.values.tolist()#[4:15]
Colnames2= Colnames[4:-2].copy()
Colnames2.remove(Feature) 
list_corr=[]
Group1=[]
Group2=[]
for j in [0,1]:
    temp_data=Mean_mydata_Gender[(Mean_mydata_Gender['Gender']==j)].copy()
    for i in range(0,len(Colnames2)):
        Subdata_FatL_SlimL['Evaluation']=temp_data[Colnames2[i]].values
        Subdata_FatL_SlimL.loc[:,['ID','Gender',Feature]]=temp_data.loc[:,['ID','Gender',Feature]].values
        
        Subdata_FatL_SlimL['Group']=np.repeat(Colnames2[i],len(Subdata_FatL_SlimL))
        data_FatL_SlimL=data_FatL_SlimL.append(Subdata_FatL_SlimL)
        
        
        data_Corr=Subdata_FatL_SlimL.loc[:,['Evaluation',Feature]].corr()    
        list_corr.append('Corr: ' +str(round(data_Corr.values[0][1],2)))
        Group1.append(j)
        Group2.append(Colnames2[i])

cat_type = CategoricalDtype(categories= Colnames2, ordered=False)
            
data_FatL_SlimL['Group']=data_FatL_SlimL['Group'].astype(cat_type)
data_FatL_SlimL.Gender = data_FatL_SlimL.Gender.map({ 0:'Female',1:'Male'})


mydata_label2=pd.DataFrame(columns=['Corr','Gender','Group','x','y'])
mydata_label2['Corr']=list_corr
mydata_label2['Gender']=Group1
mydata_label2['Group']=pd.Categorical(Group2, categories=Colnames2,ordered=False)
mydata_label2['x']=-1.7
mydata_label2['y']=-0.7

mydata_label2.Gender = mydata_label2.Gender.map({ 0:'Female',1:'Male'})

#data_FatL_SlimL['Evaluation'] = data_FatL_SlimL['Evaluation'].convert_objects(convert_numeric=True)
#data_FatL_SlimL['FatL:SlimL'] = data_FatL_SlimL['FatL:SlimL'].convert_objects(convert_numeric=True)

# base_plot=(ggplot() 
# #其气泡的颜色填充由Class映射，大小由age映射
# +geom_point(data_FatL_SlimL, aes(x = 'Evaluation', y = Feature, fill= 'factor(ID)'),colour="black",alpha=1,size=3,show_legend=False) 
# #设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
# +geom_text(mydata_label2,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
# +scale_fill_manual(values=Color_theme)                          
# +facet_grid( 'Gender~ Group',scales='fixed')  #类别Class为列变量,
# #+ylim(-1.5,1.5)
# #+xlim(-1.5,1.5)
# +theme_matplotlib()
# +theme(
#     #text=element_text(size=15,face="plain",color="black"),
#     axis_title=element_text(size=12,face="plain",color="black"),
#     axis_text = element_text(size=14,face="plain",color="black"),
#     strip_text=element_text(size=12,face="plain",color="black"),
#     strip_background=element_blank(),
#     #legend_position='none',
#     #legend_position = c(0.88,0.88),
#     figure_size = (20, 5),
#     dpi = 50
# ))
# print(base_plot)        
#base_plot.save('Grid_FatL_SlimL.pdf')         
        

def func_FatL_SlimL(X,a,b,c,d):
    x,y,z = X
    return a+b*x+c*y+d*z

y=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['FatL:SlimL'].values

x1=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['Heavy:Light'].values
x2=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['Passive:Active'].values
x3=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Cold:Warm'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7.,.7
popt, pcov = curve_fit(func_FatL_SlimL, (x1,x2,x3), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
d=popt[3]
#e=popt[4]
yvals=func_FatL_SlimL((x1,x2,x3),a,b,c,d)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('FatL:SlimL',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'FatL:SlimL'},index=[3])
label_data=label_data.append(mydata_label)


#-----------------------------------------Masculine : Feminine--------------------------------
def func_Masculine_Feminine(X,a,b,c,d):
    x,y,z = X
    return a+b*x+c*y+d*z#+d*y*y

y=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Masculine:Feminine'].values
x1=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Heavy:Light'].values
x2=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Cold:Warm'].values
x3=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Passive:Active'].values
#x3=Mean_mydata_Total[ 'Passive:Active'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7., 7.
popt, pcov = curve_fit(func_Masculine_Feminine, (x1,x2,x3), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
d=popt[3]
#e=popt[4]
yvals=func_Masculine_Feminine((x1,x2,x3),a,b,c,d)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('Masculine:Feminine',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'FatL:SlimL'},index=[3])
label_data=label_data.append(mydata_label)


#========================================HMatch:EMatch========================================================
def func_HMatch_EMatch(X,a,b,c,d):
    x,y = X
    return a+b*x+c*y+d*x*x

y=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['HMatch:EMatch'].values
x1=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['Plain: Gaudy'].values
x2=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==0]['FatL:SlimL'].values
#x3=Mean_mydata_Total[ 'Passive:Active'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7.,.7
popt, pcov = curve_fit(func_HMatch_EMatch, (x1,x2), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
d=popt[3]
#e=popt[4]
yvals=func_HMatch_EMatch((x1,x2),a,b,c,d)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('HMatch:EMatch-0',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'HMatch:EMatch-0'},index=[5])
label_data=label_data.append(mydata_label)

#======================================

y=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['HMatch:EMatch'].values
x1=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Plain: Gaudy'].values
x2=Mean_mydata_Gender[Mean_mydata_Gender['Gender']==1]['Masculine:Feminine'].values
#x3=Mean_mydata_Total[ 'Passive:Active'].values
# initial guesses for a,b,c:
p0 = 8., 2., 7.,.7
popt, pcov = curve_fit(func_HMatch_EMatch, (x1,x2), y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]
d=popt[3]
#e=popt[4]
yvals=func_HMatch_EMatch((x1,x2),a,b,c,d)

Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat('HMatch:EMatch-1',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],'Group':'HMatch:EMatch-1'},index=[5])
label_data=label_data.append(mydata_label)

#========================================Plain:Gaudy========================================================
def func_Plain_Splendid(X,a,b):
    x = X
    return a+b*x

y=Mean_mydata_Total['Plain: Gaudy'].values
x=Mean_mydata_Total['Passive:Active'].values
# initial guesses for a,b,c:
p0 = 8., 2.
popt, pcov = curve_fit(func_Plain_Splendid, x, y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
#d=popt[3]
yvals=func_Plain_Splendid(x,a,b)

Sub_Fitting_data=pd.DataFrame({'x':x,'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),
                               'Groupx':np.repeat('Passive:Active',len(y)),'Groupy':np.repeat('Plain: Gaudy',len(y)),
                               'Group':np.repeat('Plain: Gaudy',len(y))})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],
                           'Groupx':'Passive:Active','Groupy':'Plain: Gaudy',
                           'Group':'Plain: Gaudy'},index=[1])
label_data=label_data.append(mydata_label)

# base_plot=(ggplot()
# #+geom_point(Sub_Fitting_data,aes(x='x',y='Fitting Value',fill='factor(ID)'),size=6,stroke=0.25,colour="black",show_legend=False)
# +geom_point(Sub_Fitting_data,aes(x='x',y='Evaluation',fill='factor(ID)'),size=6,stroke=0.25,colour="black",show_legend=False)

# +geom_line(Sub_Fitting_data,aes(x='x',y='Fitting Value'),size=1,colour="black",show_legend=False)

# #+geom_text(label_data,aes('x','y',label='R-squared'),size=10,ha='left',va='top',colour="black",nudge_x=0)


# +scale_fill_manual(values=Color_theme,scales='free_x')   
# #+facet_wrap('~Group',nrow=1) 
# +theme_matplotlib()
# +theme(
#     strip_text=element_text(size=9,face="plain",color="black"),
#     strip_background=element_rect(colour='black'),
#     #text=element_text(size=15,face="plain",color="black"),
#     axis_title=element_text(size=18,face="plain",color="black"),
#     axis_text = element_text(size=15,face="plain",color="black"),
#     #legend_position='none',
#     #legend_position = (0,0),
#     figure_size = (8, 8),
#     dpi = 50
# ))
# print(base_plot)


#--------------------------------------Like:Dislike--------------------------------------------------

def func_Like_Dislike(X,a,b):
    x = X
    return a+b*x

y=Mean_mydata_Total['Dislike:Like'].values
x=Mean_mydata_Total['HMatch:EMatch'].values
# initial guesses for a,b,c:
p0 = 8., 2.
popt, pcov = curve_fit(func_Like_Dislike, x, y,p0)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
#d=popt[3]
yvals=func_Like_Dislike(x,a,b)

Sub_Fitting_data=pd.DataFrame({'x':x,'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),
                               'Groupx':np.repeat('Passive:Active',len(y)),'Groupy':np.repeat('Plain: Gaudy',len(y)),
                               "Group":'Dislike:Like'})
Fitting_data=Fitting_data.append(Sub_Fitting_data)

Corr=Sub_Fitting_data.loc[:,['Evaluation','Fitting Value']].corr().values[0][1]

print(Corr) 

SSE,RR,Adjust_RR=score(yvals,y,2)
print('RR: '+ str(RR) + '  ' +'Adjust_RR: '+ str(Adjust_RR)) 

mydata_label=pd.DataFrame({'R-squared':'R_squared: ' +str(round(RR,2)),'x':[-2],'y':[-1.3],
                           'Groupx':'Passive:Active','Groupy':'Plain: Gaudy'},index=[1])
label_data=label_data.append(mydata_label)

# #---------------------------------------Comprehensive Result-----------------------------------------
# x_col=['Heavy:Light', 'Passive:Active', 'Passive:Active', 'Cold:Warm', 'HMatch:EMatch']
# y_col=['Tense:Relaxed','Plain: Gaudy', 'Traditional:Modern', 'Masculine:Feminine','Dislike:Like']

# r_value, p_value=np.full(len(x_col),np.NAN),np.full(len(x_col),np.NAN)
# R_squared=[]
# for i in range(0,len(x_col)):
#     x=Mean_mydata_Total[x_col[i]].values
#     y=Mean_mydata_Total[y_col[i]].values
#     slope, intercept, r_value[i], p_value[i], std_err =stats.linregress(x,y)
#     print("r-squared:", r_value[i]**2 )
#     print('p_value: ' , p_value[i] )
#     yvals=intercept + slope*x
#     Sub_Fitting_data=pd.DataFrame({'Evaluation':y,'Fitting Value':yvals,'ID':np.array(range(0,len(y))),'Group':np.repeat(y_col[i],len(y))})
#     Fitting_data=Fitting_data.append(Sub_Fitting_data)
#     R_squared.append('R_squared: ' +str(round(r_value[i]**2,2)))
    
# #T_value_Fabric, P_value_Fabric=stats.ttest_ind(yvals, y, equal_var=True)#stats.f_oneway(x,y)#   
# mydata_label=pd.DataFrame({'R-squared':R_squared,'Group':y_col,'x':list(np.repeat(-2,len(y_col))),'y':list(np.repeat(-1.3,len(y_col)))})
# label_data=label_data.append(mydata_label) 
# #label_data['y'] = label_data['y'].convert_objects(convert_numeric=True)
# #label_data['x'] = label_data['x'].convert_objects(convert_numeric=True)
 

# #Fitting_data['Group']=Fitting_data['Group'].astype("category",categories=Colnames[4:],ordered=False)
# #label_data['Group']=label_data['Group'].astype("category",categories=Colnames[4:],ordered=False)

base_plot=(ggplot()
+geom_point(Fitting_data,aes('Evaluation','Fitting Value',fill='factor(ID)'),size=3,stroke=0.25,colour="black",show_legend=False)
#+geom_text(label_data,aes('x','y',label='R-squared'),size=10,ha='left',va='top',colour="black",nudge_x=0)
+scale_fill_manual(values=Color_theme,scales='free_x')   
+facet_wrap('~Group',nrow=1) 
+theme_matplotlib()
+theme(
    strip_text=element_text(size=15,face="plain",color="black"),
    strip_background=element_rect(colour='black'),
    #text=element_text(size=15,face="plain",color="black"),
    axis_title=element_text(size=18,face="plain",color="black"),
    axis_text = element_text(size=15,face="plain",color="black"),
    #legend_position='none',
    #legend_position = (0,0),
    figure_size = (18, 3),
    dpi = 150
))
print(base_plot)
# #base_plot.save('Grid_Fitting.pdf')  
