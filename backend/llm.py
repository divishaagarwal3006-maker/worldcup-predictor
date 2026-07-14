import os

SYSTEM_PROMPT = (
    "You are a football (soccer) analyst writing short, punchy scouting "
    "report summaries for a World Cup predictor app. Given a team and its "
    "modeled probability of winning the tournament, write 2-3 sentences "
    "of color commentary explaining why the model likes or doesn't like "
    "their chances. Be specific and confident, but don't invent statistics "
    "beyond what's given. No headers, no bullet points, just prose."
)


def _fallback_summary(team, probability, rank):
    if probability > 0.15:
        tone = f"{team} are a serious title threat"
    elif probability > 0.05:
        tone = f"{team} have a real path to the final"
    elif probability > 0.01:
        tone = f"{team} are a longshot but not out of it"
    else:
        tone = f"{team} would need a lot to go right"
    return f"{tone}, ranked #{rank} in the simulation with a {probability:.1%} title probability."


def generate_scouting_report(team, probability, rank):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return _fallback_summary(team, probability, rank)

    try:
        import google.generativeai as genai
    except ImportError:
        return _fallback_summary(team, probability, rank)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)

    user_prompt = (
        f"Team: {team}\n"
        f"Modeled probability of winning the tournament: {probability:.1%}\n"
        f"Rank among all teams in this simulation: #{rank}\n\n"
        "Write the scouting report."
    )

    try:
        response = model.generate_content(user_prompt)
        return response.text.strip()
    except Exception as e:
        return _fallback_summary(team, probability, rank) + f" (LLM commentary unavailable: {e})"


def generate_all_reports(title_probabilities, top_n=8):
    reports = {}
    for rank, (team, prob) in enumerate(list(title_probabilities.items())[:top_n], start=1):
        reports[team] = generate_scouting_report(team, prob, rank)
    return reports