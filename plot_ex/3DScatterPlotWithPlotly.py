import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Sample Data
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'z': np.random.rand(100),
    'label': np.random.choice(['A', 'B', 'C'], size=100)
})

# 3D Scatter Plot
fig = px.scatter_3d(df, x='x', y='y', z='z', color='label')
st.plotly_chart(fig)
