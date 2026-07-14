# 🏆 World Cup Winner Predictor

Predicts FIFA World Cup match outcomes and simulates full tournament brackets
using a machine learning model, then generates natural-language scouting
reports using the Gemini API.

## Live Demo

- Backend API: https://worldcup-predictor-16sf.onrender.com
- Frontend: https://divishaagarwal3006-maker.github.io/worldcup-predictor/
## How it works

1. **Data** — historical international match results + team rankings (`data/`).
   Ships with sample data so the project runs out of the box.
2. **Model** (`backend/model.py`) — predicts win/draw/loss probabilities for
   any two teams based on ranking difference, recent form, and head-to-head
   history.
3. **Simulator** (`backend/simulator.py`) — runs a Monte Carlo simulation of
   the full tournament thousands of times to estimate each team's title
   probability.
4. **LLM commentary** (`backend/llm.py`) — feeds the model's numbers to the
   Gemini API to generate a short scouting report per team.
5. **API + frontend** (`backend/app.py`, `frontend/index.html`) — a FastAPI
   backend serves predictions to a single-page HTML dashboard.

## Project structure
worldcup-predictor/
├── data/                  # historical match + ranking data
├── backend/
│   ├── model.py           # feature engineering + ML model
│   ├── train_model.py     # training script, saves model to disk
│   ├── simulator.py       # Monte Carlo tournament simulator
│   ├── llm.py             # Gemini API integration for commentary
│   └── app.py             # FastAPI app tying it all together
├── frontend/
│   └── index.html         # simple dashboard UI
└── requirements.txt

## Setup (local)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python backend/train_model.py
$env:GEMINI_API_KEY="your-key" # optional, for AI commentary
uvicorn backend.app:app --reload
```

Then open `frontend/index.html` in your browser.

## Deployment

- Backend deployed on **Render** (free tier).
- Frontend deployed on **GitHub Pages**.

## Future improvements

- [ ] Replace synthetic sample data with real historical match data
      (e.g. Kaggle international football results dataset)
- [ ] Add player-level injury/squad data as extra model features
- [ ] Add a `/compare-teams` endpoint for head-to-head-only comparisons
- [ ] Add caching so repeated tournament simulations don't recompute from scratch
- [ ] Add unit tests for `model.py` feature functions
- [ ] Add a proper loading state / error handling in the frontend UI
- [ ] Support live fixture data via an API-Football integration
- [ ] Add authentication if this ever needs to support multiple users
- [ ] Dockerize the backend for easier deployment

## License

MIT
