import streamlit as st
import random
import time
import requests
from fpdf import FPDF
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Validador de SPEI - Banxico", page_icon="🏦")

# --- FUNCIONES AUXILIARES ---

@st.cache_data
def load_logo():
    """Descarga el logotipo oficial de Banxico de una fuente segura."""
    url = "https://www.banxico.org.mx/estaticos/imagenes/sitio/base/logo-banxico-header-superior.png"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

def generate_pdf(clave, banco, monto, estado):
    """Genera un PDF con los detalles de la consulta."""
    pdf = FPDF()
    pdf.add_page()
    
    # Fuentes y diseño básico
    pdf.set_font("Arial", 'B', size=18)
    pdf.cell(200, 10, txt="Comprobante de Consulta SPEI", ln=True, align='C')
    pdf.ln(10) # Salto de línea
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(50, 50, 50)
    
    # Contenido del reporte
    pdf.cell(200, 10, txt=f"Fecha de consulta: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Clave de Rastreo: {clave}", ln=True)
    pdf.cell(200, 10, txt=f"Institución Bancaria: {banco}", ln=True)
    pdf.cell(200, 10, txt=f"Monto: ${monto}", ln=True)
    
    # Destacar el Estado
    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=14)
    if estado == "LIQUIDADO":
        pdf.set_text_color(0, 150, 0) # Verde
    else:
        pdf.set_text_color(200, 0, 0) # Rojo
    
    pdf.cell(200, 10, txt=f"ESTADO DE LA OPERACIÓN: {estado}", ln=True, align='C')

    # Devolver el PDF como bytes para la descarga
    return pdf.output(dest='S') # S de String/Bytes en FPDF2

# --- INTERFAZ DE USUARIO (UI) ---

# 1. Logotipo oficial de Banxico
logo_bytes = load_logo()
if logo_bytes:
    # Mostramos el logo centrado
    st.image(logo_bytes, width=250)
else:
    # Si falla la descarga, mostramos texto
    st.title("🏦 Banco de México")

st.markdown("<h2 style='text-align: center;'>Validador de Consultas SPEI</h2>", unsafe_allow_html=True)
st.markdown("---")

# Formulario de consulta
with st.form("form_banxico"):
    st.subheader("Ingresa los datos del pago")
    clave = st.text_input("Clave de rastreo", placeholder="Ej. 1234567890")
    banco = st.text_input("Institución bancaria", placeholder="Ej. BBVA")
    monto = st.text_input("Monto (MXN)", placeholder="Ej. 1000.50")
    
    submit_button = st.form_submit_button("Consultar Estado")

# --- LÓGICA DE NEGOCIO ---

if submit_button:
    # Validación básica de que los campos no estén vacíos
    if not clave or not banco or not monto:
        st.warning("⚠️ Por favor rellena todos los campos.")
    else:
        # Simulamos la consulta
        with st.spinner("Conectando con Banxico..."):
            time.sleep(2) # Pausa dramática para simulación
            resultado = random.choice(["LIQUIDADO", "RECHAZADO"])
            
        # Mostramos el resultado en pantalla
        if resultado == "LIQUIDADO":
            st.success(f"✅ ¡La operación ha sido procesada con éxito! Estado: {resultado}")
            color_res = "green"
        else:
            st.error(f"❌ La operación no pudo ser procesada. Estado: {resultado}")
            color_res = "red"
            
        st.info(f"Datos recibidos: Clave '{clave}', Banco '{banco}', Monto '{monto}'")
        
        # --- GENERACIÓN Y BOTÓN DE DESCARGA DEL PDF ---
        # Generamos el PDF solo *después* de que se ha hecho la consulta
        pdf_bytes = generate_pdf(clave, banco, monto, resultado)
        
        st.markdown("---")
        st.subheader("Generar Comprobante")
        
        # Botón para descargar el PDF generado
        st.download_button(
            label="📄 Descargar PDF de la consulta",
            data=pdf_bytes,
            file_name=f"consulta_spei_{clave}.pdf",
            mime="application/pdf"
        )
