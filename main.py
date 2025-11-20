import streamlit as st
import pandas as pd

pages = {
    "Home": [
        st.Page("home.py", title="Home", icon="🏠")
    ],
    "Conoce los datos": [
        st.Page("pages/data.py", title="Datos de las tablas", icon="📊")
    ], 
    "Análisis de datos por estado": [
        st.Page("pages/clientesEstado.py", title="Clientes por estado", icon="👥"),
        st.Page("pages/graficoMedidasEstado.py", title="Gráfico por estado", icon="📈"),
        st.Page("pages/resenas.py", title="Análisis de reseñas", icon="⭐"),
        st.Page("pages/mapa.py", title="Mapa", icon="🌎")
    ],
    "Análisis de datos por ciudad": [
        st.Page("pages/clienteCiudad.py", title="Clientes por ciudad",  icon="👥"),
        st.Page("pages/graficoCiudad.py", title="Gráficos por ciudad", icon="📉")
    ]
}

pg = st.navigation(pages)
pg.run()
