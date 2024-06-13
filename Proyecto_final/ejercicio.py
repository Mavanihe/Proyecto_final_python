import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas con GUI
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, Response
import io
import base64

# Generar datos
cliente_id = range(1, 21)
nombres = ['Cliente' + str(i) for i in range(1, 21)]
deuda = np.random.randint(1000, 5000, size=20)
ingreso = np.random.randint(2000, 10000, size=20)
puede_pagar = np.random.choice(['Si', 'No'], size=20)

data = {
    'ClienteID': cliente_id,
    'Nombre': nombres,
    'Deuda': deuda,
    'Ingreso': ingreso,
    'PuedePagar': puede_pagar
}

df = pd.DataFrame(data)

Datos_proyecto_final = 'Datos_proyecto_final.csv'
df.to_csv(Datos_proyecto_final, index=False)

app = Flask(__name__)


def crear_grafico_pie(df):
    clientes_pueden_pagar = df[df['PuedePagar'] == 'Si'].shape[0]
    clientes_no_pueden_pagar = df[df['PuedePagar'] == 'No'].shape[0]
    total_clientes = df.shape[0]
    
    porcentaje_pueden_pagar = (clientes_pueden_pagar / total_clientes) * 100
    porcentaje_no_pueden_pagar = (clientes_no_pueden_pagar / total_clientes) * 100
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.pie([porcentaje_pueden_pagar, porcentaje_no_pueden_pagar], labels=['Pueden Pagar', 'No Pueden Pagar'], colors=['blue', 'red'], autopct='%1.1f%%')
    ax.set_title('Porcentaje de Clientes que Pueden y No Pueden Pagar la Deuda')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    
    return base64.b64encode(img.getvalue()).decode('utf8')

def crear_grafico_barras(df):
    clientes_pueden_pagar = df[df['PuedePagar'] == 'Si'].shape[0]
    clientes_no_pueden_pagar = df[df['PuedePagar'] == 'No'].shape[0]
    total_clientes = df.shape[0]
    
    porcentaje_pueden_pagar = (clientes_pueden_pagar / total_clientes) * 100
    porcentaje_no_pueden_pagar = (clientes_no_pueden_pagar / total_clientes) * 100
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(['Pueden Pagar', 'No Pueden Pagar'], [porcentaje_pueden_pagar, porcentaje_no_pueden_pagar], color=['blue', 'green'])
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Porcentaje')
    ax.set_title('Porcentaje de Clientes que Pueden y No Pueden Pagar la Deuda')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    
    return base64.b64encode(img.getvalue()).decode('utf8')


@app.route('/')
def index():
    
    df = pd.read_csv(Datos_proyecto_final)
    
    
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    grafico_pie = crear_grafico_pie(df)
    grafico_barras = crear_grafico_barras(df)
    
    
    return render_template('index.html', tables=[df.to_html(classes='data', header="true", index=False)], grafico_pie=grafico_pie, grafico_barras=grafico_barras)

if __name__ == '__main__':
    app.run(debug=True)