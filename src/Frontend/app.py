import cfo_charts
import ceo_charts
import streamlit as st
import pandas as pd
import sys
import os
import re
import numpy as np

# Adiciona a pasta charts ao path para importar os gráficos
# Assumindo que a estrutura de pastas é a mesma da imagem (src/Frontend/charts)
# O caminho absoluto pode variar, mas vamos usar o caminho relativo que parece ser o padrão.
sys.path.append(os.path.abspath("charts"))

# --- Funções de Carregamento e Pré-processamento de Dados ---


@st.cache_data
def load_ceo_data():
    """Carrega e pré-processa os dados para o CEO."""
    try:
        df_ceo = pd.read_csv("data/Analise-CEO.csv", sep=";")
        df_teste_em_massa = pd.read_csv(
            "data/teste_em_massa-limpo.csv", sep=",", engine="python")

        # Função de limpeza de coordenadas (copiada de 1_CEO.py)
        def limpar_coord(valor):
            valor = str(valor)
            valor = re.sub(r"[^0-9\.-]", "", valor)
            valor = valor.replace(".", "")
            if not valor.startswith("-"):
                valor = "-" + valor
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
    except Exception as e:
        st.error(f"Erro ao carregar dados do CEO: {e}")
        return pd.DataFrame(), pd.DataFrame()


