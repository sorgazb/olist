import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.header("Filtro de medidas por estado")

# Leer datos
df_top = pd.read_csv("top_5_states.csv")
df_orders_delivered = pd.read_csv("df_orders_delivered.csv")
states_payments = pd.read_csv("states_payments.csv")

col = df_top.columns.tolist()

# Selección de columna para filtrar (por defecto la primera)
select_columns = col[0]
uniq_values = df_top[select_columns].unique()
select_values = st.multiselect("Selecciona uno o más estados", uniq_values)

# Filtrar DataFrame
if select_values:
    filt_df = df_top[df_top[select_columns].isin(select_values)]
else:
    filt_df = df_top.copy()

# Selección de columnas para gráfico dinámico
x_col = st.selectbox("Selecciona columna para eje X", col[0])
y_col = st.selectbox("Selecciona columna para eje Y", col[1:])

# Botón para generar gráfico dinámico
if st.button("Generar gráfico"):
    st.line_chart(filt_df.set_index(x_col)[y_col])
else:
    st.write("Esperando selección...")

st.write("")
st.write("")
st.header("Gráficos")

colores_personalizados = ["#ff9b6f", '#ff99cc', '#cc99ff', '#99ccff', '#83bb83']

# Selectbox para elegir gráfico predefinido
opcion = st.selectbox(
    "Selecciona el gráfico a mostrar:",
    ["-- Selecciona un grafico", "Customers vs Orders", "Porcentaje de pedidos por estado",
     "Porcentaje de pedidos tardíos",
     "Método de pago por estados"]
)

if opcion == "-- Selecciona un grafico":
    st.write("Esperando selección...")
elif opcion == "Customers vs Orders":
    st.subheader("Customer vs Orders por estado")

    # Usar el DataFrame filtrado
    plot_df = filt_df.melt(
        id_vars='State', 
        value_vars=['Customer', 'Orders'],  
        var_name='metric',
        value_name='count'
    )

    sns.set_theme(style="whitegrid")

    g = sns.catplot(
        data=plot_df, kind="bar",
        x="State", y="count", hue="metric",
        errorbar=None, palette=colores_personalizados, alpha=.6, height=6
    )

    g.despine(left=True)
    g.set_axis_labels("Estado", "Cantidad")
    g.legend.set_title("")

    st.pyplot(g)

elif opcion == "Porcentaje de pedidos por estado":
    st.subheader('Porcentaje de pedidos por estado')
   # Gráfico de pastel
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        df_top['%'],
        labels=df_top['State'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colores_personalizados
    )
    
    # Mostrar gráfico en Streamlit
    st.pyplot(fig)

elif opcion == "Porcentaje de pedidos tardíos":
    st.subheader('Porcentaje de pedidos tardíos y días promedio de retraso por estado')
    
    # agrupo por estado del cliente y calcula métricas
    state_delay_orders = df_orders_delivered.groupby('customer_state').agg(
        orders_deliverd=('order_id', 'count'),    
        late_orders=('delivered_late', 'sum'),      
        mean_late_days=('delay_days', 'mean')      
    ).reset_index()  
    
    #calculo el porcentaje de pedidos tardíos por estado
    state_delay_orders['late_percentage'] = (
        state_delay_orders['late_orders'] / state_delay_orders['orders_deliverd'] * 100
    ).round(2)
    
    #ordeno los estados por porcentaje de pedidos tardíos (de mayor a menor)
    state_delay_orders_sorted = state_delay_orders.sort_values('late_percentage', ascending=False)
    
    #creo la figura y el primer eje
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    #gráfico de barras
    sns.barplot(
        data=state_delay_orders_sorted,
        x='customer_state',
        y='late_percentage',
        ax=ax1,
        color=colores_personalizados[3]
    )
    
    #etiquetas del eje y izquierdo
    ax1.set_ylabel('Porcentaje de pedidos tardíos (%)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    plt.xticks(rotation=45)  
    ax1.set_xlabel('Estado')
    
    #etiquetas del eje y derecho
    ax2 = ax1.twinx()
    
    #gráfico de línea
    sns.lineplot(
        data=state_delay_orders_sorted,
        x='customer_state',
        y='mean_late_days',
        ax=ax2,
        color=colores_personalizados[2],
        marker='o',
        ci=None  
    )
    
    #configuro etiquetas y colores del eje y derecho
    ax2.set_ylabel('Días promedio de retraso', color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    st.pyplot(fig)
else:
    # Cargar datos
    states_payments = pd.read_csv('states_payments.csv', index_col='customer_state')

    # ASEGURAR QUE TODO SEA NUMÉRICO
    states_payments = states_payments.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Crear figura
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Obtener datos
    estados = states_payments.index.tolist()
    payment_methods = states_payments.columns.tolist()

    # Colores
    colors_payment = ['#ffcc99', '#ff99cc', '#99ccff', '#83bb83']

    # Posiciones
    num_estados = len(estados)
    num_payments = len(payment_methods)
    x_pos = np.arange(num_estados)

    bar_width = 0.4
    bar_depth = 0.7

    # Barras para cada método
    for j, payment in enumerate(payment_methods):
        y_offset = j * 2.5
        # CONVERTIR EXPLÍCITAMENTE A FLOAT
        values = states_payments[payment].values.astype(float)

        for i in range(num_estados):
            ax.bar3d(
                x_pos[i] - bar_width/2, 
                y_offset, 
                0, 
                bar_width, 
                bar_depth, 
                float(values[i]),  # ASEGURAR QUE ES FLOAT
                color=colors_payment[j], 
                alpha=0.85,
                edgecolor='black',
                linewidth=0.5
            )

    # Configurar ejes
    ax.set_xlabel('Estados', fontsize=13, weight='bold', labelpad=12)
    ax.set_ylabel('Método de Pago', fontsize=13, weight='bold', labelpad=15)
    ax.set_zlabel('Número de Transacciones', fontsize=13, weight='bold', labelpad=12)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(estados, fontsize=11)

    y_ticks = [j * 2.5 + bar_depth/2 for j in range(num_payments)]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(payment_methods, fontsize=10)

    ax.set_title('Métodos de Pago por Estado', fontsize=15, weight='bold', pad=20)
    ax.view_init(elev=25, azim=135)
    ax.grid(True, alpha=0.3)

    # Mostrar en Streamlit
    st.pyplot(fig)


st.write("")
st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="bottom")
with col:
    st.page_link("pages/clientesEstado.py", label="Clientes por estado", icon="⬅️")
with colm:
    st.page_link("pages/resenas.py", label="Análisis de reseñas", icon="➡️")

