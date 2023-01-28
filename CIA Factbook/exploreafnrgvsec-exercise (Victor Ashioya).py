#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats


# In[2]:


nrgvsecon=pd.read_csv("africanrgvsgdrp.csv",index_col=[0])
nrgvsecon.shape


# ### Electricity Generation Sources in each country

# We will start by seeing the different electricity generation sources in different countries

# In[3]:


nrgvsecon.head(5)


# In[4]:


import matplotlib as mpl

mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False


# In[5]:


nrgvsecon.iloc[0]


# We will use bar charts to compare different electricity generation sources.ie. `plt.bar()`

# In[6]:


x=nrgvsecon.iloc[0].index[4:]
y=nrgvsecon.iloc[0].values[4:]
orderedy=nrgvsecon.iloc[0].value_counts().index
plt.bar(x,y)
plt.xticks(rotation=90)
plt.ylim(0,100)


plt.show()


# We can see the comparisons of each electricity generation source in a country( in this case, Nigeria). 
# 
# Now, a better way to visualize this would be the bar charts in some order.e.g. the highest sources to the lowest.

# In[7]:


# argsort returns an array of indices in order ascending order
order=np.argsort(nrgvsecon.iloc[0].values[4:])


# In[8]:


# barh will plot a horizontal bar instead of a vertical one
x=nrgvsecon.iloc[0].index[4:][order]
y=nrgvsecon.iloc[0].values[4:][order]
orderedy=nrgvsecon.iloc[0].value_counts().index
fig=plt.barh(x,y)
plt.xticks(rotation=90)
plt.xlim(0,100)
plt.title(nrgvsecon['country'][0].upper())

plt.show()


# Another interesting and more clear way to do things would be to have the percent appear at the end of each bar. 
# 
# We can use `plt.text` to do this

# In[9]:


x=nrgvsecon.iloc[0].index[4:][order]
y=nrgvsecon.iloc[0].values[4:][order]
orderedy=nrgvsecon.iloc[0].value_counts().index
fig=plt.barh(x,y)
plt.xticks(rotation=90)
plt.xlim(0,100)
plt.xlabel("% from each source")
plt.title(nrgvsecon['country'][0].upper())
for i in range(len(y)):
    if y[i]!=0:
        plt.text(y[i]+1, i,f"{y[i]}%")

plt.show()


# In[10]:


# test
# nrgvsecon[nrgvsecon['country'].str.contains('kenya')].iloc[0][2:].index


# The information on this bar chart is really clear.
# 
# We can see what the percentage contribution from each electricity generation source is!
# 
# Let's create a function to get this information from any country.

# In[11]:


def plotpercountry(countries):
    for country in countries:
        order=np.argsort(nrgvsecon[nrgvsecon['country'].str.contains(country)].iloc[0].values[4:])
        y=nrgvsecon[nrgvsecon['country'].str.contains(country)].values[0][4:][order]
        x=nrgvsecon[nrgvsecon['country'].str.contains(country)].iloc[0][4:].index[order]
        plt.barh(x,y)
        plt.xlim(0,100)
        plt.xlabel("% from each source")
        plt.title(country.upper())
        for i in range(len(y)):
            if y[i]!=0:
                plt.text(y[i]+1, i,f"{y[i]}%")
        plt.show()
        


# In[12]:


plotpercountry(nrgvsecon.country.values[2:5])


# In[13]:


nrgvsecon.head(10)


# ### Comparing energy sources

# Now, we can compare the percentage of energy that Africa produces, and from which each source it comes from. 
# 
# Let's try do this using a pie chart, and a bar chart.

# In[14]:


# this find the sum of every column
nrgvsecon.sum(numeric_only=True)


# In[15]:


# the sum of the column- installed capacity
totalcapacity=nrgvsecon['installed capacity kW'].sum()


# In[16]:


# sum of energy produced by fossil fuels over the total energy produced, to find the percentage
(np.sum(nrgvsecon['installed capacity kW']*nrgvsecon['fossil fuels']/100))/(nrgvsecon['installed capacity kW'].sum())


# In[17]:


sources=['fossil fuels','biomass and waste','wind','solar','nuclear','hydroelectricity','geothermal']


