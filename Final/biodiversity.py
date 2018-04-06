
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[1]:


from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[2]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[3]:


print species.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[4]:


species.scientific_name.nunique()
# There are 5541 total species of animals and plants in the species df


# What are the different values of `category` in `species`?

# In[5]:


species.category.unique()
# it appears there are 7 total species, 5 animal species and 2 plant species


# What are the different values of `conservation_status`?

# In[6]:


species.conservation_status.unique()
# the values range from nan(null), which is assumed to be non-threatened, the rest are Species of Concern, Endangered, Threatened, In Recovery


# In[7]:


# most abundant species, group by
species_count = species.groupby(['category']).scientific_name.nunique().reset_index()
species_count


# In[45]:


species_endangeredthreatened = species[(species.conservation_status == 'Endangered') | (species.conservation_status == 'Threatened')]
species_endangeredthreatened


# In[8]:


category = 'Amphibian', 'Bird', 'Fish', 'Mammal', 'Nonvascular Plant', 'Reptile', 'Vascular Plant'
counts = [79, 488, 125, 176, 333, 78, 4262]

plt.figure(figsize=(10, 8))

plt.pie(counts, labels=category, autopct='%d%%')
plt.axis('equal')
plt.title("National Parks Species Count")

plt.savefig("NP_species_count.png")

plt.show()


# In[9]:


species_mammals = species[species.category == 'Mammal']
species_mammals.fillna('No Intervention', inplace=True)


# In[10]:


mammals_endangered = species_mammals[(species_mammals.conservation_status == "Endangered") | (species_mammals.conservation_status == 'Threatened')]
mammals_endangered


# In[11]:


mammals_soc = species_mammals[species_mammals.conservation_status == 'Species of Concern']
mammals_soc


# In[12]:


cons_status_mammals = species_mammals.groupby(['conservation_status']).scientific_name.nunique().reset_index()
cons_status_mammals
# need to look at why nunique provides a lower number than count


# In[13]:


mammal_status = 'Endangered', 'In Recovery', 'No Intervention', 'Species of Concern', 'Threatened'
counts = [6, 1, 146, 22, 2]

plt.figure(figsize=(10, 8))

plt.pie(counts, labels=mammal_status, autopct='%d%%')
plt.axis('equal')
plt.title("Mammal Population Conservation Status")

plt.savefig("Mammals_cons_status.png")

plt.show()


# In[ ]:





# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[14]:


species.groupby(['conservation_status']).scientific_name.nunique().reset_index()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[15]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[48]:


conservation_stat_counts = species.groupby(['conservation_status']).scientific_name.nunique().reset_index()
print conservation_stat_counts.head()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[17]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
print protection_counts


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[18]:


plt.figure(figsize=(10,4))
ax = plt.subplot()
           
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)       
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.savefig("Cons_status_x_Species.png")
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[19]:


species['is_protected'] = species.conservation_status.apply(lambda x: True if x != 'No Intervention' else False)
print species.head()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[20]:


category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[21]:


category_counts.head()


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[22]:


category_pivot = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index().pivot(columns='is_protected',
                                                                                                            index='category',
                                                                                                            values='scientific_name')


# Examine `category_pivot`.

# In[23]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[24]:


category_pivot.columns = ['not_protected', 'protected']
category_pivot.head()


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[25]:


category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)


# Examine `category_pivot`.

# In[26]:


category_pivot.head(10)


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[27]:


contingency = [[146, 30], [413, 75]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Paste the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[28]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[29]:


chi2, pval, dof, expected = chi2_contingency(contingency)
print pval


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[30]:


contingency2 = [[73, 5], [146, 30]]
chi2, pval, dof, expected = chi2_contingency(contingency2)
print pval


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# In[31]:


# is there a difference between fish and birds?
contingency3 = [[413, 75], [115, 11]]
chi2, pval, dof, expected = chi2_contingency(contingency3)
print pval


# Just outside of the range for significance but one that should be monitored.

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[32]:


observations = pd.read_csv('observations.csv')
observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[33]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[34]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[35]:


species['is_sheep'] = species.common_names.apply(lambda x: True if 'Sheep' in x else False)
species.head()


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[36]:


species[species.is_sheep]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[37]:


sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[38]:


sheep_observations = observations.merge(sheep_species)
sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[39]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[40]:


plt.figure(figsize=(16,4))
ax = plt.subplot()
           
plt.bar(range(len(obs_by_park)), obs_by_park.observations)       
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.savefig("Obs_Sheep_x_Week.png")
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[41]:


minimum_detectable_effect = 100 * (0.05 / 0.15)
print minimum_detectable_effect
baseline_conversion_rate = 15
significance = 0.90
sample_size = 510


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[42]:


Bryce_Park_obs = 250
Yellowstone_obs = 507

Bryce_Park_study = 510 / 250.0
Yellowstone_study = 510 / 507.0

print Bryce_Park_study
print Yellowstone_study
# The Bryce Park study would take just over 2 weeks and the Yellowstone Study would take approximately 1 week.


# In[43]:


# when I plugged the same numbers into the version on Codecademy, I got a sample size of 870 or 890 depending on the 33 vs. 33.3
# I got green checkmarks when I plugged those numbers in on section 15 of 16, but the results didn't match the explanation on
# the last slide. Wanted to note that here in case someone wants to look at that and try to repro. 
# I stuck with this version where the sample size was 510 because of how the solution was written as 2 weeks/Bryce and 1 week/Yellowstone