@st.cache_data
def load_cfo_data():
    """Carrega e pré-processa os dados para o CFO."""
    try:
        df_cfo = pd.read_csv('data/Analise-CFO.csv', sep=';', decimal=',')
        df_dem = pd.read_csv(
            'data/cupons_capturados-limpo.csv', sep=',', decimal='.')

        # Tratamento de colunas numéricas (copiado de 2_CFO.py)
        if 'valor_compra' in df_cfo.columns:
            df_cfo['valor_compra'] = df_cfo['valor_compra'].astype(str).str.replace(
                '.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        if 'valor_cupom' in df_cfo.columns:
            df_cfo['valor_cupom'] = df_cfo['valor_cupom'].astype(str).str.replace(
                '.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

        # Tratamento de datas (copiado de 2_CFO.py)
        if 'data_captura' in df_cfo.columns:
            df_cfo['data_captura'] = pd.to_datetime(
                df_cfo['data_captura'], format='%d/%m/%Y', errors='coerce')
            df_cfo = df_cfo.dropna(subset=['data_captura'])
            df_cfo['mes_ano'] = df_cfo['data_captura'].dt.to_period('M')
            df_cfo['dia_semana'] = df_cfo['data_captura'].dt.day_name(
                locale='pt_BR')

        # Padronizar a coluna de celular em df_cfo e df_dem para o merge
        if 'numero_celular' in df_cfo.columns:
            df_cfo['numero_celular'] = df_cfo['numero_celular'].astype(
                str).str.replace(r'[() -]', '', regex=True)
        if 'celular' in df_dem.columns:
            df_dem = df_dem.rename(columns={'celular': 'numero_celular'})
        if 'numero_celular' in df_dem.columns:
            df_dem['numero_celular'] = df_dem['numero_celular'].astype(
                str).str.replace(r'[() -]', '', regex=True)

        # Merge dos DataFrames
        df_merged = pd.merge(df_cfo, df_dem, on='numero_celular', how='left')

        # Cálculo de Métricas Financeiras Chave
        df_merged['valor_liquido'] = df_merged['valor_compra'] - \
            df_merged['valor_cupom']

        return df_merged
    except Exception as e:
        st.error(f"Erro ao carregar dados do CFO: {e}")
        return pd.DataFrame()


# --- Carregamento dos Dados ---
df_ceo, df_teste_em_massa = load_ceo_data()
df_cfo_merged = load_cfo_data()

# --- Configuração da Página ---
st.set_page_config(
    page_title="PicStats - Home",
    page_icon="📊",
    layout="wide"
)

st.logo(
    "imgs/logoPicStats.png"
)

st.image("imgs/logoPicStats.png", width=300)


st.title("Visão Geral Executiva")
st.markdown("""
Esta página consolida as métricas mais importantes para o **CEO** e para o **CFO**.
""")

# --- Resumo de Dados Brutos (KPIs) ---
if not df_cfo_merged.empty:
    # Cálculo de KPIs de Resumo (usando o df_cfo_merged completo para um resumo geral)
    total_liquido = df_cfo_merged['valor_liquido'].sum()
    total_desconto = df_cfo_merged['valor_cupom'].sum()
    ticket_medio = df_cfo_merged['valor_compra'].mean()
    num_cupons = df_cfo_merged.shape[0]

    # KPIs do CEO (usuários)
    num_usuarios = df_ceo['numero_celular'].nunique(
    ) if not df_ceo.empty and 'numero_celular' in df_ceo.columns else 0
    idade_media = df_ceo['idade'].mean(
    ) if not df_ceo.empty and 'idade' in df_ceo.columns else 0

    st.subheader("Resumo Geral")
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5, col_kpi6 = st.columns(6)

    with col_kpi1:
        st.metric(label="Receita Líquida Total", value=f"R$ {total_liquido:,.2f}".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    with col_kpi2:
        st.metric(label="Desconto Concedido", value=f"R$ {total_desconto:,.2f}".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    with col_kpi3:
        st.metric(label="Ticket Médio", value=f"R$ {ticket_medio:,.2f}".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    with col_kpi4:
        st.metric(label="Total de Cupons", value=f"{num_cupons:,}".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    with col_kpi5:
        st.metric(label="Total de Usuários", value=f"{num_usuarios:,}".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    with col_kpi6:
        st.metric(label="Idade Média", value=f"{idade_media:,.1f} anos".replace(
            ",", "X").replace(".", ",").replace("X", "."))

    st.markdown("---")


# --- Filtros Globais (Simplificados para a Home) ---
st.sidebar.header("Filtros")

# Filtro de Idade (CEO)
if not df_ceo.empty and "idade" in df_ceo.columns:
    idade_min, idade_max = int(
        df_ceo["idade"].min()), int(df_ceo["idade"].max())
    filtro_idade_min, filtro_idade_max = st.sidebar.slider(
        "Faixa de idade (CEO)",
        idade_min,
        idade_max,
        (idade_min, idade_max)
    )
    df_ceo_filtrado = df_ceo[
        (df_ceo["idade"] >= filtro_idade_min) &
        (df_ceo["idade"] <= filtro_idade_max)
    ]
else:
    df_ceo_filtrado = df_ceo.copy()
    st.sidebar.warning("Dados do CEO indisponíveis ou incompletos.")

# Filtro de Data (CFO)
if not df_cfo_merged.empty and "data_captura" in df_cfo_merged.columns:
    min_date = df_cfo_merged['data_captura'].min().date()
    max_date = df_cfo_merged['data_captura'].max().date()
    date_range = st.sidebar.date_input("Período de Análise (CFO)",
                                       value=(min_date, max_date),
                                       min_value=min_date,
                                       max_value=max_date)

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        df_cfo_filtrado = df_cfo_merged[(df_cfo_merged['data_captura'] >= start_date) & (
            df_cfo_merged['data_captura'] <= end_date)]
    else:
        df_cfo_filtrado = df_cfo_merged.copy()
else:
    df_cfo_filtrado = df_cfo_merged.copy()
    st.sidebar.warning("Dados do CFO indisponíveis ou incompletos.")


# --- Exibição das Métricas ---

# --- CEO Metrics ---
st.header("Visão do CEO")
col_ceo1, col_ceo2 = st.columns(2)

if not df_ceo_filtrado.empty:
    # 1. Idade dos usuários (Gráfico de Distribuição por Idade)
    with col_ceo1:
        st.subheader("1. Distribuição de Usuários por Idade")
        try:
            st.plotly_chart(ceo_charts.grafico_usuarios_por_idade(
                df_ceo_filtrado), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de idade: {e}")

    # 2. Mapa com clusters (Mapa de Localização)
    with col_ceo2:
        st.subheader("2. Mapa de Clusters de Usuários")
        try:
            st.plotly_chart(ceo_charts.grafico_mapa_clusters(
                df_ceo_filtrado), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar mapa de clusters: {e}")

    # 3. Categorias de lojas mais frequentadas
    st.subheader("3. Categorias de Lojas Mais Frequentadas")
    if not df_teste_em_massa.empty:
        try:
            # Replicando a lógica de filtro de categoria para a home (sem filtro na sidebar)
            categorias = sorted(
                df_teste_em_massa["categoria_frequentada"].dropna().unique())
            df_temp_ceo = df_teste_em_massa[df_teste_em_massa["categoria_frequentada"].isin(
                categorias)]
            st.plotly_chart(ceo_charts.grafico_categorias_frequentes(
                df_temp_ceo), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de categorias: {e}")
    else:
        st.info("Dados de categorias de lojas (df_teste_em_massa) indisponíveis.")
else:
    st.warning(
        "Não foi possível exibir as métricas do CEO devido a dados vazios ou erros de carregamento.")


st.markdown("---")

# --- CFO Metrics ---
st.header("Visão do CFO")
col_cfo1, col_cfo2, col_cfo3 = st.columns(3)

if not df_cfo_filtrado.empty:
    # 1. Receita líquida ao longo do tempo
    with col_cfo1:
        st.subheader("1. Receita Líquida ao Longo do Tempo")
        try:
            st.plotly_chart(cfo_charts.plot_time_series(
                df_cfo_filtrado, 'valor_liquido', 'Receita Líquida'), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de Receita Líquida: {e}")

    # 2. Ticket médio ao longo do tempo
    with col_cfo2:
        st.subheader("2. Ticket Médio ao Longo do Tempo")
        try:
            st.plotly_chart(cfo_charts.plot_average_time_series(
                df_cfo_filtrado, 'valor_compra', 'Ticket Médio (ATV)'), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de Ticket Médio: {e}")

    # 3. Desconto concedido ao longo do tempo
    with col_cfo3:
        st.subheader("3. Desconto Concedido ao Longo do Tempo")
        try:
            st.plotly_chart(cfo_charts.plot_time_series(
                df_cfo_filtrado, 'valor_cupom', 'Desconto Concedido'), use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de Desconto Concedido: {e}")
else:
    st.warning(
        "Não foi possível exibir as métricas do CFO devido a dados vazios ou erros de carregamento.")
