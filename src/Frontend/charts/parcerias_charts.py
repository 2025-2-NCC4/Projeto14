import plotly.express as px
import pandas as pd


# Função auxiliar para formatar valores em Reais
def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# 1. Gráfico de Receita por Loja/Categoria
def plot_receita_por_categoria(df: pd.DataFrame, group_col: str = "nome_loja"):
    """Cria um gráfico de barras da Receita Líquida por Loja ou Categoria."""

    # Agrupa e soma a receita líquida
    df_grouped = df.groupby(group_col)["valor_liquido"].sum().reset_index()
    df_grouped = df_grouped.sort_values("valor_liquido", ascending=False).head(10)

    # Cria o gráfico
    fig = px.bar(
        df_grouped,
        x="valor_liquido",
        y=group_col,
        orientation="h",
        title=f"Receita Líquida por {group_col.replace('_', ' ').title()}",
        labels={
            "valor_liquido": "Receita Líquida (R$)",
            group_col: group_col.replace("_", " ").title(),
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # Formatação do eixo X para Reais
    fig.update_layout(
        xaxis_tickprefix="R$ ",
        xaxis_tickformat=",.0f",
        yaxis_autorange="reversed",
        hovermode="y unified",
    )

    return fig


# 2. Gráfico de Desconto por Loja/Categoria
def plot_desconto_por_categoria(df: pd.DataFrame, group_col: str = "nome_loja"):
    """Cria um gráfico de pizza da distribuição do Desconto Concedido por Loja ou Categoria."""

    # Agrupa e soma o desconto
    df_grouped = df.groupby(group_col)["valor_cupom"].sum().reset_index()
    df_grouped = df_grouped.sort_values("valor_cupom", ascending=False).head(10)

    # Cria o gráfico de pizza
    fig = px.pie(
        df_grouped,
        values="valor_cupom",
        names=group_col,
        title=f"Distribuição do Desconto por {group_col.replace('_', ' ').title()}",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    fig.update_traces(textinfo="percent+label")
    fig.update_layout(showlegend=True)

    return fig


# 3. Gráfico de Evolução Mensal da Receita
def plot_evolucao_mensal_receita(df: pd.DataFrame):
    """Cria um gráfico de linha da evolução mensal da Receita Líquida."""

    if "data_captura" not in df.columns:
        return px.line(title="Evolução Mensal: Coluna 'data_captura' não encontrada.")

    df["mes_ano"] = df["data_captura"].dt.to_period("M").astype(str)
    df_grouped = df.groupby("mes_ano")["valor_liquido"].sum().reset_index()

    fig = px.line(
        df_grouped,
        x="mes_ano",
        y="valor_liquido",
        title="Evolução Mensal da Receita Líquida",
        labels={"valor_liquido": "Receita Líquida (R$)", "mes_ano": "Mês/Ano"},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    fig.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.0f",
        xaxis_title="Mês/Ano",
        hovermode="x unified",
    )

    return fig


# 4. Gráfico de Margem por Loja/Categoria (Mantido, mas pode não ser usado no 3_PARCERIAS.py)
def plot_margem_por_categoria(df: pd.DataFrame, group_col: str = "nome_loja"):
    """Cria um gráfico de barras da Margem por Loja ou Categoria."""

    df_grouped = (
        df.groupby(group_col)
        .agg(
            total_liquido=("valor_liquido", "sum"), total_compra=("valor_compra", "sum")
        )
        .reset_index()
    )

    # Calcula a margem (simplificada)
    df_grouped["margem"] = (
        df_grouped["total_liquido"] / df_grouped["total_compra"]
    ) * 100
    df_grouped = df_grouped.sort_values("margem", ascending=False).head(10)

    fig = px.bar(
        df_grouped,
        x="margem",
        y=group_col,
        orientation="h",
        title=f"Margem por {group_col.replace('_', ' ').title()}",
        labels={"margem": "Margem (%)", group_col: group_col.replace("_", " ").title()},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    fig.update_layout(
        xaxis_ticksuffix="%",
        yaxis_autorange="reversed",
        hovermode="y unified",
    )

    return fig


# 5. Gráfico de Ticket Médio por Loja/Categoria
def plot_ticket_medio_por_categoria(df: pd.DataFrame, group_col: str = "nome_loja"):
    """Cria um gráfico de barras do Ticket Médio por Loja ou Categoria."""

    df_grouped = df.groupby(group_col)["valor_compra"].mean().reset_index()
    df_grouped = df_grouped.sort_values("valor_compra", ascending=False).head(10)

    fig = px.bar(
        df_grouped,
        x="valor_compra",
        y=group_col,
        orientation="h",
        title=f"Ticket Médio por {group_col.replace('_', ' ').title()}",
        labels={
            "valor_compra": "Ticket Médio (R$)",
            group_col: group_col.replace("_", " ").title(),
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    fig.update_layout(
        xaxis_tickprefix="R$ ",
        xaxis_tickformat=",.2f",
        yaxis_autorange="reversed",
        hovermode="y unified",
    )

    return fig
