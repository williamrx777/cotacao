import streamlit as st
import requests
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Função para obter a cotação atual
def obtem_cotacao(moeda):
    url = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"
    resposta = requests.get(url)
    dados = resposta.json()
    return float(dados[f'{moeda}BRL']['bid'])

# Função para carregar dados históricos do arquivo
def carrega_dados_arquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    return []

# Função para salvar dados no arquivo
def salva_dados_arquivo(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Função para atualizar o histórico com a cotação atual
def atualiza_historico(moeda, caminho_arquivo):
    cotacao_atual = obtem_cotacao(moeda)
    horario_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Carrega os dados existentes
    dados_historico = carrega_dados_arquivo(caminho_arquivo)
    
    # Adiciona a nova entrada ao histórico
    dados_historico.append({'timestamp': horario_atual, 'valor': cotacao_atual})
    
    # Salva os dados atualizados no arquivo
    salva_dados_arquivo(caminho_arquivo, dados_historico)

    return dados_historico

# Função para gerar o gráfico
def gera_grafico_horario(moeda, dados_historico):
    datas = [datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S') for item in dados_historico]
    valores = [item['valor'] for item in dados_historico]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datas, y=valores, mode='lines+markers', name=moeda, line=dict(color='blue')))
    
    fig.update_layout(
        title=f'Evolução Horária do {moeda}',
        xaxis_title='Hora',
        yaxis_title='Valor em BRL',
        xaxis_rangeslider_visible=True,
        template='plotly_dark'
    )
    
    return fig

# Caminhos dos arquivos de histórico
arquivo_dolar = 'historico_dolar.json'
arquivo_euro = 'historico_euro.json'

# Atualizando o histórico e gerando gráficos
historico_dolar = atualiza_historico('USD', arquivo_dolar)
historico_euro = atualiza_historico('EUR', arquivo_euro)

grafico_dolar = gera_grafico_horario('Dólar', historico_dolar)
grafico_euro = gera_grafico_horario('Euro', historico_euro)

# Configurando o layout do Streamlit
st.set_page_config(page_title="Cotações de Moedas", layout="wide")

# Título da página
st.title("Cotações de Moedas - Histórico Horário")

# Exibindo gráficos
st.write(f"Dólar (USD/BRL): R${historico_dolar[-1]['valor']:.2f}")
st.plotly_chart(grafico_dolar, use_container_width=True)

st.write(f"Euro (EUR/BRL): R${historico_euro[-1]['valor']:.2f}")
st.plotly_chart(grafico_euro, use_container_width=True)
