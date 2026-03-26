import streamlit as st
import random
import time

# Configuración institucional
st.set_page_config(page_title="Banxico SPEI", page_icon="🏦")

st.markdown("<h1 style='text-align: center;'>BANXICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #BDA87F;'>Validación de Pagos SPEI</h3>", unsafe_allow_html=True)

with st.form("form_banxico"):
    clave = st.text_input("Clave de Rastreo", placeholder="Ingresa los 20 dígitos")
    banco = st.text_input("Institución Receptora", placeholder="Ej: HSBC")
    monto = st.text_input("Monto (Opcional)", placeholder="$ 0.00")
    enviar = st.form_submit_button("CONSULTAR ESTATUS")

if enviar:
    with st.spinner("Conectando con Banxico..."):
        time.sleep(2)
        resultado = random.choice(["LIQUIDADO", "EN PROCESO", "DEVUELTO"])
        if resultado == "LIQUIDADO":
            st.success(f"✅ Estatus: {resultado}. El pago ha sido validado.")
        else:
            st.warning(f"⚠️ Estatus: {resultado}. Verifique con su banco.")
