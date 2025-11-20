import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Cargar datos
states_reviews = pd.read_csv("states_reviews.csv")
df_top = pd.read_csv("top_5_states.csv")
df_orders_delivered_on_time = pd.read_csv("df_orders_delivered_on_time.csv")

colores_personalizados = ['#ff9b6f', '#ff99cc', '#cc99ff', '#99ccff', "#83bb83"]

opcion = st.selectbox(
    "Selecciona el gráfico a mostrar:",
    ["-- Selecciona un gráfico",
     "Puntuación media de reseñas por estado (Pedidos a tiempo)", 
     "Distribución de puntuaciones de reseñas por estado"]
)

if opcion == "-- Selecciona un gráfico":
    st.write("Esperando selección...")
elif opcion == "Puntuación media de reseñas por estado (Pedidos a tiempo)":
    st.subheader('Puntuación media de reseñas por estado (Pedidos a tiempo)')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    states_reviews_sorted = states_reviews.sort_values('mean_reviews', ascending=False)
    
    sns.barplot(
        data=states_reviews_sorted,
        y='state',
        x='mean_reviews',
        palette=colores_personalizados
    )

    for index, row in states_reviews_sorted.iterrows():
        ax1.text(row['mean_reviews'] + 0.05, index, f"{row['num_reviews']} reseñas", va='center')

    ax1.set_xlabel('Puntuación media')
    ax1.set_ylabel('Estado')
    ax1.set_xlim(0, 5)
    plt.tight_layout()
    st.pyplot(fig1)

else:
    st.subheader('Distribución de puntuaciones de reseñas por estado')

    # Columnas y filtro
    col = df_top.columns.tolist()
    select_columns = col[0]
    uniq_values = df_top[select_columns].unique()
    select_values = st.multiselect("Selecciona uno o más estados", uniq_values)

    # Filtrar DataFrames
    if select_values:
        filt_reviews = states_reviews[states_reviews['state'].isin(select_values)]
        filt_orders = df_orders_delivered_on_time[df_orders_delivered_on_time['customer_state'].isin(select_values)]
    else:
        filt_reviews = states_reviews.copy()
        filt_orders = df_orders_delivered_on_time.copy()

    # Ordenar por puntuación media
    filt_reviews = filt_reviews.sort_values('mean_reviews', ascending=False)

    # Agrupar y pivotar
    score_count = filt_orders.groupby(['customer_state', 'review_score']).size().reset_index(name='count_scores')
    score_count = score_count.pivot(index='customer_state', columns='review_score', values='count_scores').fillna(0)
    score_count = score_count.astype(int).sort_values(by=5, ascending=False)

        
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    # fig2.patch.set_facecolor('#f5f5f5')
    # ax2.set_facecolor('#f0f0f0')
    score_count.plot(kind='line', marker='o',color=colores_personalizados, ax=ax2)

    ax2.set_title('Distribución de puntuaciones por estado', fontsize=14)
    ax2.set_xlabel('Estado')
    ax2.set_ylabel('Número de reseñas')
    ax2.legend(title='Puntuación')
    plt.tight_layout()
    st.pyplot(fig2)



st.write("")
st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="bottom")
with col:
    st.page_link("./estado/graficoMedidasEstado.py", label="Gráfico por estado", icon="⬅️")
with colm:
    st.page_link("./estado/mapa.py", label="Mapa", icon="➡️")

