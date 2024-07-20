import random
import rps
import json

PLAYERS = {
    'aur': 'S!B|P?>!B',
    'ehud': '~!B|P@<!B',
    'hed': '~!B|P?!B',
    'amir': '~!~!B|S@P?-P@+>!B',
}

def tournament():
    random.seed(42)
    scores = {p: 0 for p in PLAYERS}
    for a in PLAYERS:
        for b in PLAYERS:
            if a != b:
                prog_a = {k: v for k, v in zip("ABCD", PLAYERS[a].split("|"))}
                prog_b = {k: v for k, v in zip("ABCD", PLAYERS[b].split("|"))}
                score, match_log, _full_log = rps.run_game(100, prog_a, prog_b, random.randint(0, 1<<64))
                scores[a] += score
                scores[b] -= score
                print(a, b)
                print(match_log, score)
    print(json.dumps(scores, indent=2))

if __name__ == "__main__":
    tournament()