# In[18]:


# a function to calculate totals from all sources
def sumcapacity(sources):
  capacities=[]
  for source in sources:
    capacities.append((np.sum(nrgvsecon['installed capacity kW']*nrgvsecon[source]/100))/totalcapacity)
  return capacities


# In[19]:


capas=(sumcapacity(sources))


# Let's create a [simple pie chart]("https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html").

# In[20]:


fig1, ax1 = plt.subplots()
ax1.pie(capas, labels=sources, autopct='%1.1f%%',
         startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.set_facecolor('lightgrey')
ax1.legend()

plt.show()


# We can clearly see that the highest percentages come from fossil fuels and hydroelectricity. 
# 
# One question to ask at this point would be whether gdp could still be correlated with electricity generation sources.
# 
# For clarity, let's do this again with a bar chart

# In[21]:


mpl.rcParams['axes.spines.top'] = True
mpl.rcParams['axes.spines.right'] = True
plt.barh(sources,(np.array(capas)*100))
plt.xlim(0,100)
for i in range(len(capas)):
    if capas[i]!=0:
        plt.text(capas[i]*100+1, i,f"{(capas[i]*100):.2f}%")
plt.show()


# ### gdp

# Can we draw some insights on where African gdp's per capita lie? We will use a histogram in this case: `plt.hist` and for seaborn `sns.displot`

# In[22]:


nrgvsecon.head()


# In[23]:


# np.log10(nrgvsecon['real gdp per capita $'].describe())


# In[24]:


# 10**np.arange(2.7,4.4+0.1,0.1)


# In[25]:


bins=10**np.arange(2.7,4.4+0.1,0.1)
ticks=[1000,3000,10000,30000]


# In[26]:


labels=[f'{v}' for v in ticks]
plt.hist(data = nrgvsecon, x='real gdp per capita $',bins=bins)
plt.xscale('log');
plt.xticks(ticks,labels);


# In[27]:


sns.displot(nrgvsecon['real gdp per capita $']);


# It looks like most African countries(more than half) have their real gpd per capita below $ 5000. 
# 
# What other questions might we have? Do countries with low gdp rely on fossil fuels? Again, is there a correlation between the two?

# In[28]:


nrgvsecon.sort_values('installed capacity kW').head()


# ## Assignment starts here

# We can find the correlation between two variables using `scipy.stats`. We imported this module at the beginning of the notebook. It contains functions that compute all the statistics for us! 
# 
# For example, let's see the [spearman rank correlation]("https://statistics.laerd.com/statistical-guides/spearmans-rank-order-correlation-statistical-guide.php") between installed capacity and gdp per capita. 
# 
# (This may seem like a lot of jargon, but basically, what the [function]("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html") will return is two numbers. The closer the first number(the correlation) is to 1 or -1, the more the variables are alike, otherwise, the closer it is to 0, the less the variables are alike)

# In[29]:


stats.spearmanr(nrgvsecon['installed capacity kW'],nrgvsecon['real gdp per capita $'])


# A correlation of 0.43 isn't a strong correlation. What if we plotted these two against each other?

# In[30]:


x=nrgvsecon['installed capacity kW']
y=nrgvsecon['real gdp per capita $']

plt.xlabel('energy capacity')
plt.ylabel('real gdp')
plt.scatter(x,y);


# From the scatterplot, would you say that a correlation exists?
# 
# From observations;
#    * Fewer countries with high energy capacity
#    * Countries with a higher GDP have little energy capacity
# 
# Hence no direct correlation between GDP and energy capacity

# ### Taking population to account

# The plot above almost clearly indicates that there is no/a very small correlation between **total energy produced** and **gdp per capita**. This is due to several factors. Some countries, such as Seychelles, have extremely high gdp per capita, due to their low population. The total energy capacity, however, doesn't take population into account. How can we do this, with the data we have, for every country?

# In[31]:


pop_energy_gdp = nrgvsecon[["population", "real gdp per capita $", "installed capacity kW"]]
pop_energy_gdp_corr = pop_energy_gdp.corr()
pop_energy_gdp_corr


# In[32]:


import seaborn as sns
sns.heatmap(pop_energy_gdp_corr);


# Can we find the correlation between the gdp per capita, and the variable that takes population into account? 
# 
# Hint: how did we do this above?(Apart from the spearman's rank correlation, try search for other ways to find correlation, and see how these fair.e.g.  [Pearson correlation]("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html"))

# In[33]:


sns.pairplot(pop_energy_gdp_corr);


# In[34]:


plt.plot(nrgvsecon["real gdp per capita $"], label="GDP")
plt.plot(nrgvsecon["population"], label="Population")
plt.title("GDP Per Capita $ v Population")
plt.legend();


# Can you plot the two variables against one another; gdp against the 'other variable'
# 
# Hint: We mentioned this in class
# 
# Remember to label the axis

# In[35]:


x=nrgvsecon['population']
y=nrgvsecon['real gdp per capita $']

plt.xlabel('Population')
plt.ylabel('GDP')
plt.scatter(x,y);


# Now, there are some outliers in our data, like South Africa, who produce a high amount of electricity, some of which goes to export, and Libya, who export a lot of fossil fuel despite their low population, causing high gdp per capita, among others.
# 
# Can we find a method to get rid of outliers like these? 
# 
# Create new variables, that remove the outliers' data, and see whether the correlation is stronger, or weaker.

# In[36]:


nrgvsecon.head()


# In[37]:


# Plotting boxplots for each of the numerical columns
sns.set_style('darkgrid')
fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (15, 10))
fig.suptitle('Box plots showing outliers', y= 0.93, fontsize = 15)

