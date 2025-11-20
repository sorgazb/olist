import streamlit as st

pages = {
    "Home": [
        st.Page("main.py", title="Home", icon="🏠")
    ],
    "Conoce los datos": [
        st.Page("./pages/data.py", title="Datos de las tablas", icon="📊")
    ], 
    "Análisis de datos por estado": [
        st.Page("./estado/clientesEstado.py", title="Clientes por estado", icon="👥"),
        st.Page("./estado/graficoMedidasEstado.py", title="Gráfico por estado", icon="📈"),
        st.Page("./estado/resenas.py", title="Análisis de reseñas", icon="⭐"),
        st.Page("./estado/mapa.py", title="Mapa", icon="🌎")
    ],
    "Análisis de datos por ciudad": [
        st.Page("./ciudad/clienteCiudad.py", title="Clientes por ciudad",  icon="👥"),
        st.Page("./ciudad/graficoCiudad.py", title="Gráficos por ciudad", icon="📉")
    ]
}

pg = st.navigation(pages)
pg.run()

