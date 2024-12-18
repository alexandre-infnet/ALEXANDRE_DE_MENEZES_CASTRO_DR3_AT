import os
import streamlit as st
import requests
import pandas as pd
from statsbombpy import sb
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI


def query_event(event_type=None, player=None, team=None):
    events = sb.events(match_id)

    filtered_events = events
    if event_type:
        filtered_events = filtered_events[filtered_events['type'] == event_type]
    if player:
        filtered_events = filtered_events[filtered_events['player'] == player]
    if team:
        filtered_events = filtered_events[filtered_events['team'] == team]
    return filtered_events


def compare_players(player1, player2):
    player1_stats = events[events['player'] == player1].groupby('type').size()
    player2_stats = events[events['player'] == player2].groupby('type').size()
    comparison = pd.concat([player1_stats, player2_stats], axis=1, keys=[player1, player2])
    comparison.fillna(0, inplace=True)

    return comparison


def get_players_statistics(match_id):
    events = sb.events(match_id)
    unique_players = events["player"].dropna().unique()
    statistics_data = []

    for player in unique_players:
        player_events = events[events["player"] == player]

        passes = int(player_events[player_events["type"] == "Pass"].shape[0])
        shots = int(player_events[player_events["type"] == "Shot"].shape[0])
        tackles = int(player_events[player_events["type"] == "Tackle"].shape[0])

        statistics_data.append({
            "Player": player,
            "Passes": passes,
            "Shots": shots,
            "Tackles": tackles
        })

    statistics_df = pd.DataFrame(statistics_data)
    st.dataframe(statistics_df)


API_BASE_URL = "http://127.0.0.1:8000"

st.title("Interface para Análise de Partidas")
match_id = st.number_input("ID da Partida", value=3788741)
player_name = st.text_input("Nome do Jogador", value="Bryan Cristante")

tools = [
    Tool(
        name="Query Events",
        func=lambda x: query_event(**eval(x)),
        description="Consulta eventos específicos da partida. Use parâmetros como event_type, player ou team."
    ),
    Tool(
        name="Compare Players",
        func=lambda x: compare_players(**eval(x)),
        description="Compara dois jogadores baseando-se em eventos da partida."
    ),
]

if st.button("Sumarizar"):
    if match_id:
        try:
            response = requests.post(f"{API_BASE_URL}/match_summary", json={"match_id": match_id})
            if response.status_code == 200:
                st.subheader("Resumo da Partida")
                st.write(response.json()["match_summary"])
            else:
                st.error(f"Erro: {response.status_code} - {response.json().get('detail', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")
    else:
        st.error("Por favor, insira um ID de partida válido.")

selected_metric = st.selectbox("Selecione o evento:", ["Passes", "Chutes", "Desarmes", "Minutos Jogados"])
if st.button("Obter Eventos e Perfil do Jogador"):
    if match_id and player_name:
        try:
            response = requests.post(
                f"{API_BASE_URL}/player_profile",
                json={"match_id": match_id, "player_name": player_name}
            )
            if response.status_code == 200:
                player_data = response.json()

                st.subheader("Estatísticas do Jogo")
                statistics = player_data["statistics"]

                if selected_metric == "Passes":
                    st.metric("Passes", statistics["passes"])
                if selected_metric == "Chutes":
                    st.metric("Chutes", statistics["shots"])
                if selected_metric == "Desarmes":
                    st.metric("Desarmes", statistics["tackles"])
                if selected_metric == "Minutos Jogados":
                    st.metric("Minutos Jogados", statistics["minutes_played"])

                st.text(f"Time: {player_data['team']}")
                st.text(f"ID do Jogador: {player_data['player_id']}")
                st.text(f"ID da Partida: {player_data['match_id']}")

                st.subheader("Posição e detalhes")
                for position in player_data["player_position"]:
                    st.text(f"Posição: {position['position']}")
                    st.text(f"Período de Início: {position['from']} (2º Tempo)")
                    if position["to"]:
                        st.text(f"Período de Término: {position['to']}")
                    else:
                        st.text("Período de Término: Final do jogo")
                    st.text(f"Motivo de Início: {position['start_reason']}")
                    st.text(f"Motivo de Término: {position['end_reason']}")
            else:
                st.error(f"Erro: {response.status_code} - {response.json().get('detail', 'Erro desconhecido')}")
            st.subheader("Estatísticas dos jogadores da partida")
            get_players_statistics(match_id)

        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")
    else:
        st.error("Por favor, insira o ID da partida e o nome do jogador.")

st.subheader("Consulta de eventos específicos da partida e Geração de comparações entre dois jogadores.")

events = sb.events(match_id)
player1 = st.selectbox("jogador 1", events["player"].dropna().unique())
player2 = st.selectbox("jogador 2", events["player"].dropna().unique())

if st.button("Comparar jogadores"):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

    query_event_result = agent.run('Query Events with parameters: {"event_type": "Shot", "team": "Italy"}')
    st.text(query_event_result)

    compare_players_result = agent.run(
        f'Compare Players with parameters: {{"player1": "{player1}", "player2": "{player2}"}}'
    )

    st.text(compare_players_result)