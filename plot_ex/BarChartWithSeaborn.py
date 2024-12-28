import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Sample Data
data = sns.load_dataset("titanic")

# Create the bar plot
plt.figure(figsize=(10,6))
sns.barplot(x='class', y='fare', data=data)
st.pyplot(plt)