for ax, data, name in zip(axes.flatten(), nrgvsecon, ['population','real gdp per capita $', 
                                                      'installed capacity kW','fossil fuels', 'solar', 'nuclear',
                                                     'wind', 'hydroelectricity', 'tide and wave', 'geothermal',
                                                     'biomass and waste']):
    sns.boxplot(nrgvsecon[name], ax = ax)


# * All have outliers except "hydroelectricity", "tide and wave", "fossil fuels"

# In[38]:


# We will use Quantile Flooring and Capping
print(nrgvsecon["population"].quantile(0.10))
print(nrgvsecon["population"].quantile(0.90))


# In[39]:


nrgvsecon["population"].describe()


# In[40]:


nrgvsecon["population"] = np.where(nrgvsecon["population"]<1140407.1, 1140407.1, nrgvsecon["population"])
nrgvsecon["population"] = np.where(nrgvsecon["population"]>57351464.0, 57351464.0, nrgvsecon["population"])
# calculate the skewness
print(nrgvsecon["population"].skew())


# In[41]:


# Dropping the outlier data points
index = nrgvsecon[(nrgvsecon['population'] >= 2.250821e+08)|(nrgvsecon['population'] <= 9.701700e+04)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['population'].describe()


# In[42]:


print(nrgvsecon["real gdp per capita $"].quantile(0.10))
print(nrgvsecon["real gdp per capita $"].quantile(0.90))


# In[43]:


nrgvsecon["real gdp per capita $"].describe()


# In[44]:


nrgvsecon["real gdp per capita $"] = np.where(nrgvsecon["real gdp per capita $"]<1220.0, 1220.0, nrgvsecon["real gdp per capita $"])
nrgvsecon["real gdp per capita $"] = np.where(nrgvsecon["real gdp per capita $"]>11950.0, 11950.0, nrgvsecon["real gdp per capita $"])
# calculate the skewness
print(nrgvsecon["real gdp per capita $"].skew())


# In[45]:


# Dropping the outlier data points
index = nrgvsecon[(nrgvsecon['real gdp per capita $'] >= 24400.000000)|(nrgvsecon['real gdp per capita $'] <= 700.000000)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['real gdp per capita $'].describe()


# In[46]:


print(nrgvsecon["installed capacity kW"].quantile(0.10))
print(nrgvsecon["installed capacity kW"].quantile(0.90))


# In[47]:


nrgvsecon["installed capacity kW"].describe()


# In[48]:


nrgvsecon["installed capacity kW"] = np.where(nrgvsecon["installed capacity kW"]<87400.0, 87400.0, nrgvsecon["installed capacity kW"])
nrgvsecon["installed capacity kW"] = np.where(nrgvsecon["installed capacity kW"]>10198799.999999996, 10198799.999999996, nrgvsecon["installed capacity kW"])
# calculate the skewness
print(nrgvsecon["installed capacity kW"].skew())


# In[49]:


# Dropping the outlier data points
index = nrgvsecon[(nrgvsecon['installed capacity kW'] >= 6.272800e+07)|(nrgvsecon['installed capacity kW'] <= 2.800000e+04)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['installed capacity kW'].describe()


# In[50]:


print(nrgvsecon["solar"].quantile(0.10))
print(nrgvsecon["solar"].quantile(0.90))


# In[51]:


nrgvsecon["solar"].describe()


# In[52]:


nrgvsecon["solar"] = np.where(nrgvsecon["solar"]<0.0, 0.0, nrgvsecon["solar"])
nrgvsecon["solar"] = np.where(nrgvsecon["solar"]>4.559999999999998, 4.559999999999998, nrgvsecon["solar"])
# calculate the skewness
print(nrgvsecon["solar"].skew())


# In[53]:


# Dropping the outlier data points
index = nrgvsecon[(nrgvsecon['solar'] >= 8.100000)|(nrgvsecon['solar'] <= 0.000000)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['solar'].describe()


# In[54]:


print(nrgvsecon["wind"].quantile(0.10))
print(nrgvsecon["wind"].quantile(0.90))


# In[55]:


nrgvsecon["wind"].describe()


# In[56]:


nrgvsecon["wind"] = np.where(nrgvsecon["wind"]<0.0, 0.0, nrgvsecon["wind"])
nrgvsecon["wind"] = np.where(nrgvsecon["wind"]>3.3200000000000016, 3.3200000000000016, nrgvsecon["wind"])
# calculate the skewness
print(nrgvsecon["wind"].skew())


# In[57]:


index = nrgvsecon[(nrgvsecon['wind'] >= 17.800000)|(nrgvsecon['wind'] <= 0.000000)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['wind'].describe()


# In[58]:


print(nrgvsecon["biomass and waste"].quantile(0.10))
print(nrgvsecon["biomass and waste"].quantile(0.90))


# In[59]:


nrgvsecon["biomass and waste"].describe()


# In[60]:


nrgvsecon["biomass and waste"] = np.where(nrgvsecon["biomass and waste"]<0.0, 0.0, nrgvsecon["biomass and waste"])
nrgvsecon["biomass and waste"] = np.where(nrgvsecon["biomass and waste"]>2.2800000000000002, 2.2800000000000002, nrgvsecon["biomass and waste"])
# calculate the skewness
print(nrgvsecon["biomass and waste"].skew())


# In[61]:


index = nrgvsecon[(nrgvsecon['biomass and waste'] >=15.000000)|(nrgvsecon['biomass and waste'] <= 0.000000)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['biomass and waste'].describe()


# In[62]:


print(nrgvsecon["nuclear"].quantile(0.10))
print(nrgvsecon["nuclear"].quantile(0.90))


# In[63]:


nrgvsecon["nuclear"].describe()


# In[64]:


nrgvsecon["nuclear"] = np.where(nrgvsecon["nuclear"]<0.0, 0.0, nrgvsecon["nuclear"])
nrgvsecon["nuclear"] = np.where(nrgvsecon["nuclear"]>2.6, 2.6, nrgvsecon["nuclear"])
# calculate the skewness
print(nrgvsecon["nuclear"].skew())


# In[65]:


index = nrgvsecon[(nrgvsecon['nuclear'] >=5.200000)|(nrgvsecon['nuclear'] <= 0.000000)].index
nrgvsecon.drop(index, inplace=True)
nrgvsecon['nuclear'].describe()


# 
# print(nrgvsecon["population"].quantile(0.10))
# print(nrgvsecon["population"].quantile(0.10))
# print(nrgvsecon["population"].quantile(0.10))
# print(nrgvsecon["population"].quantile(0.10))

# Plot the new variables against one another. Remember to label the axis

# In[72]:


x=nrgvsecon['solar']
y=nrgvsecon['wind']

plt.xlabel('Population')
plt.ylabel('GDP')
plt.scatter(x,y);


# This should more/less be similar to the plot we saw for income vs energy use per person!
