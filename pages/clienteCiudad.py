import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer datos
df = pd.read_csv("orders_top_5_states.csv", parse_dates=['Order Purchase Timestamp'])
df['Order Purchase Timestamp'] = pd.to_datetime(df['Order Purchase Timestamp'])

# Rango completo
min_fecha = df['Order Purchase Timestamp'].min().date()
max_fecha = df['Order Purchase Timestamp'].max().date()

# Slider para rango de fechas
rango_fechas = st.slider(
    "Selecciona rango de fechas",
    min_value=min_fecha,
    max_value=max_fecha,
    value=(min_fecha, max_fecha),
    format="DD/MM/YYYY"
)

# Filtrar por rango
df_filtrado = df[
    (df['Order Purchase Timestamp'].dt.date >= rango_fechas[0]) &
    (df['Order Purchase Timestamp'].dt.date <= rango_fechas[1])
]

# Conteo por estado
conteo_estado = (
    df_filtrado.groupby('State')['Customer Unique Id']
    .nunique()
    .reset_index(name='Clientes totales')
)

# Selector de estado
estado_seleccionado = st.selectbox(
    "Selecciona un Estado para ver el número de clientes por ciudad",
    df_filtrado['State'].unique()
)

# Filtrar por estado
ciudades_estado = df_filtrado[df_filtrado['State'] == estado_seleccionado]

# Mostrar ciudades y conteo
conteo_ciudades = (
    ciudades_estado.groupby('City')['Customer Unique Id']
    .nunique()
    .reset_index(name='Clientes totales')
)

conteo_ciudades.rename(columns={'City': 'Ciudad'}, inplace=True)

st.subheader(f"Clientes por ciudad en {estado_seleccionado}")
st.dataframe(conteo_ciudades, hide_index=True)

st.write("")
st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="bottom")
with col:
    st.page_link("pages/mapa.py", label="Mapa", icon="⬅️")
with colm:
    st.page_link("pages/graficoCiudad.py", label="Gráficos por ciudad", icon="➡️")
