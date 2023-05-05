# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 10:59:03 2019

@author: Jie Zhang
"""

import math
import re  
import os
import pandas as pd
import numpy as np
#from plotnine import *
#from plotnine.data import *
#import matplotlib.pyplot as plt 
#import scipy.stats as stats
#from scipy.optimize import curve_fit 
#from colormath.color_objects import sRGBColor, LCHabColor
#from colormath.color_conversions import convert_color

import itertools
def expandgrid(*itrs):
    product = list(itertools.product(*itrs))
    return {'Var{}'.format(i+1):[x[i] for x in product] for i in range(len(itrs))}
C = np.arange(0,100,0.5)
H = np.arange(0,360,2)
#C = np.arange(0,101,5)
#H = np.arange(0,361,15)
df_grid=pd.DataFrame(expandgrid(C, H))
df_grid.columns=['C','H']
df_grid['L']=25

def func_Heavy_Light(X,a=-1.908,b=0.023,c=0.017):
    x,y = X
    return a+b*x+c*y

def func_Passive_Active(X,a=-2.074,b=0.053):
    x = X
    return a+b*x

def func_Cold_Warm(X,a=-0.015,b=0.102,c=0.603,d=42.714):
    x,y = X
    return a+b*pow(x,c)*np.cos((y-d)/180*math.pi)


def func_Plain_Splendid(X,a=-0.029,b=0.475):
    x = X
    return a+b*x

def func_Like_Dislike(X,a=-0.101,b=0.714):
    x = X
    return a+b*x
#---------------------------Female Colors--------------------
def func_FatL_SlimL(X,a=-0.116,b=-0.332,c=-0.110,d=-0.185):
    x,y,z = X
    return a+b*x+c*y+d*z

    
def func_HMatch_EMatch_Female(X,a=-0.351,b=0.712,c=-0.091,d=-0.185):
    x,y = X
    return a+b*x+c*y+d*y*y  

HL=func_Heavy_Light((df_grid['L'].values,df_grid['C'].values)) 
PA=func_Passive_Active(df_grid['C'].values) 
CW=func_Cold_Warm((df_grid['C'].values,df_grid['H'].values)) 
PS=func_Plain_Splendid(PA) 
FS_female=func_FatL_SlimL((HL,PA,CW))
HE_female=func_HMatch_EMatch_Female((FS_female,PS))
df_grid['DL_female']=func_Like_Dislike(HE_female)

#array_LCH=df_grid.apply(lambda x: LCHabColor(x['L'], x['C'], x['H']), axis=1)
#array_rgb = array_LCH.map(lambda x:convert_color(x, sRGBColor))

#def rgb_to_hex(rgb):
#    return '%02x%02x%02x' % rgb
#df_grid['hex'] = array_rgb.apply(lambda x:rgb_to_hex((int(x.rgb_r*255),int(x.rgb_g*255),int(x.rgb_b*255))))
#df_grid['hex'] = array_rgb.apply(lambda x: x.get_rgb_hex())
#df_grid.to_csv('LCH_L80_Female2.csv',index=False,header=True,encoding = "gb18030")

#---------------------------Female Colors--------------------
def func_Masculine_Feminine(X,a=-0.155,b=0.126,c=0.252,d=0.449):
    x,y,z = X
    return a+b*x+c*y+d*z

    
def func_HMatch_EMatch_Male(X,a=-0.038,b=-0.203,c=-0.398,d=-0.099):
    x,y = X
    return a+b*x+c*y+d*y*y  

HL=func_Heavy_Light((df_grid['L'].values,df_grid['C'].values)) 
PA=func_Passive_Active(df_grid['C'].values) 
CW=func_Cold_Warm((df_grid['C'].values,df_grid['H'].values)) 
PS=func_Plain_Splendid(PA) 
FS_male=func_Masculine_Feminine((HL,PA,CW))
HE_male=func_HMatch_EMatch_Male((FS_male,PS))
df_grid['DL_male']=func_Like_Dislike(HE_male)

#array_LCH=df_grid.apply(lambda x: LCHabColor(x['L'], x['C'], x['H']), axis=1)
#array_rgb = array_LCH.map(lambda x:convert_color(x, sRGBColor))

#def rgb_to_hex(rgb):
#    return '%02x%02x%02x' % rgb
#df_grid['hex'] = array_rgb.apply(lambda x:rgb_to_hex((int(x.rgb_r*255),int(x.rgb_g*255),int(x.rgb_b*255))))
#df_grid['hex'] = array_rgb.apply(lambda x: x.get_rgb_hex())
#df_grid.to_csv('LCH_L25.csv',index=False,header=True,encoding = "gb18030")

