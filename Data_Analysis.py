#!/usr/bin/env python
# coding: utf-8

# # Importing all the required libraries 

# In[1]:


import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams["figure.figsize"] = (20,10)

import plotly.express as px

import seaborn as sns


# # Reading the data

# In[2]:


df = pd.read_csv('data_sets/prop_data_clean.csv')


# In[3]:


df.head(3)


# # Getting the shape of the data

# In[4]:


df.shape


# # Checking for null columns

# In[5]:


df.isnull().sum()


# In[6]:


df1 = df.copy()


# # Removing all the unwanted columns

# In[7]:


df1 = df.drop(['city', 'desc', 'floor_count', 'floor_num', 'id', 'id_string', 'latitude', 'longitude', 'poster_name', 'project', 'title', 'trans', 'url'], axis='columns')

df1.head()


# # Removing all the null values from the table

# In[8]:


df1.isnull().sum()


# In[9]:


df2 = df1.copy()


# In[10]:


df2 = df1.dropna()
df2.isnull().sum()


# In[11]:


df2.shape


# # Verifying the table

# In[12]:


df2.head()


# #### Creating columns for 'year date' and 'month' from the post_date column

# In[13]:


df2['year_posted'] = df2['post_date'].apply(lambda x: x.split('-')[0])


# In[14]:


df2['month_posted'] = df2['post_date'].apply(lambda x: x.split('-')[1])


# In[15]:


df2.head(5)


# # Deleting the post date column

# In[16]:


df2.drop(['post_date'], axis='columns')


# # Describing the table to know mean, sd

# In[17]:


df2.describe()


# # Removing outliers

# In[18]:


Q1 = df2.price.quantile(0.25)
Q3 = df2.price.quantile(0.75)

Q1, Q3


# In[19]:


IQR = Q3 - Q1
IQR


# In[20]:


lower_limit = Q1 - 1.5*(IQR)
upper_limit = Q1 + 1.5*(IQR)

lower_limit, upper_limit


# In[21]:


df3 = df2[(df2.price>lower_limit)&(df2.price<upper_limit)]


# # Histogram for area 

# In[22]:


df3.area.hist()


# # Making box plot for the price column

# In[23]:


df3.boxplot(column='price')
plt.show()


# # Distribution plot for price

# In[24]:


sns.distplot(df3['price'])


# # Counter Plot for Total Number of User_Type
# 
# From the below counter plot, It was found that Agent highest number and acts as a middle person for renting houses. 

# In[25]:


sns.countplot(x='user_type', data=df3)


# ## Count plot for Number of houses posted for the past 2 years
# 
# The Year 2020 has the highest number of houses for rent with count above 8000.

# In[26]:


sns.countplot(x='year_posted', data=df3)


# # Joint plot to display relationship between two variable Area and Price

# In[27]:


sns.jointplot(x='area', y='price', data=df3, kind='reg')


# # Pair plot to get the pair wise relationship from the dataset.

# In[28]:


sns.pairplot(df3, hue='user_type')


# # Creating a heatmap to find the correlation between variables

# In[29]:


sns.heatmap(df3.corr(), annot=True)


# # Creating Bar Graph for localities with total prices
# 
# Credit/Resource: https://www.kaggle.com/shreekant009/mumbai-house-price-with-plotly

# In[30]:


mumbai = df3.groupby(['locality','price'])['area'].sum().reset_index().sort_values('price',ascending =False)
fig = px.bar(df3[:700], y='area', x='locality', color='price', height=600)

fig.update_layout(
    title='Houses For Rent In Mumbai')

fig.show()


# # Treemap for the listed properties for Rent
# 
# Credit/Resource: https://www.kaggle.com/shreekant009/mumbai-house-price-with-plotly

# In[31]:


df3['price'] = df3['price'].astype(float)
df3['bedroom_num'] = df3['bedroom_num'].astype(float)

fig = px.treemap(df3, path=['locality','area','price','bedroom_num'], color='locality')
fig.update_layout(
    title='Properties For Rent')
fig.show()


# # Bar Chart for House for Rent
# 
# Credit/Resource: https://www.kaggle.com/shreekant009/mumbai-house-price-with-plotly

# In[32]:


rent = df3.sort_values('price',ascending=False).head(100)
fig = px.bar(rent, x='locality', y='price', color='price', height=500, hover_data=['price','area','bedroom_num'])
fig.update_layout(
    title='Houses For Rent')
fig.show()


# # Box Plot for Number of Bedroom 
# 
# Credit/Resource: https://www.kaggle.com/shreekant009/mumbai-house-price-with-plotly

# In[33]:


fig = px.box(df3, x="bedroom_num", y="price")
fig.update_layout(
    title='Bedroom Wise House Price Rents')
fig.show()


# # Scatter Plot
# 
# Credit/Resource: https://www.youtube.com/watch?v=cbqZa_1vzcg&list=PLeo1K3hjS3uu7clOTtwsp94PcHbzqpAdg&index=5&t=0s

# In[34]:


def scatter_chart(df,locality):
    bhk2 = df3[(df3.locality==locality) & (df3.bedroom_num==2)]
    bhk3 = df3[(df3.locality==locality) & (df3.bedroom_num==3)]
    matplotlib.rcParams['figure.figsize'] = (15,10)
    plt.scatter(bhk2.area,bhk2.price,color='blue',label='2 BHK', s=50)
    plt.scatter(bhk3.area,bhk3.price,marker='+', color='green',label='3 BHK', s=50)
    plt.xlabel("Total Area")
    plt.ylabel("Price Per Thousand Indian Rupees")
    plt.title(locality)
    plt.legend()
    
scatter_chart(df3,"Andheri East")


# In[35]:


cleaned_data = df3.to_csv('data_sets/cleaned_data.csv', index=False)

