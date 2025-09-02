import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página y Estilos ---
st.set_page_config(
    page_title="Generador de Gráfico de Barras",
    page_icon="🧪",
    layout="wide"
)

# --- Función para ocultar elementos de Streamlit ---
def hide_streamlit_elements():
    """Función para ocultar elementos de Streamlit"""
    hide_css = """
    <style>
    /* Ocultar el menú principal */
    #MainMenu {visibility: hidden;}
    
    /* Ocultar el footer */
    footer {visibility: hidden;}
    
    /* Ocultar el header */
    header {visibility: hidden;}
    
    /* Ocultar los botones de acción (compartir, etc.) */
    .stActionButton {display: none !important;}
    
    /* Ocultar la barra de herramientas */
    [data-testid="stToolbar"] {display: none !important;}
    
    /* Ocultar elementos de decoración */
    [data-testid="stDecoration"] {display: none !important;}
    
    /* Ocultar el widget de estado */
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Ocultar el botón "Deploy" si aparece */
    [data-testid="stHeaderActionElements"] {display: none !important;}
    
    /* Método alternativo para versiones más recientes */
    .st-emotion-cache-1wmy9hl {display: none !important;}
    .st-emotion-cache-1hskohh {display: none !important;}
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)

# Aplicar la función para ocultar elementos
hide_streamlit_elements()

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
    
    # Analizar tipos de datos de las columnas
    columnas_categoricas = []
    columnas_numericas = []
    
    for col in columnas:
        if pd.api.types.is_numeric_dtype(df[col]):
            columnas_numericas.append(col)
        else:
            columnas_categoricas.append(col)
    
    # Selectbox para columna de etiquetas con validación
    label_col = st.selectbox(
        "Columna para Etiquetas/Categorías:",
        columnas,
        help="Selecciona la columna que contiene las categorías (texto)"
    )
    
    # Verificar si la columna seleccionada es apropiada para etiquetas
    if pd.api.types.is_numeric_dtype(df[label_col]):
        st.warning(f"⚠️ **Advertencia**: La columna '{label_col}' contiene números. Para etiquetas es recomendable usar columnas con texto.")
        if columnas_categoricas:
            st.info(f"💡 **Sugerencia**: Considera usar alguna de estas columnas de texto: {', '.join(columnas_categoricas)}")
    
    # Selectbox para columna de valores con validación
    value_col = st.selectbox(
        "Columna para Valores Numéricos:",
        columnas,
        index=1 if len(columnas) > 1 else 0,
        help="Selecciona la columna que contiene los valores numéricos"
    )
    
    # Verificar si la columna seleccionada es numérica
    if not pd.api.types.is_numeric_dtype(df[value_col]):
        st.error(f"❌ **Error**: La columna '{value_col}' no contiene números. Por favor, selecciona una columna numérica.")
        if columnas_numericas:
            st.info(f"💡 **Sugerencia**: Estas columnas contienen números: {', '.join(columnas_numericas)}")
        st.stop()  # Detener la ejecución hasta que se seleccione una columna válida

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
    # La validación ya se hizo arriba, así que podemos proceder directamente
    st.markdown("---")
    st.header("3. Resultado del Gráfico")
    
    processed_data = df.groupby(label_col)[value_col].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if sort_order == "De mayor a menor":
        processed_data = processed_data.sort_values(by=value_col, ascending=False)
    else:
        processed_data = processed_data.sort_values(by=value_col, ascending=True)
    
    num_bars = len(processed_data)
    
    if color_mode == "Paleta automática":
        colors = plt.get_cmap(palette)(np.linspace(0.2, 0.8, num_bars))
    else:
        colors = [fixed_color] * num_bars
    
    bars = ax.bar(processed_data[label_col], processed_data[value_col], color=colors)
    
    for bar in bars:
        height = bar.get_height()
        label_text = f'{height:.1%}' if (height < 1 and height > 0) else f'{height:,.0f}'
        ax.text(bar.get_x() + bar.get_width() / 2, height, label_text,
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel(custom_xlabel, fontsize=12)
    ax.set_ylabel(custom_ylabel, fontsize=12)
    ax.set_title(custom_title, fontsize=18, fontweight='bold', pad=20)
    
    plt.xticks(rotation=45, ha="right")
    if not processed_data.empty:
        ax.set_ylim(0, processed_data[value_col].max() * 1.15)
    
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    fig.tight_layout()

    st.pyplot(fig)
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf.getvalue(),
        file_name=f"{value_col.replace(' ', '_').lower()}_chart.png",
        mime="image/png",
        use_container_width=True
    )

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
