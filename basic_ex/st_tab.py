import streamlit as st

# Create tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

# Content for Tab 1
with tab1:
    st.header("Welcome to Tab 1")
    st.write("This is the content of the first tab.")

# Content for Tab 2
with tab2:
    st.header("Welcome to Tab 2")
    st.write("This is the content of the second tab.")

# Content for Tab 3
with tab3:
    st.header("Welcome to Tab 3")
    st.write("This is the content of the third tab.")
