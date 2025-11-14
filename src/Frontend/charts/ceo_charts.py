import plotly.express as px
import pandas as pd

PALETA_PICMONEY = {
    "primaria": "#04237D",
    "secundaria": "#44A427",
    "terciaria": "#FABC45",
    "escuro": "#04164C",
    "verde_escuro": "#1E5128",
    "amarelo_escuro": "#C49000"
}

picmoney_scale = [
    [0.0, PALETA_PICMONEY["primaria"]],
    [0.5, PALETA_PICMONEY["secundaria"]],
    [1.0, PALETA_PICMONEY["terciaria"]]
]

SEQUENCIA_PICMONEY = [
    PALETA_PICMONEY["primaria"],
    PALETA_PICMONEY["secundaria"],
    PALETA_PICMONEY["terciaria"]
]

#=========================PRIMEIRA ABA CEO=========================#
# Distribuição por idade
def grafico_usuarios_por_idade(df):
    fig = px.histogram(
        df,
        x="idade",
        nbins=10,
        title="Distribuição de Idade dos Usuários",
        color_discrete_sequence=[PALETA_PICMONEY["secundaria"]]
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


# Distribuição por gênero
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

# Distribuição por horário
def grafico_distribuicao_por_horario(df):
    # Tenta converter para datetime, extrai a hora e remove NaNs
    df_temp = df.copy()
    
    # Tenta converter com formato HH:MM:SS, se falhar, tenta sem formato
    try:
        df_temp["horario"] = pd.to_datetime(df_temp["horario"], format="%H:%M:%S", errors="coerce").dt.hour
    except:
        df_temp["horario"] = pd.to_datetime(df_temp["horario"], errors="coerce").dt.hour
        
    df_temp.dropna(subset=["horario"], inplace=True)
    
    if df_temp.empty:
        return px.bar(title="Dados de horário insuficientes para o gráfico.")

    fig = px.histogram(
        df_temp,
        x="horario",
        nbins=24,
        title="Distribuição de Horários de Uso",
        color_discrete_sequence=[PALETA_PICMONEY["secundaria"]]
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
        bargap=0.25,
        xaxis_title="Horário do Dia",
        yaxis_title="Quantidade de Usuários",
        xaxis=dict(dtick=1, showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )

    return fig

#=========================SEGUNDA ABA CEO=========================#

# Modelos de celular
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


# Tipos de celular
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

# Usuários com App PicMoney
def grafico_usuarios_com_app(df):
    if "possui_app_picmoney" not in df.columns:
        return px.bar(title="Coluna 'possui_app_picmoney' não encontrada.")

    dados = df["possui_app_picmoney"].value_counts().reset_index()
    dados.columns = ["Possui App", "Quantidade"]

    fig = px.pie(
        dados,
        names="Possui App",
        values="Quantidade",
        title="Usuários que Possuem o App PicMoney",
        color_discrete_sequence=["#44A427", "#1E5128"]
    )

    fig.update_layout(
        template="plotly_dark",
        title=dict(x=0.5)
    )

    return fig

# Tipo de celular por idade

def grafico_tipo_celular_por_idade(df):
    if {"idade", "tipo_celular"}.issubset(df.columns):
        fig = px.histogram(
            df,
            x="idade",
            color="tipo_celular",
            barmode="stack",
            title="Distribuição do Tipo de Celular por Idade",
            color_discrete_sequence=[
                PALETA_PICMONEY["verde_escuro"],
                PALETA_PICMONEY["amarelo_escuro"]]
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Idade",
            yaxis_title="Quantidade de Usuários",
            bargap=0.1
        )
    else:
        fig = px.bar(title="Colunas 'idade' ou 'tipo_celular' não encontradas.")

    return fig

# Modelo de celular vs engajamento (valor capturado)
def grafico_modelo_vs_engajamento(df):
    if {"modelo_celular", "ultimo_valor_capturado"}.issubset(df.columns):
        fig = px.box(
            df,
            x="modelo_celular",
            y="ultimo_valor_capturado",
            title="Engajamento por Modelo de Celular (Valor Capturado)",
            color="modelo_celular",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Modelo de Celular",
            yaxis_title="Último Valor Capturado (R$)",
            showlegend=False,
            xaxis=dict(tickangle=-45)
        )
    else:
        fig = px.bar(title="Dados insuficientes para gerar a correlação.")

    return fig



#=========================TERCEIRA ABA CEO=========================#

# Localização (simplificado)
def grafico_distribuicao_local(df_mapa):
    if {"latitude", "longitude"}.issubset(df_mapa.columns):
        fig = px.scatter_mapbox(
            df_mapa,
            lat="latitude",
            lon="longitude",
            color="local",
            hover_name="local",
            zoom=14.4,
            title="Distribuição Geográfica dos Usuários e Capturas",
            color_discrete_sequence=["#23EB05", "#0000FF"]
        )

        fig.update_layout(
            mapbox_style="carto-darkmatter",
            template="plotly_dark",
            width=600,
            height=750,
        )
    else:
        fig = px.bar(title="Nenhuma coordenada encontrada.")

    return fig

# Locais mais frequentes
def grafico_locais_frequentes(df):
    if "local" not in df.columns:
        return px.bar(title="A coluna 'local' não foi encontrada.")

    locais = df["local"].value_counts().reset_index()
    locais.columns = ["Local", "Frequência"]

    fig = px.bar(
        locais,
        x="Local",
        y="Frequência",
        title="Locais Mais Frequentes",
        text="Frequência",
        color="Local",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=1.5,
        marker_line_color="#1E1E1E",
        opacity=0.85
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Local",
        yaxis_title="Frequência",
        showlegend=False,
        xaxis=dict(tickangle=-45)
    )

    return fig

# Heatmap de densidade geográfica
def grafico_heatmap_localizacao(df):
    if {"latitude", "longitude"}.issubset(df.columns):
        fig = px.density_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            radius=25,  # tamanho do raio da "mancha" de calor
            center=dict(lat=df["latitude"].mean(), lon=df["longitude"].mean()),
            zoom=11,
            mapbox_style="carto-darkmatter",
            title="Heatmap de Concentração Geográfica",
            color_continuous_scale=picmoney_scale
        )

        fig.update_layout(
            template="plotly_dark",
            height=750,
            color_continuous_scale=picmoney_scale

        )
        return fig
    else:
        return px.bar(title="Colunas de coordenadas não encontradas.")


# Horário x Local (Heatmap)
def grafico_horario_por_local(df):
    if not {"horario", "local"}.issubset(df.columns):
        return px.bar(title="Colunas necessárias ('horario', 'local') não encontradas.")

    # Conversão do horário para hora (0–23)
    df_temp = df.copy()
    
    # Tenta converter com formato HH:MM:SS, se falhar, tenta sem formato
    try:
        df_temp["horario"] = pd.to_datetime(df_temp["horario"], format="%H:%M:%S", errors="coerce").dt.hour
    except:
        df_temp["horario"] = pd.to_datetime(df_temp["horario"], errors="coerce").dt.hour
        
    # Remove linhas onde a conversão falhou (NaN)
    df_temp.dropna(subset=["horario", "local"], inplace=True)
    
    if df_temp.empty:
        return px.bar(title="Dados insuficientes para o gráfico de Horário por Local.")

    # Agrupar
    matriz = df_temp.groupby(["local", "horario"]).size().reset_index(name="contagem")

    fig = px.density_heatmap(
        matriz,
        x="horario",
        y="local",
        z="contagem",
        color_continuous_scale="Viridis",
        title="Horários Mais Movimentados por Local"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Horário do Dia",
        yaxis_title="Local"
    )

    return fig


# Mapa com clusters
def grafico_mapa_clusters(df):
    if not {"latitude", "longitude"}.issubset(df.columns):
        return px.scatter_mapbox(title="Coordenadas não encontradas.")

    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="local" if "local" in df.columns else None,
        hover_name="local" if "local" in df.columns else None,
        zoom=14.4,
        title="Mapa com Agrupamento de Pontos (Cluster)"
    )

    fig.update_traces(cluster=dict(enabled=True))

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        template="plotly_dark",
        height=750
    )

    return fig


