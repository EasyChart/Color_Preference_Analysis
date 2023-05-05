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

#base_plot.save('Color_theme.pdf')  
#---------------------------------------------------------------------------------------------
file = open('Shirts.csv')
mydata=pd.read_csv(file,encoding = "utf-8")

Colnames=mydata.columns.values.tolist()

#------------------------------male-------------------------------------------
Mean_mydata_Total=mydata[mydata['Gender']=='男'].groupby('Group').mean()#[(mydata['Job']=='颜色科学') | (mydata['Job']=='服装设计')]
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
for i in range(0,len(Colnames)): 
    for j in range(0,len(Colnames)):
        Sub_data['y']=Mean_mydata_Total[Colnames[i]].copy()
        if i>=j:
            if i!=j :
                Sub_data['x']=Mean_mydata_Total[ Colnames[j]]
                Sub_data['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
                Sub_data['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
                Sub_data['ID']=list(range(0,len(Mean_mydata_Total)))
         
                data_Corr=Sub_data.loc[:,['x','y']].corr()    
                list_corr.append('R: ' +str(round(data_Corr.values[0][1],2)))
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
                        if (x>=division[h]) & (x<=division[h]+0.2):
                            xx=division[h].copy()
                            if (division[h]<-2):
                                xx=-2
                            elif (division[h]>2):
                                xx=2
                            Hist_x.append(xx+0.2)
                            Hist_y.append((Record_count[0,h].copy())*0.35-2)
                            Record_count[0,h]=Record_count[0,h]+1
                Sub_data['y']=list(Hist_y.copy())
                Sub_data['x']=list(Hist_x.copy()) 
            
            Sub_data['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
            Sub_data['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
            Sub_data['ID']=list(range(0,len(Mean_mydata_Total)))
         
            df_data=df_data.append(Sub_data)

cat_type = CategoricalDtype(categories= np.array(Colnames), ordered=False)
df_data['Group1']=df_data['Group1'].astype(cat_type)
df_data['Group2']=df_data['Group2'].astype(cat_type)

mydata_label2=pd.DataFrame(columns=['Corr','Group1','Group2','x','y'])
mydata_label2['Corr']=list_corr
mydata_label2['Group1']=pd.Categorical(Group1, categories=Colnames,ordered=False)
mydata_label2['Group2']=pd.Categorical(Group2, categories=Colnames,ordered=False)
mydata_label2['x']=-1.8
mydata_label2['y']=-1.4
     
#--------------------------------Female-------------------------------------------
Mean_mydata_Total=mydata[mydata['Gender']=='女'].groupby('Group').mean()#[(mydata['Job']=='颜色科学') | (mydata['Job']=='服装设计')]
#Mean_mydata_Total=Mean_mydata_Total.set_index('Group')

Mean_mydata_Total=pd.merge(Mean_mydata_Total,Color_mydata,left_index=True,right_index=True)
Colnames=Mean_mydata_Total.columns.values.tolist()[:11] 
# =============================================================================
df_data_female  = pd.DataFrame(columns=['x','y','Group1','Group2','ID'])
Sub_data2 = pd.DataFrame(columns=['x','y','Group1','Group2','ID'])
list_corr=[]
Group1=[]
Group2=[]
Step=0.2
for i in range(0,len(Colnames)): 
    for j in range(0,len(Colnames)):
        Sub_data2['y']=Mean_mydata_Total[Colnames[i]].copy()
        if i<=j:
            if i!=j :
                Sub_data2['x']=Mean_mydata_Total[ Colnames[j]]
                Sub_data2['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
                Sub_data2['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
                Sub_data2['ID']=list(range(0,len(Mean_mydata_Total)))
         
                data_Corr=Sub_data2.loc[:,['x','y']].corr()    
                list_corr.append('R: ' +str(round(data_Corr.values[0][1],2)))
                Group1.append(Colnames[i])
                Group2.append(Colnames[j])
            else:
                #count, division = np.histogram(Sub_data['y'], bins =np.arange(-2,2,0.2)) 
                division= np.arange(-2,2.1,0.2)
                Hist_x=[]
                Hist_y=[]
                Record_count=np.ones([1,len(division)])
                for k in range(0,len(Sub_data2['y'])):
                    x=Sub_data2['y'][k]
                    if (x<-2): x=-2
                    if (x>2.1): x=2
                    for h in range(0,len(division)):
                        if (x>=division[h]) & (x<=division[h]+0.2):
                            xx=division[h].copy()
                            if (division[h]<-2):
                                xx=-2
                            elif (division[h]>2):
                                xx=2
                            Hist_x.append(xx+0.2)
                            Hist_y.append((Record_count[0,h].copy())*0.35-2)
                            Record_count[0,h]=Record_count[0,h]+1
                Sub_data2['y']=list(Hist_y.copy())
                Sub_data2['x']=list(Hist_x.copy()) 
            
            Sub_data2['Group1']=np.repeat(Colnames[i],len(Mean_mydata_Total))
            Sub_data2['Group2']=np.repeat(Colnames[j],len(Mean_mydata_Total))
            Sub_data2['ID']=list(range(0,len(Mean_mydata_Total)))
         
            df_data_female=df_data_female.append(Sub_data2)

cat_type = CategoricalDtype(categories= np.array(Colnames), ordered=False)
df_data_female['Group1']=df_data_female['Group1'].astype(cat_type)
df_data_female['Group2']=df_data_female['Group2'].astype(cat_type)

mydata_label_female=pd.DataFrame(columns=['Corr','Group1','Group2','x','y'])
mydata_label_female['Corr']=list_corr
mydata_label_female['Group1']=pd.Categorical(Group1, categories=Colnames,ordered=False)
mydata_label_female['Group2']=pd.Categorical(Group2, categories=Colnames,ordered=False)
mydata_label_female['x']=-1.8
mydata_label_female['y']=-1.4


#--------------------------------Display-------------------------------------------
df_data['Gender']="Male"
df_data_female['Gender']="Female"
df_data_Display=df_data.append(df_data_female)

base_plot=(ggplot() 
#其气泡的颜色填充由Class映射，大小由age映射
+geom_point(df_data_Display, aes(x = 'x', y = 'y',fill="Gender",),colour= 'black',stroke=0.25,size=4,alpha=0.8,show_legend=True) 
#+geom_point(df_data_female, aes(x = 'x', y = 'y'),colour= 'black',fill="#FD2D8B",stroke=0.25,size=4,alpha=0.8,show_legend=True) 
#+geom_point(df_data, aes(x = 'x', y = 'y'),colour="black",fill="#00B0F0",stroke=0.25,size=4,alpha=0.8,show_legend=True) 
#设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
+geom_text(mydata_label2,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
+geom_text(mydata_label_female,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
+scale_fill_manual(values=("#FD2D8B","#00B0F0"))                          
+facet_grid( 'Group1~ Group2',scales='fixed')  #类别Class为列变量,
+ylim(-2,2)
+xlim(-2,2)
+theme_matplotlib()
+theme(
    #text=element_text(size=15,face="plain",color="black"),
    axis_title=element_text(size=12,face="plain",color="black"),
    axis_text = element_text(size=14,face="plain",color="black"),
    strip_text=element_text(size=12,face="plain",color="black"),
    strip_background=element_blank(),
     legend_title=element_text(size=16,face="plain",color="black"),
     legend_text=element_text(size=15,face="plain",color="black"),
    legend_position='top',
    #legend_position = c(0.88,0.88),
    figure_size = (20, 20),
    dpi = 50
))
print(base_plot)        
base_plot.save('Figure_11_Gender_Analysis.pdf')   

# =============================================================================
# #--------------------------------Display-------------------------------------------
#           
# base_plot=(ggplot() 
# #其气泡的颜色填充由Class映射，大小由age映射
# +geom_point(df_data_female, aes(x = 'x', y = 'y',fill= 'factor(ID)'),colour= 'black',stroke=0.25,size=4,alpha=0.8,show_legend=True) 
# 
# +geom_point(df_data, aes(x = 'x', y = 'y',fill= 'factor(ID)'),colour="black",stroke=0.25,size=4,alpha=0.8,show_legend=True) 
# #设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
# +geom_text(mydata_label2,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
# +geom_text(mydata_label_female,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
# +scale_fill_manual(values=Color_theme)                          
# +facet_grid( 'Group1~ Group2',scales='fixed')  #类别Class为列变量,
# +ylim(-2,2)
# +xlim(-2,2)
# +theme_matplotlib()
# +theme(
#     #text=element_text(size=15,face="plain",color="black"),
#     axis_title=element_text(size=12,face="plain",color="black"),
#     axis_text = element_text(size=14,face="plain",color="black"),
#     strip_text=element_text(size=12,face="plain",color="black"),
#     strip_background=element_blank(),
#     #legend_position='none',
#     #legend_position = c(0.88,0.88),
#     figure_size = (20, 20),
#     dpi = 50
# ))
# print(base_plot)        
# base_plot.save('gender_Grid_Corr2.pdf') 
# =============================================================================

##--------------------------------Display-------------------------------------------
#          
#base_plot=(ggplot() 
##其气泡的颜色填充由Class映射，大小由age映射
#+geom_point(df_data_female, aes(x = 'x', y = 'y', fill= 'factor(ID)'),colour="black",stroke=0.25,alpha=1,size=3,show_legend=False) 
#
#+geom_point(df_data, aes(x = 'x', y = 'y', fill= 'factor(ID)'),colour="black",stroke=0.25,alpha=1,size=3,show_legend=False) 
##设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
#+geom_text(mydata_label2,aes('x','y',label='Corr'),size=12,ha='left',va='top',colour="black")
#+scale_fill_manual(values=Color_theme)                          
#+facet_grid( 'Group1~ Group2',scales='fixed')  #类别Class为列变量,
#+ylim(-1.5,1.5)
#+xlim(-1.5,1.5)
#+theme_matplotlib()
#+theme(
#    #text=element_text(size=15,face="plain",color="black"),
#    axis_title=element_text(size=12,face="plain",color="black"),
#    axis_text = element_text(size=14,face="plain",color="black"),
#    strip_text=element_text(size=12,face="plain",color="black"),
#    strip_background=element_blank(),
#    #legend_position='none',
#    #legend_position = c(0.88,0.88),
#    figure_size = (20, 20),
#    dpi = 50
#))
#print(base_plot)        
##base_plot.save('Grid_Corr.pdf')   