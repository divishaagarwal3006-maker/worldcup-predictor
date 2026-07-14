from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

from backend.model import load_model, load_data, predict_match
from backend.simulator import run_monte_carlo
from backend.llm import generate_all_reports

app = FastAPI(title="World Cup Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_clf = None
_rankings = None
_matches = None


@app.on_event("startup")
def load_artifacts():
    global _clf, _rankings, _matches
    _clf, _rankings = load_model()
    _matches, _ = load_data()


class MatchRequest(BaseModel):
    team_a: str
    team_b: str


class TournamentRequest(BaseModel):
    groups: Dict[str, List[str]]
    n_simulations: int = 5000
    include_commentary: bool = False


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _clf is not None}


@app.get("/teams")
def list_teams():
    if _rankings is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    return {"teams": sorted(_rankings.keys())}


@app.post("/predict-match")
def predict_single_match(req: MatchRequest):
    if _clf is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    probs = predict_match(_clf, _rankings, req.team_a, req.team_b, matches=_matches)
    return {
        "team_a": req.team_a,
        "team_b": req.team_b,
        "team_a_win_probability": probs["team_a_win"],
        "draw_probability": probs["draw"],
        "team_b_win_probability": probs["team_b_win"],
    }


@app.post("/simulate-tournament")
def simulate_tournament(req: TournamentRequest):
    if _clf is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    all_teams = [t for group in req.groups.values() for t in group]
    unknown = [t for t in all_teams if t not in _rankings]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown teams: {unknown}")
    probs = run_monte_carlo(_clf, _rankings, req.groups, _matches, n_simulations=req.n_simulations)
    result = {"title_probabilities": probs}
    if req.include_commentary:
        result["scouting_reports"] = generate_all_reports(probs)
    return result