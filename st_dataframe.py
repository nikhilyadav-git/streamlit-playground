import streamlit as st
import pandas as pd

df = pd.read_csv('data/food.csv')

#st.dataframe(df)

st.dataframe(df.style.highlight_max(axis=0))
# st.table(df)

st.json({'hello':'world'})

test_code = """
print('Hello World!')
"""
st.code(test_code)