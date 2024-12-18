from fastapi import FastAPI
from models import MatchNarrativeRequest, MatchSummaryRequest, PlayerProfileRequest
from helpers import collect_match_events, generate_narrative, get_player_profile, summarize_match_events


app = FastAPI(
    title="API de Narração Personalizada",
    description="Cria narrativas personalizadas de partidas de futebol.",
)


@app.post("/match_narrative", summary="Gera uma narração personalizada da partida.")
def match_narrative(request: MatchNarrativeRequest):
    events = collect_match_events(request.match_id)

    if "error" in events:
        return events

    narrative = generate_narrative(events, request.style)
    return {"narrative": narrative}


@app.post("/player_profile", summary="Retorna o perfil de um jogador.")
def player_profile(request: PlayerProfileRequest):
    result = get_player_profile(request.match_id, request.player_name)
    return result


@app.post("/match_summary", summary="Sumariza os eventos de uma partida.")
def match_summary(request: MatchSummaryRequest):
    result = summarize_match_events(request.match_id)
    return {"match_summary": result}
