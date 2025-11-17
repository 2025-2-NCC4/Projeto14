import streamlit as st
import pandas as pd
import os
import sys
import plotly.io as pio

# Configuração inicial
st.set_page_config(layout="wide", page_title="Dashboard de Parcerias por Loja")

# Adiciona a pasta charts ao path para importar os gráficos
sys.path.append(os.path.abspath("charts"))
try:
    import parcerias_charts
except ImportError:
    st.error(
        "Não foi possível importar o módulo 'parcerias_charts'. Verifique o caminho."
    )
    st.stop()

# Caminho para a pasta de dados
DATA_DIR = "data"

# Arquivos de base de parcerias (que contêm a categoria)
ARQUIVOS_BASE = [
    "base_paulista-limpo.csv",
    "base_players-limpo.csv",
    "cupons_capturados-limpo.csv",
    "teste_em_massa-limpo.csv",
]

# Arquivo com os dados financeiros e 'nome_loja'
ARQUIVO_CFO = "Analise-CFO.csv"

# --- Funções de Carregamento e Consolidação ---


@st.cache_data
def load_data():
    """Carrega e consolida todos os dados em memória, eliminando o arquivo intermediário."""

    # --- 1. Consolidar Bases de Parcerias (Base de 40.000 registros) ---
    dfs_parcerias = []
    for arquivo in ARQUIVOS_BASE:
        caminho = os.path.join(DATA_DIR, arquivo)
        try:
            # Carrega com separador padrão (ponto e vírgula)
            df = pd.read_csv(caminho, sep=";", decimal=",", encoding="latin-1")

            # Adicionar coluna de origem
            df["origem"] = arquivo.replace("-limpo.csv", "")
            dfs_parcerias.append(df)
        except Exception as e:
            st.warning(
                f"Aviso: Erro ao carregar base de categoria {arquivo}. Pode estar faltando. Erro: {e}"
            )

    df_consolidado = pd.concat(dfs_parcerias, ignore_index=True)

    # --- 2. Carregar Dados Financeiros (CFO - 10.000 registros) ---
    caminho_cfo = os.path.join(DATA_DIR, ARQUIVO_CFO)
    df_cfo = pd.DataFrame()

    try:
        # Carrega o CFO com o separador correto (ponto e vírgula)
        # Assumindo que 'nome_loja' e valores financeiros estão aqui
        df_cfo = pd.read_csv(caminho_cfo, sep=";", decimal=".", encoding="latin-1")
    except Exception as e:
        st.warning(
            f"Aviso: Não foi possível carregar o arquivo {ARQUIVO_CFO}. Valores financeiros e nome da loja serão zero/vazios. Erro: {e}"
        )

    # --- 3. Juntar os Dados pelo Índice (Sem Chave Comum) ---

    if df_cfo.empty:
        # Fallback para valores zero e nome de loja vazio
        df_consolidado["nome_loja"] = "Loja Desconhecida"
        df_consolidado["valor_cupom"] = 0.0
        df_consolidado["valor_liquido"] = 0.0
        df_consolidado["valor_compra"] = 0.0
    else:
        # Calcular valor_liquido no CFO
        df_cfo["valor_liquido"] = df_cfo["valor_compra"] - df_cfo["valor_cupom"]

        # Colunas a serem extraídas do CFO (incluindo 'nome_loja')
        colunas_valor = ["nome_loja", "valor_cupom", "valor_liquido", "valor_compra"]

        # Garantir que 'nome_loja' exista no CFO antes de prosseguir
        if "nome_loja" not in df_cfo.columns:
            st.error(
                "Erro: A coluna 'nome_loja' não foi encontrada no arquivo Analise-CFO.csv."
            )
            return pd.DataFrame()  # Retorna vazio para parar o dashboard

        df_cfo_valores = df_cfo[colunas_valor].copy()

        # Criar um DataFrame de 40.000 linhas com os valores do CFO (10.000) e o restante vazio/zero
        df_valores_completos = pd.DataFrame(
            {
                "nome_loja": ["Loja Desconhecida"] * len(df_consolidado),
                "valor_cupom": [0.0] * len(df_consolidado),
                "valor_liquido": [0.0] * len(df_consolidado),
                "valor_compra": [0.0] * len(df_consolidado),
            }
        )

        # Copiar os 10.000 valores do CFO para o DataFrame completo
        # Assumimos que os 40.000 registros de categoria e os 10.000 registros de CFO estão na mesma ordem.
        df_valores_completos.iloc[: len(df_cfo_valores)] = df_cfo_valores.values

        # Adicionar as colunas de valor ao DataFrame consolidado
        df_consolidado["nome_loja"] = df_valores_completos["nome_loja"]
        df_consolidado["valor_cupom"] = df_valores_completos["valor_cupom"]
        df_consolidado["valor_liquido"] = df_valores_completos["valor_liquido"]
        df_consolidado["valor_compra"] = df_valores_completos["valor_compra"]

    # --- 4. Garantir Colunas Mínimas e Tipos ---

    # Garantir que a coluna 'celular' exista para a contagem de transações (usando 'origem' como fallback)
    if "celular" not in df_consolidado.columns:
        df_consolidado["celular"] = df_consolidado[
            "origem"
        ]  # Coluna temporária para contagem

    # Garantir que a coluna 'margem_cupom' exista para os gráficos
    if "margem_cupom" not in df_consolidado.columns:
        df_consolidado["margem_cupom"] = 0.0

    # Tratamento de datas
    if "data_captura" in df_consolidado.columns:
        df_consolidado["data_captura"] = pd.to_datetime(
            df_consolidado["data_captura"], errors="coerce"
        )
        df_consolidado = df_consolidado.dropna(subset=["data_captura"])

    return df_consolidado


