#!/usr/bin/env python
# coding: utf-8

# In[31]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[32]:


import numpy as np
import pandas as pd


# In[33]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[34]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[35]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[36]:


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# In[37]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[38]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[39]:


# Create our session (link) from Python to the DB
session = Session(engine)


# In[40]:


engine.execute('SELECT * FROM Station LIMIT 5').fetchall()


# In[41]:


engine.execute('SELECT * FROM Measurement LIMIT 5').fetchall()


# # Exploratory Climate Analysis

# In[42]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results

rec_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
print(rec_date)


# In[43]:


# Calculate the date 1 year ago from the last data point in the database
one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print(one_year_ago)


# In[44]:


# Perform a query to retrieve the data and precipitation scores
prcp_data = session.query(Measurement.date, Measurement.prcp).    filter(Measurement.date > one_year_ago).    order_by(Measurement.date).all()


# In[45]:


#save as dataframe and set index to date
prcp_data_df = pd.DataFrame(prcp_data)
prcp_data_df.head()


# In[46]:


#Sort the dataframe by date
prcp_data_df.set_index('date').head()


# In[47]:


# Use Pandas Plotting with Matplotlib to plot the data

ax = prcp_data_df.plot(figsize=(8,4))
ax.set_title("Precipitation Analysis (8/24/16 to 8/23/17)")
ax.set_ylabel('frequency')
plt.show()


# In[48]:


# Use Pandas to calcualte the summary statistics for the precipitation data
prcp_data_df.describe()


# In[49]:


# Design a query to show how many stations are available in this dataset?
locations = session.query(Measurement).group_by(Measurement.station).count()
print("There are {} stations available.".format(locations))


# In[63]:


# What are the most active stations? (i.e. what stations have the most rows)?
active = session.query(Measurement.station, func.count(Measurement.station)).            group_by(Measurement.station).            order_by(func.count(Measurement.station).desc()).all()
active


# In[67]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station? 

most_active = active[0][0]
session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).                filter(Measurement.station == most_active).all()


# In[70]:


# Choose the station with the highest number of temperature observations.
temp = session.query(Measurement.station, Measurement.tobs).                filter(Measurement.station == most_active).                filter(Measurement.date >= one_year_ago).all()
tobs_df = pd.DataFrame(temp)
tobs_df.set_index('station', inplace=True)
tobs_df.head()


# In[71]:


# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
temp_obs = session.query(Measurement.tobs).                                filter(Measurement.station==most_active).                                filter(Measurement.date >= one_year_ago).                                order_by(Measurement.date.desc()).all()
temp_obs_df = pd.DataFrame(temp_obs)
temp_obs_df.head()


# 
