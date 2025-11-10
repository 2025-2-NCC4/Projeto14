# pages/2_CFO.py
import streamlit as st
import plotly.io as pio
pio.templates.default = "plotly_dark"

st.set_page_config(page_title="Dashboard CFO", layout="wide")

st.title("Visão Financeira - CFO")
st.write("KPIs e métricas financeiras.")

# Criando 5 abas genéricas
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Métrica 1",
    "Métrica 2",
    "Métrica 3",
    "Métrica 4",
    "Métrica 5"
])

with aba1:
    st.subheader("Métrica 1 - Receita Total")
    st.write("(Colocar gráfico aqui)")

with aba2:
    st.subheader("Métrica 2 - Custo Operacional")
    st.write("(Colocar gráfico aqui)")

with aba3:
    st.subheader("Métrica 3 - Margem de Lucro")
    st.write("(Colocar gráfico aqui)")

with aba4:
    st.subheader("Métrica 4 - Previsão Financeira")
    st.write("(Colocar gráfico aqui)")

with aba5:
    st.subheader("Métrica 5 - Comparativo entre Parceiros")
    st.write("(Colocar gráfico aqui)")