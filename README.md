# Axelrod's Tournament

Reproduction of [Robert Axelrod's 1981 tournament](https://en.wikipedia.org/wiki/Robert_Axelrod) in the [Iterated Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma), where strategies compete against each other (including themselves) over 200 rounds.

## How to Run

```
python3 tournament.py
```

Requires Python 3.10+ — no external dependencies.

## Payoff Matrix

|  | Defect (D) | Cooperate (C) |
|--|------------|---------------|
| **Defect (D)** | 1, 1 | 5, 0 |
| **Cooperate (C)** | 0, 5 | 3, 3 |

- Mutual cooperation: 3 points each (3 years of freedom)
- Mutual defection: 1 point each (1 year of freedom)
- Defect vs cooperate: 5 vs 0 points

## Strategies

| Strategy | Type | Description |
|----------|------|-------------|
| Tit For Tat | Classic | Cooperates first, then copies opponent's last move |
| Always Cooperate | Classic | Always cooperates |
| Always Defect | Classic | Always defects |
| Random | Classic | 50/50 random choice |
| Periodic DDC | Classic | Cycles: defect, defect, cooperate |
| Periodic CCD | Classic | Cycles: cooperate, cooperate, defect |
| Grudger | Classic | Cooperates until opponent defects once, then always defects |
| Suspicious Tit For Tat | Classic | Like TFT but defects on the first move |
| Pavlov | Classic | Win-Stay, Lose-Shift — repeats action if payoff was good, switches otherwise |
| Forgiving TFT | Custom | Like TFT but only retaliates after two consecutive defections |

## Tournament Rules

- Round-robin: every strategy plays against every other strategy (including itself)
- 200 rounds per match
- Strategies ranked by highest average score per round

## Results

| Rank | Strategy | Avg/Round |
|------|----------|-----------|
| 1 | Grudger | 2.591 |
| 2 | Tit For Tat | 2.550 |
| 3 | Forgiving TFT (custom) | 2.442 |
| 4 | Pavlov | 2.408 |
| 5 | Periodic DDC | 2.348 |
| 6 | Always Cooperate | 2.257 |
| 7 | Always Defect | 2.201 |
| 8 | Periodic CCD | 2.143 |
| 9 | Random | 2.131 |
| 10 | Suspicious Tit For Tat | 2.039 |

Note: Random strategy introduces variance — results may differ slightly between runs.

## Analysis

"Nice" strategies (those that never defect first) dominate the top of the ranking — Grudger, Tit For Tat, Forgiving TFT, and Pavlov all cooperate on the first move. This confirms Axelrod's original finding: being nice, retaliatory, and forgiving is the winning combination.

**Grudger** edges out Tit For Tat in this set because it punishes defectors permanently, which earns more against noisy or periodically defecting opponents. However, in larger tournaments with more cooperative strategies, TFT's forgiveness tends to win out.

**Always Defect** ranks below Always Cooperate — a counterintuitive result that shows how mutual cooperation (3 pts) consistently outperforms mutual defection (1 pt) when most strategies are willing to cooperate.