# --- Carregar Dados ---
df_parcerias = load_data()

if df_parcerias.empty:
    st.error(
        "Não foi possível carregar os dados de Parcerias. Verifique os arquivos CSV e a coluna 'nome_loja'."
    )
    st.stop()

# --- Título ---
st.title("💛 Dashboard de Parcerias por Loja")
st.markdown(
    "Análise da performance financeira das parcerias da PicMoney, agrupadas por nome de loja."
)

# --- Sidebar para Filtros ---
st.sidebar.header("Filtros de Parcerias")

# 1. Filtro de Nome de Loja
# O filtro é criado a partir dos valores únicos da coluna 'nome_loja'
nomes_loja = ["Todas"] + sorted(df_parcerias["nome_loja"].unique().tolist())
selected_loja = st.sidebar.multiselect("Nome da Loja", nomes_loja, default=["Todas"])

# --- Aplicação dos Filtros ---
df_filtered = df_parcerias.copy()

# Filtro de Nome de Loja (Aplica a filtragem no DataFrame)
if "Todas" not in selected_loja:
    df_filtered = df_filtered[df_filtered["nome_loja"].isin(selected_loja)]

# O filtro de Origem foi removido daqui.

# Filtro de Data (Mantido do código original)
if "data_captura" in df_filtered.columns and not df_filtered.empty:
    min_date = df_filtered["data_captura"].min().date()
    max_date = df_filtered["data_captura"].max().date()
    date_range = st.sidebar.date_input(
        "Selecione o Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        df_filtered = df_filtered[
            (df_filtered["data_captura"] >= start_date)
            & (df_filtered["data_captura"] <= end_date)
        ]


# --- Indicadores Chave de Performance (KPIs) ---
st.header("Indicadores Chave de Performance (KPIs)")

total_receita_liquida = df_filtered["valor_liquido"].sum()
total_desconto_concedido = df_filtered["valor_cupom"].sum()
total_transacoes = len(df_filtered)
ticket_medio = df_filtered["valor_compra"].mean() if total_transacoes > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Receita Líquida Total",
        value=f"R$ {total_receita_liquida:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

with col2:
    st.metric(
        label="Total de Desconto Concedido",
        value=f"R$ {total_desconto_concedido:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

with col3:
    st.metric(
        label="Total de Transações", value=f"{total_transacoes:,.0f}".replace(",", ".")
    )

with col4:
    st.metric(
        label="Ticket Médio",
        value=f"R$ {ticket_medio:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

# --- Análise de Performance por Loja ---
st.header("Análise de Performance por Loja")

col5, col6 = st.columns(2)

# Os gráficos agora agrupam por 'nome_loja'
with col5:
    st.subheader("Top 10 Lojas por Receita Líquida")
    st.plotly_chart(
        parcerias_charts.plot_receita_por_categoria(df_filtered, group_col="nome_loja"),
        use_container_width=True,
    )

with col6:
    st.subheader("Distribuição do Desconto Concedido por Loja")
    st.plotly_chart(
        parcerias_charts.plot_desconto_por_categoria(
            df_filtered, group_col="nome_loja"
        ),
        use_container_width=True,
    )

# --- Tabela de Dados Detalhados por Loja ---
st.header("📊 Dados Detalhados por Nome de Loja")

# Criar um resumo por loja
loja_resumo = (
    df_filtered.groupby("nome_loja")
    .agg(
        {
            "celular": "count",  # Usamos 'celular' (ou o fallback) para contar o número de transações
            "valor_liquido": "sum",
            "valor_cupom": "sum",
            "valor_compra": "mean",
        }
    )
    .reset_index()
)

# Renomear as 5 colunas
loja_resumo.columns = [
    "Nome da Loja",
    "Número de Transações",
    "Receita Líquida (R$)",
    "Total de Desconto (R$)",
    "Ticket Médio (R$)",
]

# Ordenar por receita líquida
loja_resumo = loja_resumo.sort_values("Receita Líquida (R$)", ascending=False)

# Formatação dos valores
loja_resumo["Receita Líquida (R$)"] = (
    loja_resumo["Receita Líquida (R$)"]
    .map("R$ {:,.2f}".format)
    .str.replace(",", "X")
    .str.replace(".", ",")
    .str.replace("X", ".")
)
loja_resumo["Total de Desconto (R$)"] = (
    loja_resumo["Total de Desconto (R$)"]
    .map("R$ {:,.2f}".format)
    .str.replace(",", "X")
    .str.replace(".", ",")
    .str.replace("X", ".")
)
loja_resumo["Ticket Médio (R$)"] = (
    loja_resumo["Ticket Médio (R$)"]
    .map("R$ {:,.2f}".format)
    .str.replace(",", "X")
    .str.replace(".", ",")
    .str.replace("X", ".")
)
loja_resumo["Número de Transações"] = (
    loja_resumo["Número de Transações"].map("{:,.0f}".format).str.replace(",", ".")
)

# Exibir tabela
st.dataframe(loja_resumo, use_container_width=True, hide_index=True)

# --- Tabela de Dados Detalhados (Registros Individuais) ---
st.header("📋 Registros Detalhados")

# Selecionar colunas principais para exibição
colunas_exibicao = [
    "celular",
    "nome_loja",
    "origem",
    "valor_liquido",
    "valor_compra",
    "valor_cupom",
]

# Filtrar apenas as colunas que existem no dataframe
colunas_exibicao = [col for col in colunas_exibicao if col in df_filtered.columns]

# Exibir tabela com dados detalhados
st.dataframe(
    df_filtered[colunas_exibicao].head(100), use_container_width=True, hide_index=True
)

st.info(f"Mostrando os primeiros 100 registros de {len(df_filtered)} registros totais")
