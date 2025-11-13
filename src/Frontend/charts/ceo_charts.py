import plotly.express as px

# 1 Distribuição por idade
def grafico_usuarios_por_idade(df):
    fig = px.histogram(
        df,
        x="idade",
        nbins=10,
        title="Distribuição de Idade dos Usuários",
        color_discrete_sequence=["#44A427"]
    )

    fig.update_traces(
        marker_line_color="#1E1E1E",
        marker_line_width=1.5,
        opacity=0.8
    )

    fig.update_layout(
        template="plotly_dark",
        font=dict(color="white", size=14),
        title=dict(x=0.5, font=dict(size=22)),
        bargap=0.3,
        xaxis_title="Idade (anos)",
        yaxis_title="Número de Usuários",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )

    return fig


# 2 Distribuição por gênero
def grafico_usuarios_por_genero(df):
    fig = px.pie(
        df,
        names="sexo",
        title="Distribuição por Sexo",
        color_discrete_sequence=["#76FE4D", "#44A427", "#31721D"]
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# 3 Modelos de celular
def grafico_usuarios_por_modelo(df):
    dados = df["modelo_celular"].value_counts().reset_index()
    dados.columns = ["modelo_celular", "quantidade"]

    fig = px.bar(
        dados,
        x="modelo_celular",
        y="quantidade",
        title="Modelos de Celular mais Utilizados",
        color_discrete_sequence=["#04237D"]
    )

    fig.update_traces(
        opacity=0.8,
        marker_line_color="#1E1E1E",
        marker_line_width=1.5
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_tickangle=-45
    )

    return fig


# 4 Tipos de celular
def grafico_tipo_celular(df):
    if "tipo_celular" in df.columns:
        fig = px.pie(
            df,
            names="tipo_celular",
            title="Distribuição por Tipo de Celular",
            color_discrete_sequence=["#04237D", "#04164C"]
        )
    else:
        fig = px.pie(
            values=[50, 50],
            names=["Android", "iOS"],
            title="Distribuição por Tipo de Celular (Exemplo)"
        )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig


# 5 Localização (simplificado)
def grafico_distribuicao_local(df):
    if {"latitude", "longitude"}.issubset(df.columns):
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            hover_name="local",
            title="Distribuição Geográfica dos Usuários",
            zoom=14.4,
            color_discrete_sequence=["#FABC45"]
        )

        fig.update_layout(
            mapbox_style="carto-darkmatter",
            template="plotly_dark",
            width=600,
            height=750,
        )
    else:
        fig = px.bar(
            title="Mapa não disponível – faltam coordenadas na base."
        )

    return fig


# 6 Valor capturado por idade
def grafico_valor_capturado_por_idade(df):
    if {"idade", "ultimo_valor_capturado"}.issubset(df.columns):
        fig = px.box(
            df,
            x="idade",
            y="ultimo_valor_capturado",
            title="Relação entre Idade e Valor Capturado",
            color_discrete_sequence=["#0A2E9C"]
        )

        fig.update_traces(
            marker=dict(
                size=8, 
                opacity=0.8, 
                line=dict(width=1, color="#1E1E1E"))
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Idade (anos)",
            yaxis_title="Último Valor Capturado (R$)"
        )
    else:
        fig = px.bar(
            title="Dados insuficientes para este gráfico."
        )

    return fig


# 7 Categorias mais frequentes (placeholder)
def grafico_categorias_frequentes(df_teste_em_massa):
    if "categoria_frequentada" in df_teste_em_massa.columns:
        # Contar as categorias mais frequentes
        categorias = df_teste_em_massa["categoria_frequentada"].value_counts().reset_index()
        categorias.columns = ["Categoria", "Frequência"]

        fig = px.bar(
            categorias,
            x="Categoria",
            y="Frequência",
            title="Categorias Mais Frequentadas",
            text="Frequência",
            color="Categoria",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=1.5,
            marker_line_color="#1E1E1E"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Categoria",
            yaxis_title="Número de Registros",
            showlegend=False
        )
    else:
        fig = px.bar(title="Coluna 'categoria_frequentada' não encontrada.")

    return fig

