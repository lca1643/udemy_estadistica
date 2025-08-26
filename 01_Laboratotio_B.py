import streamlit as st
import pandas as pd
import io
import plotly.express as px

# --- 1. Configuración de la Página y Estilos ---
st.set_page_config(
    page_title="Generador de Gráfico de Barras",
    page_icon="🧪",
    layout="wide"
)

# --- CSS para personalización ---
st.markdown(
    """
    <style>
    .header-container {
        background-color: #094C72;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
    }
    
    .info-box {
        background-color: #094C72;
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        font-size: 16px;
        border-left: 4px solid #0B5A8A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-box svg {
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .stDownloadButton > button {
        background-color: #094C72 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #0B5A8A !important;
        color: white !important;
    }
    
    .stDownloadButton > button:focus {
        background-color: #094C72 !important;
        color: white !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- ENCABEZADO ---
st.markdown("""
<div class="header-container">
    <h1 style='margin: 5px 0;'>Curso de Fundamentos de Estadística</h1>
    <h2 style='margin: 5px 0;'>Udemy</h2>
    <p style='margin: 5px 0; font-size: 25px;'><strong>Luis Corona Alcantar</strong></p>
    <p style='margin: 5px 0; font-size: 20px;'>lca1643@gmail.com</p>
    <hr style='border: 2px solid rgba(255,255,255,0.3); margin: 20px 0;'>
    <h1 style='font-size: 50px; margin: 0;'>🧪 0.1 Laboratorio de Estadística</h1>
    <h2 style='font-size: 40px; margin: 10px 0;'>📊 Generador de Gráfico de Barras</h2>
</div>
""", unsafe_allow_html=True)

# --- INSTRUCCIONES ---
st.header("INSTRUCCIONES")
st.markdown("""
1. Cargar un archivo CSV o Excel  
2. Elegir una columna con datos categóricos (texto)  
3. Elegir una columna con datos numéricos  
4. Configurar las opciones del gráfico  
""")

st.markdown("---")

# --- SECCIÓN 1: CARGAR ARCHIVO ---
st.header("1. Cargar Archivo de Datos")

uploaded_file = st.file_uploader(
    "Carga tu archivo (CSV o Excel)",
    type=["csv", "xlsx"]
)

df = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("¡Archivo cargado exitosamente!")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# --- MOSTRAR VISTA PREVIA ---
if df is not None:
    st.header("Vista Previa de los Datos")
    st.dataframe(df.head())
    
    # --- SECCIÓN 2: CONFIGURACIÓN ---
    st.header("2. Configuración del Gráfico")
    
    columnas = df.columns.tolist()
    label_col = st.selectbox(
        "Columna para Etiquetas/Categorías:",
        columnas,
        help="Selecciona la columna que contiene las categorías (texto)"
    )
    value_col = st.selectbox(
        "Columna para Valores Numéricos:",
        columnas,
        index=1 if len(columnas) > 1 else 0,
        help="Selecciona la columna que contiene los valores numéricos"
    )

    # --- ORDEN ---
    sort_order = st.selectbox(
        "Ordenar datos:",
        ["De mayor a menor", "De menor a mayor"]
    )
    
    # --- PERSONALIZAR ---
    st.markdown("### Personalizar")
    
    default_title = f"Distribución de {value_col}"
    custom_title = st.text_input("Título del gráfico:", value=default_title)
    custom_xlabel = st.text_input("Título eje X:", value=label_col)
    custom_ylabel = st.text_input("Título eje Y:", value=value_col)
    
    # --- OPCIONES DE COLOR ---
    st.markdown("### Colores")
    color_mode = st.radio(
        "Seleccionar modo de color:",
        ["Paleta automática", "Color fijo"]
    )
    
    if color_mode == "Paleta automática":
        palette = st.selectbox(
            "Selecciona una paleta de colores:",
            ["viridis", "plasma", "cividis", "coolwarm", "Set2", "tab10"]
        )
    else:
        fixed_color = st.color_picker("Elige un color fijo para las barras", "#1f77b4")

    # --- GENERAR GRÁFICO ---
    if pd.api.types.is_numeric_dtype(df[value_col]):
        
        st.markdown("---")
        st.header("3. Resultado del Gráfico")
        
        processed_data = df.groupby(label_col)[value_col].sum().reset_index()
        
        if sort_order == "De mayor a menor":
            processed_data = processed_data.sort_values(by=value_col, ascending=False)
        else:
            processed_data = processed_data.sort_values(by=value_col, ascending=True)

        # --- Construcción del gráfico con Plotly ---
        if color_mode == "Paleta automática":
            palette_map = {
                "viridis": px.colors.sequential.Viridis,
                "plasma": px.colors.sequential.Plasma,
                "cividis": px.colors.sequential.Cividis,
                "coolwarm": px.colors.diverging.RdBu,
                "Set2": px.colors.qualitative.Set2,
                "tab10": px.colors.qualitative.T10
            }
            colors = palette_map.get(palette, px.colors.qualitative.T10)
            fig = px.bar(
                processed_data,
                x=label_col,
                y=value_col,
                color=label_col,
                color_discrete_sequence=colors,
                text=processed_data[value_col]
            )
        else:
            fig = px.bar(
                processed_data,
                x=label_col,
                y=value_col,
                color_discrete_sequence=[fixed_color],
                text=processed_data[value_col]
            )

        # --- Ajustes visuales minimalistas ---
        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside"
        )
        fig.update_layout(
            title=custom_title,
            xaxis_title=custom_xlabel,
            yaxis_title=custom_ylabel,
            title_font=dict(size=22, family="Arial", color="black"),
            xaxis=dict(tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
            plot_bgcolor="white",
            bargap=0.2,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- Exportar imagen ---
        buf = io.BytesIO()
        fig.write_image(buf, format="png", scale=2)
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf.getvalue(),
            file_name=f"{value_col.replace(' ', '_').lower()}_chart.png",
            mime="image/png",
            use_container_width=True
        )
        
    else:
        st.error(f"❌ Error: La columna '{value_col}' no es numérica. Por favor, elige una columna con números.")

# --- INFORMACIÓN CUANDO NO HAY ARCHIVO ---
else:
    st.markdown(
        """
        <div class="info-box">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <div>Esperando a que se cargue un archivo de datos para generar el gráfico de barras.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.expander("💡 ¿Qué formato debe tener mi archivo?"):
        st.markdown("""
        - Tu archivo puede ser un **CSV** o **Excel** (.xlsx, .xls)  
        - Debe tener una **columna de encabezados** en la primera fila  
        - Asegúrate de tener al menos:  
          - Una columna con **texto** (categorías/etiquetas)  
          - Una columna con **números** (valores a graficar)  
        
        **Ejemplo de estructura:**
        
        | Producto | Ventas |
        |----------|--------|
        | A        | 100    |
        | B        | 150    |
        | C        | 80     |
        """)
