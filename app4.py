# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:26:47 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

# --------------------------
# CONFIGURACIÓN GENERAL
# --------------------------
st.set_page_config(page_title="Evaluación de Desempeño - Javier Pérez", layout="wide")

st.title("📊 Evaluación de Desempeño PbR-SED")
st.markdown("""
#### Elaborado por: **Javier Horacio Pérez Ricárdez**  
📞 **Celular:** +52 56 1056 4095  
✉️ **Postulación para la vacante:** Jefatura de Departamento de Valoración del Desempeño  
""")

st.info("Esta aplicación presenta una simulación de análisis del cumplimiento de metas utilizando herramientas de visualización interactivas en Python.")

# --------------------------
# DATOS SIMULADOS
# --------------------------
entidades = ["CDMX", "Edomex", "Jalisco", "Nuevo León", "Veracruz", "Puebla"]
indicadores = [
    "Educación Básica",
    "Cobertura de Salud",
    "Seguridad Pública",
    "Infraestructura Carretera",
    "Atención a Grupos Vulnerables",
    "Acceso a la Vivienda",
    "Saneamiento Básico",
    "Empleo Formal",
    "Igualdad de Género",
    "Acceso a Internet"
]

np.random.seed(42)
df = pd.DataFrame({
    "Entidad Federativa": np.random.choice(entidades, size=50),
    "Indicador": np.random.choice(indicadores, size=50),
    "Meta Programada (%)": np.random.uniform(70, 100, size=50).round(2),
    "Meta Alcanzada (%)": np.random.uniform(60, 105, size=50).round(2)
})
df["Cumplimiento (%)"] = (df["Meta Alcanzada (%)"] / df["Meta Programada (%)"] * 100).round(2)

# --------------------------
# FILTROS
# --------------------------
st.sidebar.header("🎛️ Filtros")

entidades_seleccionadas = st.sidebar.multiselect(
    "Selecciona las entidades federativas:",
    options=entidades,
    default=entidades
)

indicadores_seleccionados = st.sidebar.multiselect(
    "Selecciona los indicadores:",
    options=indicadores,
    default=indicadores
)

df_filtrado = df[
    (df["Entidad Federativa"].isin(entidades_seleccionadas)) &
    (df["Indicador"].isin(indicadores_seleccionados))
]

# --------------------------
# EXPORTACIÓN DE DATOS
# --------------------------
st.subheader("📤 Exportar Datos Filtrados")

col_csv, col_excel = st.columns(2)

with col_csv:
    csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar CSV",
        data=csv_data,
        file_name='datos_filtrados.csv',
        mime='text/csv'
    )

with col_excel:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, sheet_name='Filtrado', index=False)
    st.download_button(
        label="⬇️ Descargar Excel",
        data=output.getvalue(),
        file_name='datos_filtrados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# --------------------------
# TABLA DE DATOS
# --------------------------
st.subheader("📑 Tabla de Cumplimiento de Metas")
st.dataframe(df_filtrado, use_container_width=True)

# --------------------------
# DISPERSIÓN: META PROGRAMADA VS ALCANZADA
# --------------------------
st.subheader("🎯 Cumplimiento de Metas por Entidad Federativa")

fig = px.scatter(
    df_filtrado,
    x="Meta Programada (%)",
    y="Meta Alcanzada (%)",
    color="Entidad Federativa",
    hover_name="Indicador",
    opacity=0.8
)
fig.update_traces(marker=dict(size=10, symbol="circle"))
fig.add_shape(
    type="line",
    x0=60, x1=105,
    y0=60, y1=105,
    line=dict(color="gray", dash="dash"),
)
fig.update_layout(
    title="Meta Alcanzada vs Meta Programada",
    xaxis_title="Meta Programada (%)",
    yaxis_title="Meta Alcanzada (%)",
    legend_title="Entidad"
)
st.plotly_chart(fig, use_container_width=True)

if not df_filtrado.empty:
    avg_cumplimiento = df_filtrado["Cumplimiento (%)"].mean().round(2)
    st.metric("🔹 Promedio General de Cumplimiento (%)", f"{avg_cumplimiento} %")

# --------------------------
# ANÁLISIS POR INDICADOR
# --------------------------
st.subheader("📈 Comparativa de Cumplimiento por Indicador")

if not df_filtrado.empty:
    df_indicador = df_filtrado.groupby("Indicador")["Cumplimiento (%)"].mean().sort_values(ascending=False).reset_index()

    fig_indicador = px.bar(
        df_indicador,
        x="Indicador",
        y="Cumplimiento (%)",
        color="Cumplimiento (%)",
        color_continuous_scale="Viridis",
        title="Promedio de Cumplimiento por Indicador"
    )
    fig_indicador.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_indicador, use_container_width=True)

    mejor = df_indicador.iloc[0]
    peor = df_indicador.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric("✅ Mejor Indicador", f"{mejor['Indicador']}", f"{mejor['Cumplimiento (%)']:.2f} %")
    col2.metric("⚠️ Peor Indicador", f"{peor['Indicador']}", f"{peor['Cumplimiento (%)']:.2f} %")

# --------------------------
# ANÁLISIS POR ENTIDAD
# --------------------------
st.subheader("🏛️ Comparativa de Cumplimiento por Entidad Federativa")