#=========================QUARTA ABA CEO=========================#

# Valor capturado por idade
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

# Valor capturado por tipo de cupom
def grafico_valor_por_tipo_cupom(df):
    if {"ultimo_tipo_cupom", "ultimo_valor_capturado"}.issubset(df.columns):
        dados = df.dropna(subset=["ultimo_tipo_cupom", "ultimo_valor_capturado"])

        fig = px.box(
            dados,
            x="ultimo_tipo_cupom",
            y="ultimo_valor_capturado",
            title="Valor Capturado por Tipo de Cupom",
            color="ultimo_tipo_cupom",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Tipo de Cupom",
            yaxis_title="Valor Capturado (R$)",
            showlegend=False
        )
        return fig
    
    return px.bar(title="Dados insuficientes para gerar este gráfico.")

# Ticket médio por faixa etária
def grafico_ticket_medio_por_faixa_etaria(df):
    if {"idade", "ultimo_valor_capturado"}.issubset(df.columns):
        df = df.dropna(subset=["idade", "ultimo_valor_capturado"])

        bins = [0, 20, 30, 40, 50, 60, 200]
        labels = ["15–20", "21–30", "31–40", "41–50", "51–60", "60+"]

        df["faixa_etaria"] = pd.cut(df["idade"], bins=bins, labels=labels, right=False)

        ticket = df.groupby("faixa_etaria")["ultimo_valor_capturado"].mean().reset_index()
        ticket.columns = ["Faixa Etária", "Ticket Médio"]

        fig = px.bar(
            ticket,
            x="Faixa Etária",
            y="Ticket Médio",
            text="Ticket Médio",
            title="Ticket Médio por Faixa Etária",
            color="Faixa Etária",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            template="plotly_dark",
            yaxis_title="Ticket Médio (R$)",
            showlegend=False
        )
        return fig

    return px.bar(title="Dados insuficientes para gerar este gráfico.")



