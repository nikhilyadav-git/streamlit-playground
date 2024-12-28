import streamlit as st
import plotly.express as px
import pandas as pd

# Sample animated data
df = pd.DataFrame({
    "Year": [2000, 2001, 2002, 2003, 2004],
    "Value": [10, 11, 12, 14, 13],
    "Category": ["A", "B", "C", "A", "B"]
})

fig = px.bar(df, x='Year', y='Value', animation_frame='Year', color='Category', title="Animated Bar Plot")

st.plotly_chart(fig)
