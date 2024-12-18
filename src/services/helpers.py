from typing import List
from statsbombpy import sb
import google.generativeai as genai
from models import PlayerProfileResponse, PlayerStatistics


genai.configure(api_key="AIzaSyCOts1mwmF2GIF_FUiUYuujoDJe4DoTBsU")
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize_match_events(match_id: int) -> str:
    events = sb.events(match_id)
    if events.empty:
        return {"error": f"Nenhum evento encontrado para a partida ID {match_id}."}

    goals = events[events["type"] == "Goal"]
    assists = events[events["pass_assisted_shot_id"].notnull()]
    cards = events[events["type"].isin(["Yellow Card", "Red Card"])]

    highlights = []

    for _, goal in goals.iterrows():
        highlights.append(
            f"Gol de {goal['player']} pelo {goal['team']} aos {goal['minute']} minutos."
        )

    for _, assist in assists.iterrows():
        highlights.append(
            f"Assistência de {assist['player']} para {assist['pass_recipient']} pelo {assist['team']}."
        )

    for _, card in cards.iterrows():
        highlights.append(
            f"{card['type']} para {card['player']} do {card['team']} aos {card['minute']} minutos."
        )

    description = " ".join(highlights)
    prompt = f"Crie um resumo amigável de uma partida de futebol com os seguintes destaques: {description}."

    response = model.generate_content(prompt)
    return response.text


def collect_match_events(match_id: int) -> List[str]:
    try:
        events = sb.events(match_id)
        if events.empty:
            return {"error": f"Nenhum evento encontrado para a partida ID {match_id}."}

        highlights = []

        goals = events[events["type"] == "Goal"]
        assists = events[events["pass_assisted_shot_id"].notnull()]
        cards = events[events["type"].isin(["Yellow Card", "Red Card"])]

        for _, goal in goals.iterrows():
            highlights.append(
                f"Gol de {goal['player']} pelo {goal['team']} aos {goal['minute']} minutos."
            )

        for _, assist in assists.iterrows():
            highlights.append(
                f"Assistência de {assist['player']} para {assist['pass_recipient']} pelo {assist['team']}."
            )

        for _, card in cards.iterrows():
            highlights.append(
                f"{card['type']} para {card['player']} do {card['team']} aos {card['minute']} minutos."
            )

        return highlights

    except Exception as e:
        return {"error": f"Erro ao coletar eventos da partida: {e}"}


def generate_narrative(highlights: List[str], style: str) -> str:
    try:
        prompt_styles = {
            "formal": "Crie uma narração formal, técnica e objetiva dos seguintes eventos de uma partida de futebol:",
            "humoristico": "Crie uma narração descontraída, criativa e engraçada dos seguintes eventos de uma partida de futebol:",
            "tecnico": "Crie uma análise detalhada e técnica dos seguintes eventos de uma partida de futebol:",
        }

        prompt = f"{prompt_styles[style]} {' '.join(highlights)}"
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return {"error": f"Erro ao gerar a narrativa: {e}"}


def get_player_profile(match_id: int, player_name: str) -> PlayerProfileResponse:
    events = sb.events(match_id)
    lineups = sb.lineups(match_id=match_id)

    player_profile = None
    team_name = None

    for team, lineup in lineups.items():
        player_data = lineup[lineup['player_name'] == player_name]
        if not player_data.empty:
            player_profile = player_data.iloc[0]
            team_name = team
            break

    if player_profile is not None:
        team = team_name
        player_profile = player_profile
        player_id = int(player_profile['player_id'])
        player_position = player_profile['positions']


    player_events = events[events["player"] == player_name]

    if player_events.empty:
        return {
            "error": f"Jogador '{player_name}' não encontrado na partida ID {match_id}."
        }

    passes = int(player_events[player_events["type"] == "Pass"].shape[0])
    shots = int(player_events[player_events["type"] == "Shot"].shape[0])
    tackles = int(player_events[player_events["type"] == "Tackle"].shape[0])
    minutes_played = int(
        player_events["minute"].max() - player_events["minute"].min() + 1
    )

    return PlayerProfileResponse(
        name=player_name,
        match_id=match_id,
        statistics=PlayerStatistics(
            passes=passes, shots=shots, tackles=tackles, minutes_played=minutes_played
        ),
        team=team,
        player_id=player_id,
        player_position=player_position
    )
