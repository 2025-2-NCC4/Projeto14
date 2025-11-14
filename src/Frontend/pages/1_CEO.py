import streamlit as st
import pandas as pd
import sys
import os
import re

# Adiciona a pasta charts ao path para importar os gráficos
sys.path.append(os.path.abspath("charts"))
import ceo_charts

# Configurações da página
st.set_page_config(page_title="Dashboard - CEO", layout="wide")

# Carregando base de dados
@st.cache_data
def load_data():
    df_ceo = pd.read_csv("data/analise-ceo.csv", sep=";")
    df_teste_em_massa = pd.read_csv("data/teste_em_massa-limpo.csv", sep=",", engine="python")
    df_cfo = pd.read_csv("data/analise-cfo.csv", sep=";")

    df_mapa = pd.DataFrame()

    #coords ceo
    if{"latitude", "longitude"}.issubset(df_ceo.columns):
        temp = df_ceo[["latitude", "longitude"]].copy()
        temp["source"] = "CEO"
        df_mapa = pd.concat([df_mapa, temp], ignore_index=True)

    #coords cfo
    if{"latitude", "longitude"}.issubset(df_cfo.columns):
        temp = df_cfo[["latitude", "longitude"]].copy()
        temp["source"] = "CFO"
        df_mapa = pd.concat([df_mapa, temp], ignore_index=True)

    # === Correção das colunas de latitude e longitude ===
    def limpar_coord(valor):
        valor = str(valor)

        # Remove tudo que não for número, ponto ou menos
        valor = re.sub(r"[^0-9\.-]", "", valor)

        # Remove todos os pontos
        valor = valor.replace(".", "")

        # Garante que comece com "-"
        if not valor.startswith("-"):
            valor = "-" + valor

        # Latitude/longitude brasileiras costumam ter 8 ou 9 dígitos após o sinal
        # Exemplo correto: -235674304  ->  -23.5674304
        if len(valor) > 3:
            valor = valor[:3] + "." + valor[3:]
    
        try:
            return float(valor)
        except:
            return None


    if "latitude" in df_ceo.columns and "longitude" in df_ceo.columns:
        df_ceo["latitude"] = df_ceo["latitude"].apply(limpar_coord)
        df_ceo["longitude"] = df_ceo["longitude"].apply(limpar_coord)

    return df_ceo, df_teste_em_massa

df_ceo, df_teste_em_massa = load_data()


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
    st.plotly_chart(ceo_charts.grafico_usuarios_por_idade(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_usuarios_por_genero(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_distribuicao_por_horario(df_ceo), use_container_width=True)

# === ABA 2: Dispositivos e Tecnologia ===
with tabs[1]:
    st.subheader("📱 Dispositivos e Tecnologia")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_modelo(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_tipo_celular(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_usuarios_com_app(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_tipo_celular_por_idade(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_modelo_vs_engajamento(df_ceo), use_container_width=True)


# === ABA 3: Localização e Presença ===
with tabs[2]:
    st.subheader("📍 Localização e Presença")
    st.plotly_chart(ceo_charts.grafico_mapa_clusters(df_ceo), use_container_width=True)
   #st.plotly_chart(ceo_charts.grafico_distribuicao_local(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_locais_frequentes(df_ceo), use_container_width=True)
    #st.plotly_chart(ceo_charts.grafico_heatmap_localizacao(df_ceo), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_horario_por_local(df_ceo), use_container_width=True)


# === ABA 4: Engajamento ===
with tabs[3]:
    st.subheader("🎯 Engajamento dos Usuários")
    st.plotly_chart(ceo_charts.grafico_valor_capturado_por_idade(df_ceo), use_container_width=True)


# === ABA 5: Campanhas e Comportamento ===
with tabs[4]:
    st.subheader("🏷️ Campanhas e Comportamento")
    st.plotly_chart(ceo_charts.grafico_categorias_frequentes(df_teste_em_massa), use_container_width=True)
