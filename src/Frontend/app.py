import streamlit as st

st.set_page_config(
    page_title="PicMoney Dashboard",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Navegação")
st.sidebar.write("Selecione uma página:")
# A navegação será automática, pois estamos usando a pasta pages/

st.title("Bem-vindo ao Dashboard PicMoney")
st.write("""
Utilize o menu lateral para navegar entre:
- Visão Geral (CEO)
- Financeiro (CFO)
""")
