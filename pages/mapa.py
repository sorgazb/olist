import streamlit as st

st.image("mapa_entregas_retraso.png")
st.image("mapa_entregas_totales.png")

st.write("")
st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="bottom")
with col:
    st.page_link("./estado/resenas.py", label="Análisis de reseñas", icon="⬅️")
with colm:
    st.page_link("./ciudad/clienteCiudad.py", label="Clientes por ciudad", icon="➡️")