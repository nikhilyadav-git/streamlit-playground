import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Sample Data
data = sns.load_dataset("tips")

# Create the boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x="day", y="total_bill", data=data)
st.pyplot(plt)
