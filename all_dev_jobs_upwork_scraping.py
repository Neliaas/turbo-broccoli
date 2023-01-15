#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 13:55:03 2021

@author: vangogh
"""

# install packages
import upwork
from upwork.routers.jobs import search
import pandas as pd
import numpy as np
import os
import datetime

# change working directory
os.getcwd()
os.chdir('C:\\Users\\nelya\\Desktop\\python\\results')

# set configs
config = {"consumer_key": "ad3bc7d04689531b9f93db64d10b8bf4",
          "consumer_secret": "86a7cd499236dc26", 
          "access_token": "ec74301040a84f76e1a39781cfbcaa97",
          "access_token_secret": "53ed79ef4129a0b6"}

config = upwork.Config(config)

# initialize the client
client = upwork.Client(config)

# SCRAPING

# Create paging variables automatically
pages = []

for i in np.arange(0, 5100, 100):
    pages.append(str(i) + ";" + str(i+100))
   
# Create a list of subcategories  and job types   
subcat = ['Other - Software Development',
                 'Scripts & Utilities', 'Desktop Software Development', 
                 'Game Development', 'QA & Testing', 'Product Management'] 

subcat_jt =  ['Mobile Development', 
                 'Ecommerce Development', 'Web & Mobile Design']

jt = ['hourly', 'fixed']  

client_hires = ['1-3', '4-10', '11-40', '40-']
    
# LOOP 1: Web Dev subcategory by    
data_1 = []

for i in pages:
    for j in client_hires:
        params = {'q': 'development', 'paging': i, 'category2': 'Web, Mobile & Software Dev',
              'subcategory2': 'Web Development', 'client_hires': j}
        data = search.Api(client).find(params) 
        for z in data['jobs']: 
            data_1.append(z)
            
df_1 = pd.DataFrame(data_1)

# LOOP 2
data_2 = []

for i in pages:
    for j in jt:
        params = {'q': 'development', 'paging': i, 'category2': 'Web, Mobile & Software Dev',
              'subcategory2': 'Web Development', 'client_hires': '0', 'job_type': j }
        data = search.Api(client).find(params) 
        for z in data['jobs']: 
            data_2.append(z)
        
df_2 = pd.DataFrame(data_2)

# LOOP 3
data_3 = []

for i in pages:
    for j in subcat_jt:
        for m in jt:
            params = {'q': 'development', 'paging': i, 'category2': 'Web, Mobile & Software Dev',
              'subcategory2': j, 'job_type': m }
            data = search.Api(client).find(params) 
            for z in data['jobs']: 
                data_3.append(z)
        
df_3 = pd.DataFrame(data_3)

# LOOP 4
data_4 = []

for i in pages:
    for j in subcat:
        params = {'q': 'development', 'paging': i, 'category2': 'Web, Mobile & Software Dev',
              'subcategory2': j}
        data = search.Api(client).find(params) 
        for z in data['jobs']: 
            data_4.append(z)
        
df_4 = pd.DataFrame(data_4)

# Final df
df = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)

##### ANALYZE, EDA

# What are our jobs subcategories? How cat and subcat relate?
df.category2.value_counts()
df.subcategory2.value_counts()

# Job Status?
df.job_status.value_counts()


# Now let's have a look at the required skills distribution
skills = np.concatenate(df['skills'].values)
unique, counts = np.unique(skills, return_counts=True)
skills_distr = pd.DataFrame({"skills": unique, "counts": counts})
skills_distr = skills_distr.sort_values(by=['counts'], ascending=False)

skills_distr.to_csv(f'skills_{datetime.date.today()}.csv')


# Skills versus Date Posted 
# Split dataframe by number of weeks since posted 'less than a week',
# 'more than 1 week, less than 2 weeks', etc
df['date'] = pd.to_datetime(df.date_created, format='%Y-%m-%d')

# Finally, explode a column of dictionaries with client info
df_final = pd.concat([df.drop(['client'], axis=1), df['client'].apply(pd.Series)], axis=1)

df_final.to_csv(f'jobs_{datetime.date.today()}.csv')


