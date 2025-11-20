import streamlit as st
import pandas as pd


col1,col2 = st.columns([0.5,2])
with col1:
    st.write("")
with col2:
    st.title("Dashboard Olist")
    st.write("")
    st.write("")
    

col3, col4 = st.columns([1,3])

# Imagen Olist
with col3:
    st.image("./logo.png", width=200)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
        
# Texto descriptivo
with col4:
    st.markdown("""
    **Olist**, una destacada startup brasileña, está transformando el panorama del comercio digital en Latinoamérica.  
    ***Fundada en 2015***, esta plataforma actúa como un intermediario eficiente, conectando pequeños y medianos comerciantes con los principales marketplaces y canales de venta en línea.  

    Su modelo de negocio innovador no solo facilita la digitalización de las operaciones, sino que también ofrece soluciones de logística, marketing y financiamiento.  

    Con una presencia cada vez más sólida en el mercado, Olist ha demostrado su capacidad para empoderar a los negocios locales y ayudarles a competir en un entorno cada vez más digitalizado y competitivo.  

    Este análisis explorará cómo Olist está redefiniendo el comercio digital en la región y sus perspectivas de futuro.
    """)

st.write("")
st.write("")
        
col5,col6 = st.columns([1,2])
with col5:
    st.write("")
with col6:
    st.page_link("https://olist.com/", label="Página web Olist", icon="🌐")

st.write("")
st.write("")
st.write("")
st.write("")

df = pd.read_csv("./DatasetCsv/olist_customers_dataset.csv")
df1 = pd.read_csv("./DatasetCsv/olist_orders_dataset.csv")
states_reviews = pd.read_csv("states_reviews.csv")

col1, col2, col3 = st.columns(3)

p = df1['order_id'].nunique()
c = df['customer_unique_id'].nunique()
r = states_reviews['mean_reviews'].mean()

col1.metric("Pedidos", f"{p}", border=True, width=200)
col2.metric("Clientes", f"{c}", border=True, width=200)
col3.metric("Reseñas promedio", f"{r:.2f} ⭐", border=True, width=200)

st.write("")
st.write("")

col, colm = st.columns(2, vertical_alignment="center")
with col:
    st.write("")
# with colm:
    # st.page_link("./pages/data.py", label="Datos de las tablas", icon="➡️")
