import streamlit as st
import requests
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def gera_grafico_mensal(moeda, valor_atual):
    # Simulando dados para os últimos 30 dias
    dias = [datetime.now() - timedelta(days=i) for i in range(30)][::-1]  # Últimos 30 dias
    variacao = np.random.normal(loc=0, scale=0.02, size=30)  # Variação diária aleatória em torno de 0
    valores = valor_atual * (1 + np.cumsum(variacao))  # Simulação da variação cumulativa

    # Criando o gráfico de linha para evolução mensal com Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dias, y=valores, mode='lines+markers', name=moeda, line=dict(color='blue')))

    # Adicionando o valor atual da moeda como texto no gráfico
    fig.add_annotation(
        x=dias[-1], 
        y=valores[-1],
        text=f'{moeda}: R${valor_atual:.2f}',
        showarrow=True,
        arrowhead=1
    )

    # Customizando o gráfico
    fig.update_layout(
        title=f'Evolução Mensal do {moeda}',
        xaxis_title='Data',
        yaxis_title='Valor em BRL',
        xaxis_rangeslider_visible=True,
        template='plotly_dark'
    )

    return fig

# Configurando o layout do Streamlit
st.set_page_config(page_title="Cotações de Moedas", layout="wide")

# Título da página
st.title("Cotações de Moedas")

# Obtendo cotações
cotacao = requests.get(f"https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
cotacao = cotacao.json()

# Extraindo os valores das cotações
cotacao_dolar = float(cotacao['USDBRL']['bid'])
cotacao_euro = float(cotacao['EURBRL']['bid'])

# Criando os gráficos
grafico_dolar = gera_grafico_mensal('Dólar', cotacao_dolar)
grafico_euro = gera_grafico_mensal('Euro', cotacao_euro)

# Exibindo cotações e gráficos
st.write(f"Dólar (USD/BRL): R${cotacao_dolar:.2f}")
st.plotly_chart(grafico_dolar, use_container_width=True)

st.write(f"Euro (EUR/BRL): R${cotacao_euro:.2f}")
st.plotly_chart(grafico_euro, use_container_width=True)


