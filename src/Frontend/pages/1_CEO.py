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


# FILTROS GLOBAIS DO DASHBOARD
# ==============================
st.sidebar.header("Filtros")

# Faixa de idade (mínimo e máximo)
idade_min, idade_max = int(df_ceo["idade"].min()), int(df_ceo["idade"].max())
filtro_idade_min, filtro_idade_max = st.sidebar.slider(
    "Faixa de idade",
    idade_min,
    idade_max,
    (idade_min, idade_max)
)

# Filtro por gênero (se existir na base)
coluna_genero = None
for col in df_ceo.columns:
    if col.lower().strip() in ["genero", "gênero", "sexo"]:
        coluna_genero = col
        break

if coluna_genero:
    filtro_genero = st.sidebar.multiselect(
        "Gênero",
        options=df_ceo[coluna_genero].dropna().unique(),
        default=df_ceo[coluna_genero].dropna().unique()
    )
else:
    filtro_genero = None

# Filtro por cidade (se existir)
coluna_cidade = None
for col in df_ceo.columns:
    if col.lower().strip() in ["cidade", "city", "municipio"]:
        coluna_cidade = col
        break

if coluna_cidade:
    filtro_cidade = st.sidebar.multiselect(
        "Cidade",
        options=df_ceo[coluna_cidade].dropna().unique(),
        default=df_ceo[coluna_cidade].dropna().unique()
    )
else:
    filtro_cidade = None


# Aplicação dos filtros
# ==============================
df_ceo_filtrado = df_ceo.copy()

# Aplicar faixa de idade
df_ceo_filtrado = df_ceo_filtrado[
    (df_ceo_filtrado["idade"] >= filtro_idade_min) &
    (df_ceo_filtrado["idade"] <= filtro_idade_max)
]

# Aplicar filtro de gênero
if filtro_genero is not None:
    df_ceo_filtrado = df_ceo_filtrado[df_ceo_filtrado[coluna_genero].isin(filtro_genero)]

# Aplicar filtro de cidade
if filtro_cidade is not None:
    df_ceo_filtrado = df_ceo_filtrado[df_ceo_filtrado[coluna_cidade].isin(filtro_cidade)]

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
    st.plotly_chart(ceo_charts.grafico_usuarios_por_idade(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_usuarios_por_genero(df_ceo_filtrado), use_container_width=True)
     # --- Filtro por horário ---
    st.markdown("### Filtro por horário do dia")

    col1, col2 = st.columns(2)
    with col1:
        horario_inicio = st.time_input("Horário inicial", value=pd.to_datetime("00:00").time())
    with col2:
        horario_fim = st.time_input("Horário final", value=pd.to_datetime("23:59").time())

    # Garantir que a coluna esteja em formato datetime.time
    df_temp = df_ceo_filtrado.copy()
    df_temp["horario"] = pd.to_datetime(df_temp["horario"], errors="coerce").dt.time

    df_aba1 = df_temp[
        (df_temp["horario"] >= horario_inicio) &
        (df_temp["horario"] <= horario_fim)
    ]
    st.plotly_chart(ceo_charts.grafico_distribuicao_por_horario(df_aba1), use_container_width=True)

# === ABA 2: Dispositivos e Tecnologia ===
with tabs[1]:
    st.subheader("📱 Dispositivos e Tecnologia")
    st.plotly_chart(ceo_charts.grafico_usuarios_por_modelo(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_tipo_celular(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_usuarios_com_app(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_tipo_celular_por_idade(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_modelo_vs_engajamento(df_ceo_filtrado), use_container_width=True)



# === ABA 3: Localização e Presença ===
with tabs[2]:
    st.subheader("📍 Localização e Presença")
    
    st.plotly_chart(ceo_charts.grafico_mapa_clusters(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_locais_frequentes(df_ceo_filtrado), use_container_width=True)
    # --- Filtro por horário ---
    st.markdown("### Filtro por horário do dia")

    col1, col2 = st.columns(2)
    with col1:
        horario_inicio3 = st.time_input("Horário inicial", key="inicio3", value=pd.to_datetime("00:00").time())
    with col2:
        horario_fim3 = st.time_input("Horário final", key="fim3", value=pd.to_datetime("23:59").time())

    df_temp3 = df_ceo_filtrado.copy()
    df_temp3["horario"] = pd.to_datetime(df_temp3["horario"], errors="coerce").dt.time

    df_aba3 = df_temp3[
        (df_temp3["horario"] >= horario_inicio3) &
        (df_temp3["horario"] <= horario_fim3)
    ]
    st.plotly_chart(ceo_charts.grafico_horario_por_local(df_aba3), use_container_width=True)



# === ABA 4: Engajamento ===
with tabs[3]:
    st.subheader("🎯 Engajamento dos Usuários")
    st.plotly_chart(ceo_charts.grafico_valor_capturado_por_idade(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_valor_por_tipo_cupom(df_ceo_filtrado), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_ticket_medio_por_faixa_etaria(df_ceo_filtrado), use_container_width=True)


# === ABA 5: Campanhas e Comportamento ===
with tabs[4]:
    st.subheader("🏷️ Campanhas e Comportamento")

    # --- Filtro por categoria de loja ---
    st.markdown("### Filtro por categoria de loja")

    categorias = sorted(df_teste_em_massa["categoria_frequentada"].dropna().unique())
    filtro_categoria = st.multiselect(
        "Selecione categorias:",
        options=categorias,
        default=categorias
    )

    df_aba5 = df_teste_em_massa[df_teste_em_massa["categoria_frequentada"].isin(filtro_categoria)]

    st.plotly_chart(ceo_charts.grafico_categorias_frequentes(df_aba5), use_container_width=True)
    st.plotly_chart(ceo_charts.grafico_cupom_x_loja(df_ceo_filtrado), use_container_width=True)

