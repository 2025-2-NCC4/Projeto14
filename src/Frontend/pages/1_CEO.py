import streamlit as st
import pandas as pd
import sys
import os

# Permite importar o módulo charts/ceo_charts.py
sys.path.append(os.path.abspath("charts"))
import ceo_charts

st.set_page_config(page_title="Visão Geral - CEO", layout="wide")

df = pd.read_csv("data/Analise-CEO.csv", sep=";")

st.title("Visão Geral - CEO")

tabs = st.tabs(["Usuários", "Gênero", "Modelo de Celular", "Métrica 4", "Métrica 5"])

with tabs[0]:
    st.subheader("Distribuição por Idade dos Usuários")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_idade(df), use_container_width=True)

with tabs[1]:
    st.subheader("Distribuição por Sexo")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_genero(df), use_container_width=True)

with tabs[2]:
    st.subheader("Modelos de Celular mais Utilizados")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_modelo(df), use_container_width=True)

with tabs[3]:
    st.write("Métrica 4 – aguardando dados futuros")

with tabs[4]:
    st.write("Métrica 5 – aguardando dados futuros")
