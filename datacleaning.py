import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
data = pd.read_csv("SampleSuperstore.csv",encoding='ISO-8859-1')

# Check structure
print(data.shape)
print(data.info())

# Clean data
data.drop_duplicates(inplace=True)
data.dropna(inplace=True)

# Basic stats
print(data.describe())

# EDA
print(data['Category'].value_counts())
print(data['Region'].value_counts())

# Correlation
corr = data[['Sales', 'Profit', 'Discount', 'Quantity']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()

# Total Sales by Region
region_sales = data.groupby('Region')['Sales'].sum().sort_values(ascending=False)
px.bar(region_sales, x=region_sales.index, y=region_sales.values, title='Total Sales by Region').show()
