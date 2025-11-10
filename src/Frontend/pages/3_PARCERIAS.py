import streamlit as st
import plotly.io as pio
pio.templates.default = "plotly_dark"

st.subheader("Empresas Parceiras")

empresas = [
 "SmartFit", "Outback", "Madero", "Havaianas",
 "Spoleto", "Cacau Show", "Natura", "Cinemark"
 ]
for empresa in empresas:
     st.write(f"- {empresa}")