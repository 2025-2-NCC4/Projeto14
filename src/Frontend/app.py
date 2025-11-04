import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard de Teste", layout="wide")

st.title("📊 Dashboard Empresarial")

# ====== SIDEBAR ======
st.sidebar.header("Filtros")
qtd = st.sidebar.slider("Quantidade de linhas", 10, 500, 100)

# ====== DADOS DE EXEMPLO ======
np.random.seed(42)
df = pd.DataFrame({
    "categoria": np.random.choice(["A", "B", "C"], size=1000),
    "valor": np.random.randn(1000).round(2),
    "ano": np.random.choice([2023, 2024, 2025], size=1000)
})

# ====== ABAS PRINCIPAIS ======
CEO, CFO = st.tabs(["👨‍💼 CEO", "💰 CFO"])

# ===================== CEO =====================
with CEO:
    st.header("Visão do CEO")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros", len(df))
    col2.metric("Média de Valor", f"{df['valor'].mean():.2f}")
    col3.metric("Desvio Padrão", f"{df['valor'].std():.2f}")

    st.subheader("Distribuição por Categoria")
    fig = px.pie(df, names="categoria", values="valor", title="Participação das Categorias")
    st.plotly_chart(fig, use_container_width=True)

# ===================== CFO =====================
with CFO:
    st.header("Visão do CFO")
    st.write("Relatório Financeiro com análise temporal")
    df_time = df.groupby("ano")["valor"].sum().reset_index()
    fig2 = px.bar(df_time, x="ano", y="valor", title="Soma de Valor por Ano", color="valor")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Tabela Detalhada")
    st.dataframe(df.head(qtd))
