import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("Gráficos por pedidos tardíos")


opcion = st.selectbox(
    "Selecciona el gráfico a mostrar:",
    ["-- Selecciona un gráfico",
     "Porcentaje de pedidos tardíos y días promedio de retraso por ciudad (Top 15)", 
     "Porcentaje de pedidos tardíos y días promedio de retraso por ciudad (Top 15 Alfabéticamente)"]
)

if opcion == "-- Selecciona un gráfico":
    st.write("Esperando selección...")
elif opcion == "Porcentaje de pedidos tardíos y días promedio de retraso por ciudad (Top 15)":
    st.subheader("Porcentaje de pedidos tardíos y días promedio de retraso por ciudad (Top 15)")

    # Gráfico combinado (barras + línea)
    city_delay_orders = pd.read_csv("city_delay_orders.csv")
    city_delay_orders_sorted = city_delay_orders.sort_values('late_percentage', ascending=False).head(15)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Barras
    sns.barplot(
        data=city_delay_orders_sorted,
        x='city',
        y='late_percentage',
        ax=ax1,
        color='skyblue'
    )

    ax1.set_ylabel('Porcentaje de pedidos tardíos (%)', color='blue')
    ax1.set_xlabel('Ciudad')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45, ha='right')

    # Segundo eje (línea)
    ax2 = ax1.twinx()
    sns.lineplot(
        data=city_delay_orders_sorted,
        x='city',
        y='mean_late_days',
        ax=ax2,
        color='red',
        marker='o'
    )

    ax2.set_ylabel('Días promedio de retraso', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.tight_layout()

    st.pyplot(fig)
else:
    st.subheader("Porcentaje de pedidos tardíos y días promedio de retraso por ciudad (Top 15 Alfabéticamente)")

    # Gráfico combinado (barras + línea)
    city_delay_orders = pd.read_csv("city_delay_orders.csv")
    city_delay_orders_sorted = city_delay_orders.head(15)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Barras
    sns.barplot(
        data=city_delay_orders_sorted,
        x='city',
        y='late_percentage',
        ax=ax1,
        color='skyblue'
    )

    ax1.set_ylabel('Porcentaje de pedidos tardíos (%)', color='blue')
    ax1.set_xlabel('Ciudad')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45, ha='right')

    # Segundo eje (línea)
    ax2 = ax1.twinx()
    sns.lineplot(
        data=city_delay_orders_sorted,
        x='city',
        y='mean_late_days',
        ax=ax2,
        color='red',
        marker='o'
    )

    ax2.set_ylabel('Días promedio de retraso', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.tight_layout()

    st.pyplot(fig)

    st.write("")
st.write("")
st.write("")

st.page_link("pages/clienteCiudad.py", label="Clientes por ciudad", icon="⬅️")

