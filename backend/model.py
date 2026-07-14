import random


def load_data():
    return [], None


def load_model():
    rankings = {
        "Brazil": 1, "Argentina": 2, "France": 3, "England": 4,
        "Spain": 5, "Germany": 6, "Portugal": 7, "Netherlands": 8,
    }
    return None, rankings


def predict_match(clf, rankings, team_a, team_b, matches=None):
    a_win = round(random.uniform(0.25, 0.55), 2)
    draw = round(random.uniform(0.15, 0.3), 2)
    b_win = round(1 - a_win - draw, 2)
    return {"team_a_win": a_win, "draw": draw, "team_b_win": b_win}