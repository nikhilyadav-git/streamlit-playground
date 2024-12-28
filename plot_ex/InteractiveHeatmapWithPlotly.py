import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Generate random data for the heatmap
data = np.random.rand(10, 10)
fig = px.imshow(data, color_continuous_scale='Viridis', labels={'x': 'Feature', 'y': 'Feature'})

st.plotly_chart(fig)