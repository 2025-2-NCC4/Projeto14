import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Funções de Visualização ---

def create_kpi_card(title, value, delta=None, help_text=None):
    """Cria um cartão KPI."""
    # Formatação para moeda brasileira (R$ X.XXX,XX)
    formatted_value = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    if delta is not None:
        # Formatação para porcentagem
        formatted_delta = f"{delta:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric(label=title, value=formatted_value, delta=formatted_delta, help=help_text)
    else:
        st.metric(label=title, value=formatted_value, help=help_text)

def plot_time_series(df, y_col, title):
    """Plota série temporal de uma métrica."""
    df_plot = df.groupby('data_captura')[y_col].sum().reset_index()
    fig = px.line(df_plot, x='data_captura', y=y_col, title=title,
                  labels={'data_captura': 'Data', y_col: 'Valor (R$)'},
                  template='plotly_white')
    fig.update_layout(hovermode="x unified")
    return fig

def plot_bar_chart(df, x_col, y_col, title, n_top=10):
    """Plota gráfico de barras para as top N categorias."""
    df_plot = df.groupby(x_col)[y_col].sum().nlargest(n_top).reset_index()
    df_plot = df_plot.sort_values(y_col, ascending=True)
    
    fig = px.bar(df_plot, x=y_col, y=x_col, orientation='h', title=title,
                 labels={y_col: 'Valor (R$)', x_col: 'Categoria'},
                 template='plotly_white')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_pie_chart(df, names_col, values_col, title):
    """Plota gráfico de pizza para distribuição."""
    df_plot = df.groupby(names_col)[values_col].sum().reset_index()
    fig = px.pie(df_plot, names=names_col, values=values_col, title=title,
                 hole=.3, template='plotly_white')
    return fig

def plot_age_gender_distribution(df_user_summary):
    """Plota o histograma de distribuição de usuários por idade e sexo."""
    fig = px.histogram(df_user_summary, x='idade', color='sexo',
                       title='Distribuição de Usuários por Idade e Sexo',
                       labels={'idade': 'Idade', 'count': 'Número de Usuários'},
                       template='plotly_white',
                       barmode='overlay')
    return fig

def plot_top_categories(df_filtered):
    """Plota o gráfico de barras das Top 10 Categorias Frequentadas por Receita Líquida."""
    df_cat = df_filtered.groupby('categoria_frequentada')['valor_liquido'].sum().nlargest(10).reset_index()
    df_cat = df_cat.sort_values('valor_liquido', ascending=True)

    fig = px.bar(df_cat, x='valor_liquido', y='categoria_frequentada', orientation='h',
                 title='Top 10 Categorias por Receita Líquida',
                 labels={'valor_liquido': 'Receita Líquida (R$)', 'categoria_frequentada': 'Categoria'},
                 template='plotly_white')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# --- Novas Funções de Análise de Segmento ---

def plot_segment_metric(df, segment_col, metric_col, title, sort_ascending=True):
    """Plota gráfico de barras para uma métrica por segmento."""
    df_plot = df.groupby(segment_col)[metric_col].mean().sort_values(ascending=sort_ascending).reset_index()
    
    # Formatação do eixo Y dependendo da métrica
    if metric_col == 'margem_cupom':
        labels = {metric_col: 'Margem de Cupom (%)', segment_col: 'Segmento'}
        hover_data = {metric_col: ':.2f'}
    elif metric_col == 'valor_compra':
        labels = {metric_col: 'Ticket Médio (R$)', segment_col: 'Segmento'}
        hover_data = {metric_col: ':.2f'}
    else:
        labels = {metric_col: 'Valor', segment_col: 'Segmento'}
        hover_data = None

    fig = px.bar(df_plot, x=segment_col, y=metric_col, title=title,
                 labels=labels,
                 hover_data=hover_data,
                 template='plotly_white')
    fig.update_xaxes(tickangle=45)
    return fig

def plot_segment_roi(df):
    """Plota o Retorno sobre o Investimento (ROI) por Tipo de Loja."""
    df_roi = df.groupby('tipo_loja').agg(
        total_liquido=('valor_liquido', 'sum'),
        total_cupom=('valor_cupom', 'sum')
    ).reset_index()
    
    # ROI = (Receita Líquida - Custo do Cupom) / Custo do Cupom
    # Simplificando para Receita Líquida / Custo do Cupom (para ver o retorno por R$ gasto)
    df_roi['roi'] = df_roi['total_liquido'] / df_roi['total_cupom']
    df_roi = df_roi.sort_values('roi', ascending=False).head(10)

    fig = px.bar(df_roi, x='tipo_loja', y='roi', title='Top 10 Tipos de Loja por Retorno (Receita Líquida / Desconto)',
                 labels={'tipo_loja': 'Tipo de Loja', 'roi': 'ROI (Receita Líquida / Desconto)'},
                 template='plotly_white')
    fig.update_xaxes(tickangle=45)
    return fig

def plot_segment_time_series(df, segment_col, metric_col, title):
    """Plota série temporal de uma métrica para os top 5 segmentos."""
    # Identificar os top 5 segmentos por valor_liquido
    top_segments = df.groupby(segment_col)['valor_liquido'].sum().nlargest(5).index.tolist()
    df_filtered = df[df[segment_col].isin(top_segments)]
    
    df_plot = df_filtered.groupby(['data_captura', segment_col])[metric_col].sum().reset_index()
    
    fig = px.line(df_plot, x='data_captura', y=metric_col, color=segment_col, title=title,
                  labels={'data_captura': 'Data', metric_col: 'Valor (R$)', segment_col: 'Segmento'},
                  template='plotly_white')
    fig.update_layout(hovermode="x unified")
    return fig

