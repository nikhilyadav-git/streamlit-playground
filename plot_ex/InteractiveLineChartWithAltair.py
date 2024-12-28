import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Sample Data
data = pd.DataFrame({
    'date': pd.date_range('20210101', periods=100),
    'value': (np.random.rand(100).cumsum())
})

# Altair Line Chart
chart = alt.Chart(data).mark_line().encode(
    x='date:T',
    y='value:Q'
).interactive()

st.altair_chart(chart, use_container_width=True)
