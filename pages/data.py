import streamlit as st
import pandas as pd

st.title("Datos importantes")

top5 = pd.read_csv("top_5_states.csv")
reviews = pd.read_csv("states_reviews.csv")
city = pd.read_csv("city_delay_orders.csv")

st.subheader("Medidas por estado")
st.dataframe(top5)
st.subheader("Media por review")
st.dataframe(reviews)
st.subheader("Días tardíos por ciudad")
st.dataframe(city.head(10))

st.write("")

col, colm = st.columns(2, vertical_alignment="center")
with col:
    st.page_link("main.py", label="Home", icon="⬅️")
with colm:
    st.page_link("pages/clientesEstado.py", label="Clientes por estado", icon="➡️")