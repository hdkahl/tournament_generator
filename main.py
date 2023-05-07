# This is the main file
import itertools
import json
import math

# File paths for data persistence
ROUNDS_FILE = "rounds.json"
ELO_RATINGS_FILE = "elo_ratings.json"

def save_rounds(rounds):
    with open(ROUNDS_FILE, "w") as file:
        json.dump(rounds, file)

def load_rounds():
    try:
        with open(ROUNDS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_elo_ratings(elo_ratings):
    with open(ELO_RATINGS_FILE, "w") as file:
        json.dump(elo_ratings, file)

def load_elo_ratings():
    try:
        with open(ELO_RATINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def generate_round_robin(teams):
    num_teams = len(teams)
    matches_per_round = num_teams // 2

    # Create a list of all possible match pairs
    match_pairs = list(itertools.combinations(teams, 2))

    # Generate rounds
    rounds = []
    for round_num in range(num_teams - 1):
        round_matches = []

        # Select matches for the current round
        for _ in range(matches_per_round):
            match = match_pairs.pop(0)
            round_matches.append(match)

        # Rotate the teams in the match pairs list
        match_pairs.append(match_pairs.pop(0))

        rounds.append(round_matches)

    save_rounds(rounds)
    return rounds

def update_elo_rating(winner_elo, loser_elo, score_difference):
    k_factor = score_difference
    expected_win = 1 / (1 + math.pow(10, (loser_elo - winner_elo) / 400))
    expected_loss = 1 - expected_win

    winner_new_elo = winner_elo + k_factor * (1 - expected_win)
    loser_new_elo = loser_elo + k_factor * (0 - expected_loss)

    return winner_new_elo, loser_new_elo

def track_tournament(rounds, team_elo_ratings):
    for round_num, matches in enumerate(rounds, start=1):
        print(f"Round {round_num}:")
        for match in matches:
            team1, team2 = match
            score1 = int(input(f"Score for {team1}: "))
            score2 = int(input(f"Score for {team2}: "))

            if score1 > score2:
                winner_elo, loser_elo = team_elo_ratings[team1], team_elo_ratings[team2]
                score_difference = score1 - score2
            elif score2 > score1:
                winner_elo, loser_elo = team_elo_ratings[team2], team_elo_ratings[team1]
                score_difference = score2 - score1
            else:
                print("It's a tie. Skipping match.")
                continue

            winner_elo, loser_elo = update_elo_rating(winner_elo, loser_elo, score_difference)

            team_elo_ratings[team1] = winner_elo
            team_elo_ratings[team2] = loser_elo

        print()

    save_elo_ratings(team_elo_ratings)

    print("Tournament Results:")
    for team, elo_rating in team_elo_ratings.items():
        print(f"{team}: Elo Rating = {elo_rating}")

# Example usage
teams = ["Team A", "Team B", ""]

elo_ratings = load_elo_ratings()
rounds = load_rounds()

if not rounds:
    rounds = generate_round_robin(teams)

track_tournament(rounds, elo_ratings)