if not df_filtrado.empty:
    df_entidad = df_filtrado.groupby("Entidad Federativa")["Cumplimiento (%)"].mean().sort_values(ascending=False).reset_index()

    fig_entidad = px.bar(
        df_entidad,
        x="Entidad Federativa",
        y="Cumplimiento (%)",
        color="Cumplimiento (%)",
        color_continuous_scale="Plasma",
        title="Promedio de Cumplimiento por Entidad Federativa"
    )
    st.plotly_chart(fig_entidad, use_container_width=True)

    mejor_ent = df_entidad.iloc[0]
    peor_ent = df_entidad.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric("🏆 Entidad con Mayor Cumplimiento", mejor_ent["Entidad Federativa"], f"{mejor_ent['Cumplimiento (%)']:.2f} %")
    col2.metric("📉 Entidad con Menor Cumplimiento", peor_ent["Entidad Federativa"], f"{peor_ent['Cumplimiento (%)']:.2f} %")

# --------------------------
# OBSERVACIONES AUTOMÁTICAS MEJORADAS
# --------------------------
st.subheader("📝 Observaciones Automáticas")

if not df_filtrado.empty:
    # Calculamos métricas relevantes sobre los datos FILTRADOS
    avg_cumplimiento = df_filtrado["Cumplimiento (%)"].mean()
    max_cumplimiento = df_filtrado["Cumplimiento (%)"].max()
    min_cumplimiento = df_filtrado["Cumplimiento (%)"].min()
    std_cumplimiento = df_filtrado["Cumplimiento (%)"].std()
    
    # Definimos umbrales
    UMBRAL_EXCELENTE = 105
    UMBRAL_SATISFACTORIO = 95
    UMBRAL_ACEPTABLE = 85
    UMBRAL_CRITICO = 70
    
    # Evaluamos diferentes escenarios
    if len(df_filtrado["Entidad Federativa"].unique()) == 1:
        entidad = df_filtrado["Entidad Federativa"].iloc[0]
        st.write(f"**Análisis específico para {entidad}:**")
        
        if avg_cumplimiento > UMBRAL_EXCELENTE:
            st.success(f"🌟 **Excelente desempeño**: {entidad} supera consistentemente las metas (promedio: {avg_cumplimiento:.2f}%).")
            st.write("Recomendación: Documentar buenas prácticas y considerar replicarlas en otras entidades.")
        elif avg_cumplimiento > UMBRAL_SATISFACTORIO:
            st.success(f"✅ **Desempeño satisfactorio**: {entidad} cumple con las expectativas (promedio: {avg_cumplimiento:.2f}%).")
            st.write("Recomendación: Identificar indicadores con menor cumplimiento para mejorar consistencia.")
        elif avg_cumplimiento > UMBRAL_ACEPTABLE:
            st.info(f"📘 **Desempeño aceptable**: {entidad} tiene áreas de oportunidad (promedio: {avg_cumplimiento:.2f}%).")
            st.write("Recomendación: Implementar planes de mejora focalizados en los indicadores críticos.")
        else:
            st.error(f"🚨 **Desempeño crítico**: {entidad} requiere atención inmediata (promedio: {avg_cumplimiento:.2f}%).")
            st.write("Recomendación: Revisión integral de estrategias y asignación de recursos.")
            
    else:  # Análisis general
        if std_cumplimiento > 15:
            st.warning("📊 **Alta variabilidad en cumplimiento**: Existen grandes diferencias entre entidades/indicadores.")
            st.write("Recomendación: Estandarizar procesos en entidades con bajo desempeño y replicar buenas prácticas.")
        
        if avg_cumplimiento > UMBRAL_EXCELENTE:
            st.success(f"🏆 **Excelente cumplimiento global**: {avg_cumplimiento:.2f}% (supera expectativas)")
            st.write("Recomendación: Considerar incrementar metas para el siguiente periodo.")
        elif avg_cumplimiento > UMBRAL_SATISFACTORIO:
            st.success(f"👍 **Cumplimiento satisfactorio**: {avg_cumplimiento:.2f}% (dentro del rango esperado)")
            st.write("Recomendación: Optimizar procesos en indicadores con desempeño medio.")
        elif avg_cumplimiento > UMBRAL_ACEPTABLE:
            st.info(f"📌 **Cumplimiento aceptable**: {avg_cumplimiento:.2f}% (requiere mejoras focalizadas)")
            st.write("Recomendación: Implementar mentoría entre entidades y revisar asignación de recursos.")
        else:
            st.error(f"⚠️ **Cumplimiento insuficiente**: {avg_cumplimiento:.2f}% (por debajo de lo esperado)")
            st.write("Recomendación: Revisión estratégica urgente, posible redefinición de metas y recursos.")
        
        # Análisis de extremos
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🔹 **Mayor cumplimiento**: {max_cumplimiento:.2f}%")
            st.write("Posibles causas: Buenas prácticas, recursos adecuados, metas realistas")
        with col2:
            st.write(f"🔸 **Menor cumplimiento**: {min_cumplimiento:.2f}%")
            st.write("Posibles causas: Subestimación de recursos, metas ambiciosas, problemas operativos")
            
        if (df_filtrado["Cumplimiento (%)"] > 100).any():
            st.info("ℹ️ Algunas entidades/indicadores superan el 100% de cumplimiento. Considerar:")
            st.write("- ¿Metas programadas fueron demasiado conservadoras?")
            st.write("- ¿Se pueden capitalizar estas experiencias exitosas?")
else:
    st.warning("No hay datos disponibles con los filtros actuales. Ajusta los criterios de selección.")

# --------------------------
# PIE DE PÁGINA
# --------------------------
st.markdown("""
---
Aplicación desarrollada por **Javier Horacio Pérez Ricárdez**  
📞 **Celular:** +52 56 1056 4095  
💼 Postulación: Jefatura de Departamento de Valoración del Desempeño (Unidad de Política y Estrategia para Resultados)
""")