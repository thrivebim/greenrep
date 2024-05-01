import streamlit as st
import plotly as px
import pandas as pd
import altair as alt

st.set_page_config(
        page_title="BREEAM UK",
        page_icon="leaves",
        layout="wide",
    )

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

with st.sidebar: st.caption(""":darkgrey[App made by car]""")
st.subheader("BREEAM UK - New Projects")
st.write("Scroll through each section of the certification checklist and then check the score in the Rating tab")
st.caption("WIP - Section in development")