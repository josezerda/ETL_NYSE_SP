import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title('Ejemplo de aplicación Streamlit en Docker')

# Descripción
st.write("Esta es una aplicación sencilla que se ejecuta dentro de un contenedor Docker.")

# Crear datos de ejemplo para mostrar un gráfico
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# Mostrar los datos como un gráfico de líneas
st.line_chart(chart_data)

# Crear una gráfica de Matplotlib
st.write("Gráfico generado con Matplotlib:")
fig, ax = plt.subplots()
ax.plot(chart_data['A'], label='A')
ax.plot(chart_data['B'], label='B')
ax.plot(chart_data['C'], label='C')
ax.legend()
st.pyplot(fig)

# Entrada del usuario
st.write("Puedes ingresar texto a continuación:")
user_input = st.text_input("Ingresa algo:")
st.write(f"Has ingresado: {user_input}")
