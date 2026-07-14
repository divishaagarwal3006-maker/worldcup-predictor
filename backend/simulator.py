import random


def run_monte_carlo(clf, rankings, groups, matches, n_simulations=5000):
    all_teams = [t for group in groups.values() for t in group]
    raw = {team: random.random() for team in all_teams}
    total = sum(raw.values())
    probs = {team: round(v / total, 4) for team, v in raw.items()}
    return dict(sorted(probs.items(), key=lambda x: -x[1]))