# ###################################################################################################
#  # Business Problem
# ##################################################################################################


# A gaming company wants to create level-based (persona) new customer definitions using some characteristics of its customers.
# Additionally, they aim to segment these new customer definitions and estimate how much,
# on average, new potential customers coming into these segments could contribute to the company.


# ###################################################################################################
# Persona.csv Dataset
# ##################################################################################################

# The dataset contains the prices of products sold by an international gaming company and
# some demographic information of the users who purchased these products.
# The dataset is composed of records generated for each sales transaction.
# In other words, the table is not denormalized.
# This means that a user with certain demographic characteristics may have made multiple purchases.


# ###################################################################################################
# # Variables
# ##################################################################################################

# SOURCE – The type of device the customer is connected to
# SEX – The gender of the customer
# COUNTRY – The country of the customer
# AGE – The age of the customer

# PRICE SOURCE SEX COUNTRY AGE
# 39 android male bra 17
# 39 android male bra 17
# 49 android male bra 17
# 29 android male tur 17
# 49 android male tur 17


# importing libraries and adjusting some settings
pd.set_option('display.max_column', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', '{:.2f}'.format)

import pandas as pd

# Read persona.csv file to start working on the data set and have a quick look

df = pd.read_csv('datasets/persona.csv')
df.info()

# Find the average earnings in the breakdown of COUNTRY, SOURCE, SEX, AGE and sort the output by price
# Save the new output to a new df called agg_df

agg_df = df.groupby(by=['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'}).sort_values(by='PRICE',ascending=False)

# Column names becomes index, so we need to fix the indexes

agg_df = agg_df.reset_index()

# Convert the variable AGE to a categorical variable and add to the dataframe with name AGE_CAT

bins_ = [0, 18, 23, 30, 40, agg_df['AGE'].max()]
labels_ = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df['AGE'].max())]

agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], labels=labels_, bins=bins_)


# Define new level based customers(personas)
agg_df['CUSTOMERS_LEVEL_BASED'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'AGE_CAT']].agg(lambda x: '_'.join(x), axis=1)

# Drop unnecessary columns
agg_df = agg_df[['CUSTOMERS_LEVEL_BASED', 'PRICE']]

# At the moment there are duplicate segments, need is to get rid of duplicates and deduplication of segments

agg_df = agg_df.groupby('CUSTOMERS_LEVEL_BASED').agg({'PRICE': 'mean'}).sort_values(by='PRICE', ascending=False)

# Column names becomes index, so we need to fix the indexes
agg_df = agg_df.reset_index()


# Separate new customers (personas) into segments.
agg_df['SEGMENT'] = pd.qcut(agg_df['PRICE'], 4, labels=['D', 'C', 'B', 'A'])

# Classify new customers and estimate how much revenue they can bring.
# for example:

agg_df['CUSTOMERS_LEVEL_BASED'] = agg_df['CUSTOMERS_LEVEL_BASED'].str.upper()

new_user = 'TUR_ANDROID_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]

new_user2 = 'FRA_IOS_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user2]