#=========================QUINTA ABA CEO=========================#

# Categorias mais frequentes
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

# Campanhas por cidade
def grafico_campanhas_por_cidade(df):
    if {"nome_campanha", "cidade_residencial"}.issubset(df.columns):
        dados = df.dropna(subset=["nome_campanha", "cidade_residencial"])

        agrupado = dados.groupby(["cidade_residencial", "nome_campanha"]).size().reset_index(name="Quantidade")

        fig = px.bar(
            agrupado,
            x="cidade_residencial",
            y="Quantidade",
            color="nome_campanha",
            title="Performance das Campanhas por Cidade",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Cidade",
            yaxis_title="Quantidade de Capturas"
        )

        return fig

    return px.bar(title="Dados insuficientes para este gráfico.")

# Mapa de calor por categoria de loja
def mapa_calor_por_categoria(df):
    if {"latitude", "longitude", "ultimo_tipo_loja"}.issubset(df.columns):
        df = df.dropna(subset=["latitude", "longitude", "ultimo_tipo_loja"])

        fig = px.density_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            z=None,
            radius=25,
            center=dict(lat=df["latitude"].mean(), lon=df["longitude"].mean()),
            zoom=11,
            mapbox_style="carto-darkmatter",
            color_continuous_scale="Viridis",
            title="Mapa de Calor por Categoria de Loja",
            hover_data=["ultimo_tipo_loja"]
        )

        fig.update_layout(template="plotly_dark")
        return fig

    return px.bar(title="Dados insuficientes para gerar o mapa de calor.")

# Relação entre tipo de cupom e loja mais capturada
def grafico_cupom_x_loja(df):
    if {"ultimo_tipo_cupom", "ultimo_tipo_loja"}.issubset(df.columns):
        dados = df.dropna(subset=["ultimo_tipo_cupom", "ultimo_tipo_loja"])

        agrupado = dados.groupby(["ultimo_tipo_cupom", "ultimo_tipo_loja"]).size().reset_index(name="Frequência")

        fig = px.treemap(
            agrupado,
            path=["ultimo_tipo_cupom", "ultimo_tipo_loja"],
            values="Frequência",
            title="Relação entre Tipo de Cupom e Loja Mais Capturada",
            color="Frequência",
            color_continuous_scale="Teal"
        )

        fig.update_layout(template="plotly_dark")
        return fig

    return px.bar(title="Dados insuficientes para gerar este gráfico.")
