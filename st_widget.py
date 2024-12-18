import streamlit as st
from matplotlib import image
from datetime import datetime, timedelta

page_config = {
    'page_title': 'hello',
    'page_icon': 'data/north_star.png',
    'layout':'wide',
    'initial_sidebar_state':'auto'
}

st.set_page_config(**page_config)

name = st.text_input('enter name -')
if st.button('Submit',key='submit_1'):
    st.write(f'Greetings: {name}')

message = st.text_area('enter address -')
if st.button('Submit',key='submit_2'):
    st.write(f'Address: {message}')

age = st.number_input('Enter Age',0,150)

date_from = st.date_input('Start Date', 
                          value="default_value_today", 
                          min_value=datetime.now()-timedelta(days=10), 
                          max_value=datetime.now()+timedelta(days=10), 
                          key=None, 
                          help='Format is Year/Month/Day', 
                          on_change=None, 
                          format="YYYY/MM/DD", 
                          disabled=False, 
                          label_visibility="visible")

date_to = st.date_input('End Date', 
                          value="default_value_today", 
                          min_value=datetime.now()-timedelta(days=10), 
                          max_value=datetime.now()+timedelta(days=10), 
                          key=None, 
                          help='Format is Year/Month/Day', 
                          on_change=None, 
                          format="YYYY/MM/DD", 
                          disabled=False, 
                          label_visibility="visible")

if date_to < date_from:
    st.error('End Date should be Equal or Greater Than Start Date!')

# Create a slider for the timeline from 0 to 24 hours
timeline_range = st.slider(
    'Select the hour of the day',
    #min_value=0,
    max_value=24,
    value=(5,22),  # Default value
    step=1,
    format="%d:00"
)

# Display the selected hour
st.write(f'Selected range: {timeline_range[0]}:00 to {timeline_range[1]}:00')

status = st.radio('Game On?', ('Yes','No'))
if status == 'Yes':
    st.success('Horray!')
else:
    st.error(':(')

if st.checkbox('Show/Hide'):
    st.text('Hello World!')

with st.expander('Hello'):
    st.info('World')

language = ['English','Dutch','German','French']
choice = st.selectbox('Language',language)
if choice:
    st.write(f'User speaks {choice}!')

nationality = ['UK','France','Germany','Holland']
nationality_choice = st.multiselect('Nationality',nationality,default='UK')
if nationality_choice:
    st.write(f'User nationality: {nationality_choice}!')

proficiency = ['excellent','good']
choice = st.checkbox('Proficiency',proficiency)

age = st.slider("Age",1,100,5)

color = st.select_slider('choose train',
                         options=['9301','9315','9450'])

st.image(image.imread('data/train.jpeg'))

st.video('https://www.youtube.com/watch?v=7kd4d1KOMAA&ab_channel=RajasthanTourism',
         format="video/mp4", 
         start_time=55, 
         subtitles=None, 
         end_time=None, 
         loop=False, 
         autoplay=False, 
         muted=False)