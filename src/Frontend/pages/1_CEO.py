import streamlit as st
import pandas as pd
import sys
import os

# Adiciona a pasta charts ao path para importar os gráficos
sys.path.append(os.path.abspath("charts"))
import ceo_charts

# Configurações da página
st.set_page_config(page_title="Dashboard - CEO", layout="wide")

# Carregando base de dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/analise-ceo.csv", sep=";")
    df_teste_em_massa = pd.read_csv("data/teste_em_massa-limpo.csv", sep=";")


    # === Correção das colunas de latitude e longitude ===
    def limpar_coord(valor):
        valor = str(valor).replace(".", "")  # remove todos os pontos
        if valor.startswith("-") and len(valor) > 3:
            valor = valor[:3] + "." + valor[3:]  # adiciona ponto após os 3 primeiros caracteres (-23.)
        try:
            return float(valor)
        except:
            return None

    if "latitude" in df.columns and "longitude" in df.columns:
        df["latitude"] = df["latitude"].apply(limpar_coord)
        df["longitude"] = df["longitude"].apply(limpar_coord)

    return df, df_teste_em_massa

df, df_teste_em_massa = load_data()

# Título principal
st.title("📊 Dashboard Executivo - CEO")
st.markdown("""
Aqui você encontra as principais métricas estratégicas relacionadas ao comportamento dos usuários,
dispositivos utilizados e engajamento com a PicMoney.  
Use as abas abaixo para navegar entre os indicadores.
""")

# Criação das abas
tabs = st.tabs([
    "👥 Perfil de Usuários",
    "📱 Dispositivos e Tecnologia",
    "📍 Localização e Presença",
    "🎯 Engajamento",
    "🏷️ Campanhas e Comportamento"
])

# === ABA 1: Perfil de Usuários ===
with tabs[0]:
    st.subheader("👥 Perfil de Usuários")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_idade(df), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_usuarios_por_genero(df), use_container_width=True)

# === ABA 2: Dispositivos e Tecnologia ===
with tabs[1]:
    st.subheader("📱 Dispositivos e Tecnologia")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_modelo(df), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_tipo_celular(df), use_container_width=True)

# === ABA 3: Localização e Presença ===
with tabs[2]:
    st.subheader("📍 Localização e Presença")
    st.plotly_chart(ceo_charts.grafico_distribuicao_local(df), use_container_width=True)

# === ABA 4: Engajamento ===
with tabs[3]:
    st.subheader("🎯 Engajamento dos Usuários")
    st.plotly_chart(ceo_charts.grafico_valor_capturado_por_idade(df), use_container_width=True)

# === ABA 5: Campanhas e Comportamento ===
with tabs[4]:
    st.subheader("🏷️ Campanhas e Comportamento")
    st.plotly_chart(ceo_charts.grafico_categorias_frequentes(df_teste_em_massa), use_container_width=True)
