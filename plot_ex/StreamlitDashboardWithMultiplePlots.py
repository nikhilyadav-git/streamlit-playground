import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Titanic dataset from seaborn
data = sns.load_dataset("titanic")

# Creating multiple subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Plot 1: Age distribution
sns.histplot(data['age'].dropna(), kde=True, ax=ax1)
ax1.set_title("Age Distribution")

# Plot 2: Fare by Class
sns.barplot(x='class', y='fare', data=data, ax=ax2)
ax2.set_title("Fare by Class")

# Display the plots in Streamlit
st.pyplot(fig)
