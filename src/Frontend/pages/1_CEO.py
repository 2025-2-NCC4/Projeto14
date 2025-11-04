import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("👨‍💼 Painel do CEO")

np.random.seed(42)
df = pd.DataFrame({
    "Departamento": ["Vendas", "Marketing", "RH", "TI", "Financeiro"],
    "Lucro": [15000, 12000, 8000, 10000, 13000]
})

fig = px.bar(df, x="Departamento", y="Lucro", color="Lucro", title="Lucro por Departamento")
st.plotly_chart(fig, use_container_width=True)
