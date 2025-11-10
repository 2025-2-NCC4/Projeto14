import plotly.express as px

def grafico_usuarios_por_idade(df):
    fig = px.histogram(df, x="idade", nbins=10, title="Distribuição de Idade dos Usuários")
    fig.update_layout(template="plotly_dark")
    return fig

def grafico_usuarios_por_genero(df):
    fig = px.pie(df, names="sexo", title="Distribuição por Sexo")
    fig.update_layout(template="plotly_dark")
    return fig

def grafico_usuarios_por_modelo(df):
    dados = df["modelo_celular"].value_counts().reset_index()
    dados.columns = ["modelo_celular", "quantidade"]

    fig = px.bar(
        dados,
        x="modelo_celular",
        y="quantidade",
        title="Modelos de Celular mais Utilizados"
    )
    fig.update_layout(template="plotly_dark")
    return fig
