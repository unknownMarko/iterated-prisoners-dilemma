from strategies import Action, C, D, ALL_STRATEGIES

ROUNDS = 200

# Payoff matrix: (player1_score, player2_score)
PAYOFF = {
    (C, C): (3, 3),
    (C, D): (0, 5),
    (D, C): (5, 0),
    (D, D): (1, 1),
}


def play_match(strategy1_cls, strategy2_cls, rounds=ROUNDS):
    """Play a match of `rounds` rounds between two strategy instances.
    Returns (score1, score2)."""
    s1 = strategy1_cls()
    s2 = strategy2_cls()

    score1, score2 = 0, 0

    for _ in range(rounds):
        action1 = s1.choose()
        action2 = s2.choose()

        p1, p2 = PAYOFF[(action1, action2)]
        score1 += p1
        score2 += p2

        s1.record_round(action1, action2)
        s2.record_round(action2, action1)

    return score1, score2


def run_tournament(strategies=None, rounds=ROUNDS):
    """Run a round-robin tournament. Each strategy plays against every other
    strategy (including itself). Returns results dict."""
    if strategies is None:
        strategies = ALL_STRATEGIES

    n = len(strategies)
    # total_scores[i] = cumulative score for strategy i across all matches
    total_scores = [0] * n
    # match_results[i][j] = (score_i, score_j) when i plays j
    match_results = [[None] * n for _ in range(n)]
    match_count = [0] * n

    for i in range(n):
        for j in range(n):
            s1, s2 = play_match(strategies[i], strategies[j], rounds)
            match_results[i][j] = (s1, s2)
            total_scores[i] += s1
            total_scores[j] += s2
            match_count[i] += 1
            match_count[j] += 1

    # Average score per round per match
    avg_scores = []
    for i in range(n):
        avg = total_scores[i] / match_count[i] / rounds
        avg_scores.append(avg)

    return strategies, total_scores, avg_scores, match_results


def print_results(strategies, total_scores, avg_scores, match_results):
    """Pretty-print the tournament results."""
    n = len(strategies)

    # Ranking
    ranking = sorted(range(n), key=lambda i: total_scores[i], reverse=True)

    print("=" * 70)
    print(f"{'AXELROD TOURNAMENT RESULTS':^70}")
    print(f"{'(' + str(ROUNDS) + ' rounds per match)':^70}")
    print("=" * 70)

    # Leaderboard
    print(f"\n{'Rank':<6} {'Strategy':<28} {'Total Score':<14} {'Avg/Round':<10}")
    print("-" * 60)
    for rank, i in enumerate(ranking, 1):
        name = strategies[i].name if hasattr(strategies[i], 'name') else strategies[i].__name__
        print(f"{rank:<6} {name:<28} {total_scores[i]:<14} {avg_scores[i]:<10.3f}")

    # Detailed match matrix
    print(f"\n{'=' * 70}")
    print(f"{'MATCH DETAIL (row score vs column opponent)':^70}")
    print("=" * 70)

    # Short labels
    labels = []
    for s in strategies:
        name = s.name if hasattr(s, 'name') else s.__name__
        labels.append(name[:12])

    header = f"{'':>14}" + "".join(f"{lbl:>14}" for lbl in labels)
    print(header)
    print("-" * (14 + 14 * n))

    for i in range(n):
        row = f"{labels[i]:>14}"
        for j in range(n):
            s1, _ = match_results[i][j]
            row += f"{s1:>14}"
        print(row)

    print()


def main():
    strategies, total_scores, avg_scores, match_results = run_tournament()
    print_results(strategies, total_scores, avg_scores, match_results)


if __name__ == "__main__":
    main()
