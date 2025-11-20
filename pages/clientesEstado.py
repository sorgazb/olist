import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Cargar datos
df = pd.read_csv("orders_top_5_states.csv", parse_dates=['Order Purchase Timestamp'])
df['Order Purchase Timestamp'] = pd.to_datetime(df['Order Purchase Timestamp'])

# Rango completo
min_fecha = df['Order Purchase Timestamp'].min().date()
max_fecha = df['Order Purchase Timestamp'].max().date()

# Rango de fechas
rango_fechas = st.slider(
    "Selecciona rango de fechas",
    min_value=min_fecha,
    max_value=max_fecha,
    value=(min_fecha, max_fecha),
    format="DD/MM/YYYY"
)

# Filtrar por rango
if rango_fechas == (min_fecha, max_fecha):
    df_filtrado = df.copy()
else:
    df_filtrado = df[(df['Order Purchase Timestamp'].dt.date >= rango_fechas[0]) &
                     (df['Order Purchase Timestamp'].dt.date <= rango_fechas[1])]

# Conteo por estado
conteo_estado = (
    df_filtrado.groupby('State')['Customer Unique Id']
    .nunique()
    .reset_index(name='Clientes Totales')
)

# Renombrar columna
conteo_estado.rename(columns={'State': 'Estado'}, inplace=True)

#Histórico para cada estado
df_filtrado['Mes'] = df_filtrado['Order Purchase Timestamp'].dt.to_period('M')
historico = df_filtrado.groupby(['State', 'Mes']).size().reset_index(name='Pedidos')

#Gráfico lineas
historico_pivot = historico.pivot(index='Mes', columns='State', values='Pedidos').fillna(0)
dict = {estado: historico_pivot[estado].tolist() for estado in historico_pivot.columns}


conteo_estado['Histórico Pedidos'] = conteo_estado['Estado'].map(dict)

st.subheader("Clientes por estado")
st.dataframe(
    conteo_estado,
    column_config={
        "Estado": "Estado",
        "Clientes Totales": st.column_config.NumberColumn(
            "Clientes únicos",
            help="Número total de clientes en el rango seleccionado",
            format="%d"
        ),
        "Histórico Pedidos": st.column_config.LineChartColumn(
            "Pedidos (Mes)",
            y_min=0
        )
    },
    hide_index=True,
    use_container_width=True
)

# Agrupo por estado y cuento clientes únicos
customer_by_state = conteo_estado.sort_values('Clientes Totales', ascending=False)

# Seleccionar los 5 estados con más clientes
top5_states = customer_by_state.head(5)

# Configuro el estilo
sns.set_theme(style="whitegrid")

colores_personalizados = ['#ff9b6f', '#ff99cc', '#cc99ff', '#99ccff', '#83bb83']

# Creo gráfico de barras horizontal
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Clientes Totales',
    y='Estado',
    data=top5_states,
    palette=colores_personalizados,
    ax=ax
)

# Añadir título y etiquetas
ax.set_title('Top 5 Estados por Número de Clientes', fontsize=18)
ax.set_xlabel('Número de Clientes', fontsize=14)
ax.set_ylabel('Estado', fontsize=14)

# Valores en las barras
for index, value in enumerate(top5_states['Clientes Totales']):
    ax.text(value + 50, index, str(value), va='center')

plt.tight_layout()

# Mostrar en Streamlit
st.pyplot(fig)

st.write("")
st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="bottom")
with col:
    st.page_link("data.py", label="Conoce los datos", icon="⬅️")
with colm:
    st.page_link("./estado/graficoMedidasEstado.py", label="Gráfico por estado", icon="➡️")