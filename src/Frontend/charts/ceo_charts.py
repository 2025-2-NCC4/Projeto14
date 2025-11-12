import plotly.express as px

# 1️⃣ Distribuição por idade
def grafico_usuarios_por_idade(df):
    fig = px.histogram(df, x="idade", nbins=10, title="Distribuição de Idade dos Usuários")
    fig.update_layout(template="plotly_dark")
    return fig

# 2️⃣ Distribuição por gênero
def grafico_usuarios_por_genero(df):
    fig = px.pie(df, names="sexo", title="Distribuição por Sexo")
    fig.update_layout(template="plotly_dark")
    return fig

# 3️⃣ Modelos de celular
def grafico_usuarios_por_modelo(df):
    dados = df["modelo_celular"].value_counts().reset_index()
    dados.columns = ["modelo_celular", "quantidade"]
    fig = px.bar(dados, x="modelo_celular", y="quantidade", title="Modelos de Celular mais Utilizados")
    fig.update_layout(template="plotly_dark", xaxis_tickangle=-45)
    return fig

# 4️⃣ Tipos de celular
def grafico_tipo_celular(df):
    if "tipo_celular" in df.columns:
        fig = px.pie(df, names="tipo_celular", title="Distribuição por Tipo de Celular")
    else:
        fig = px.pie(values=[50, 50], names=["Android", "iOS"], title="Distribuição por Tipo de Celular (Exemplo)")
    fig.update_layout(template="plotly_dark")
    return fig

# 5️⃣ Localização (simplificado)
def grafico_distribuicao_local(df):
    if {"latitude", "longitude"}.issubset(df.columns):
        fig = px.scatter_mapbox(
            df,
            lat="latitude", lon="longitude",
            hover_name="local",
            title="Distribuição Geográfica dos Usuários",
            zoom=10,
            color_discrete_sequence=["#00CC96"]
        )
        fig.update_layout(mapbox_style="carto-darkmatter", template="plotly_dark")
    else:
        fig = px.bar(title="Mapa não disponível – faltam coordenadas na base.")
    return fig

# 6️⃣ Valor capturado por idade
def grafico_valor_capturado_por_idade(df):
    if {"idade", "ultimo_valor_capturado"}.issubset(df.columns):
        fig = px.scatter(df, x="idade", y="ultimo_valor_capturado",
                         title="Relação entre Idade e Valor Capturado")
        fig.update_layout(template="plotly_dark")
    else:
        fig = px.bar(title="Dados insuficientes para este gráfico.")
    return fig

# 7️⃣ Categorias mais frequentes (placeholder)
def grafico_categorias_frequentes(df):
    fig = px.bar(x=["Categoria A", "Categoria B", "Categoria C"], y=[100, 60, 40],
                 title="Categorias mais Frequentadas (Exemplo)")
    fig.update_layout(template="plotly_dark")
    return fig