def plot_concentration_analysis(df):
    """Plota a análise de concentração (Pareto) da Receita Líquida por Tipo de Loja."""
    df_loja = df.groupby('tipo_loja')['valor_liquido'].sum().sort_values(ascending=False).reset_index()
    df_loja['receita_acumulada'] = df_loja['valor_liquido'].cumsum()
    df_loja['perc_acumulado'] = (df_loja['receita_acumulada'] / df_loja['valor_liquido'].sum()) * 100
    df_loja['perc_lojas'] = (df_loja.index + 1) / len(df_loja) * 100

    fig = go.Figure()

    # Coluna de Receita Líquida
    fig.add_trace(go.Bar(
        x=df_loja['tipo_loja'],
        y=df_loja['valor_liquido'],
        name='Receita Líquida',
        yaxis='y1',
        marker_color='rgba(50, 171, 96, 0.6)'
    ))

    # Linha de Percentual Acumulado (Pareto)
    fig.add_trace(go.Scatter(
        x=df_loja['tipo_loja'],
        y=df_loja['perc_acumulado'],
        name='Percentual Acumulado',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(size=5)
    ))

    fig.update_layout(
        title='Análise de Concentração (Pareto) da Receita Líquida por Tipo de Loja',
        xaxis=dict(title='Tipo de Loja', tickangle=45),
        yaxis=dict(title='Receita Líquida (R$)', side='left', showgrid=False),
        yaxis2=dict(title='Percentual Acumulado (%)', side='right', overlaying='y', range=[0, 100], showgrid=True),
        template='plotly_white',
        legend=dict(x=0.1, y=1.1, orientation='h')
    )
    return fig

def plot_coupon_type_heatmap(df):
    """Plota um heatmap da Receita Líquida por Tipo de Loja e Tipo de Cupom."""
    df_pivot = df.groupby(['tipo_loja', 'tipo_cupom'])['valor_liquido'].sum().unstack(fill_value=0)
    
    fig = px.imshow(df_pivot, 
                    text_auto=".2s", 
                    aspect="auto",
                    color_continuous_scale='Viridis',
                    title='Receita Líquida por Tipo de Loja e Tipo de Cupom (Heatmap)')
    fig.update_xaxes(title='Tipo de Cupom')
    fig.update_yaxes(title='Tipo de Loja')
    return fig

def plot_ticket_discount_scatter(df):
    """Plota um scatter plot comparando Ticket Médio e Desconto Médio por Tipo de Loja."""
    df_agg = df.groupby('tipo_loja').agg(
        ticket_medio=('valor_compra', 'mean'),
        desconto_medio=('valor_cupom', 'mean'),
        num_cupons=('valor_cupom', 'count')
    ).reset_index()

    fig = px.scatter(df_agg, x='ticket_medio', y='desconto_medio', 
                     size='num_cupons', color='tipo_loja',
                     hover_name='tipo_loja',
                     title='Ticket Médio vs. Desconto Médio por Tipo de Loja',
                     labels={'ticket_medio': 'Ticket Médio (R$)', 'desconto_medio': 'Desconto Médio (R$)'},
                     template='plotly_white')
    fig.update_layout(showlegend=False)
    return fig

# --- Novas Funções de KPIs e Análise Temporal ---

def plot_average_time_series(df, y_col, title):
    """Plota série temporal da média de uma métrica (Ticket Médio, Desconto Médio)."""
    df_plot = df.groupby('data_captura')[y_col].mean().reset_index()
    
    # Renomear coluna para clareza no gráfico
    if y_col == 'valor_compra':
        y_label = 'Ticket Médio (R$)'
    elif y_col == 'valor_cupom':
        y_label = 'Desconto Médio (R$)'
    else:
        y_label = 'Valor Médio (R$)'

    fig = px.line(df_plot, x='data_captura', y=y_col, title=title,
                  labels={'data_captura': 'Data', y_col: y_label},
                  template='plotly_white')
    fig.update_layout(hovermode="x unified")
    return fig

def plot_day_of_week_analysis(df, y_col, title):
    """Plota a distribuição de uma métrica por dia da semana."""
    # Definir a ordem correta dos dias da semana
    dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_pt = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    
    df_plot = df.groupby('dia_semana')[y_col].sum().reindex(dias_ordem).reset_index()
    df_plot['dia_semana_pt'] = df_plot['dia_semana'].map(dict(zip(dias_ordem, dias_pt)))

    fig = px.bar(df_plot, x='dia_semana_pt', y=y_col, title=title,
                 labels={'dia_semana_pt': 'Dia da Semana', y_col: 'Valor (R$)'},
                 template='plotly_white')
    return fig

def plot_stacked_area_time_series(df, metric_col, title):
    """Plota série temporal de uma métrica, segmentada por tipo de cupom (Stacked Area)."""
    df_plot = df.groupby(['data_captura', 'tipo_cupom'])[metric_col].sum().reset_index()
    
    # Renomear coluna para clareza no gráfico
    if metric_col == 'valor_liquido':
        y_label = 'Receita Líquida (R$)'
    elif metric_col == 'valor_cupom':
        y_label = 'Desconto Concedido (R$)'
    else:
        y_label = 'Valor (R$)'

    fig = px.area(df_plot, x='data_captura', y=metric_col, color='tipo_cupom',
                  title=title,
                  labels={'data_captura': 'Data', metric_col: y_label, 'tipo_cupom': 'Tipo de Cupom'},
                  template='plotly_white')
    fig.update_layout(hovermode="x unified")
    return fig
