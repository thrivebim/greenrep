import streamlit as st
import pandas as pd
import plotly as pio

st.set_page_config(
        page_title="BREEAM Reporter",
        page_icon="leaves",
        layout="wide")

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

with st.sidebar: st.caption(""":darkgrey[App made by car]""")

st.title('Green Report Tool')
st.write('This is a simple check-list and report export for Project with BREEAM or other sustainbility ratings.')
st.write("Please consider that the app doesn't warn about minimum requirements. Please consult BREEAM Official Documentation to verify you oblige to the minimum criterias.")
st.divider()
st.markdown("Disclaimer: This is not an official calculator for BREEAM and might present inaccuracies. \n The author doesn't have any right or role in BRE. The app is done based on author's knowledge, if you have any feeback or suggestion please send an email to xxxx")

st.caption('App made by car')

