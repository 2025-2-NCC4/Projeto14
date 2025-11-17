import streamlit as st

st.set_page_config(page_title="PicStats", page_icon="📊", layout="wide")

st.logo("imgs/logoPicStats.png")

st.image("imgs/logoPicStats.png", width=300)

st.sidebar.title("Navegação")
st.sidebar.write("Selecione uma página:")
# A navegação será automática, pois estamos usando a pasta pages/
st.title("Bem vindo ao Dashboard PicStats")
st.write(
    """
Utilize o menu lateral para navegar entre:
Visão Geral (CEO)
Financeiro (CFO)
"""
)
