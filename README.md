Como rodar:
Instale as dependencias do requirements.txt

Rode a API:
Entre no diretório src/services
Rode o comando: uvicorn routes:app --reload

Rode o Streamlit:
Rode o comando: streamlit run src/app.py

Este projeto é uma aplicação Streamlit para análise de partidas de futebol. Ele utiliza a biblioteca statsbombpy para acessar dados detalhados de eventos de partidas, e LangChain para a integração com modelos de linguagem para consultas e comparações avançadas. A interface permite:
	•	Resumir partidas específicas.
	•	Obter estatísticas detalhadas de jogadores.
	•	Comparar eventos de diferentes jogadores.
	•	Consultar eventos específicos de uma partida.

Recursos Principais

1. Resumo de Partidas

A aplicação se conecta a uma API local para gerar um resumo textual da partida com base no match_id.

2. Estatísticas de Jogadores

Exibe estatísticas como passes, chutes, desarmes e minutos jogados para um jogador selecionado.

3. Comparação de Jogadores

Permite comparar dois jogadores de uma partida com base nos eventos realizados, como passes, chutes e desarmes.

4. Consulta de Eventos

Oferece ferramentas para buscar eventos específicos da partida por tipo, jogador ou time.

Requisitos

Dependências
	•	Python 3.8+
	•	Bibliotecas:
	•	streamlit
	•	requests
	•	pandas
	•	statsbombpy
	•	matplotlib
	•	langchain
	•	openai

Variáveis de Ambiente
	•	OPENAI_API_KEY: Chave de API da OpenAI para utilização dos modelos de linguagem.

rquitetura
	1.	Backend (API Local):
	    •	A aplicação utiliza uma API local para processar e retornar resumos e dados detalhados.
	2.	Frontend (Streamlit):
	    •	Interface de usuário para entrada de dados e visualização de estatísticas.
	3.	Integração de Modelos de Linguagem:
	    •	Uso do LangChain e OpenAI para análises avançadas de dados.
