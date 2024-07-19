import random


def rps_increment(move):
    return "PSR"["RPS".index(move)]


def rps_decrement(move):
    return "SRP"["RPS".index(move)]


def rps_add(move1, move2):
    return "RPS"[("RPS".index(move1) + "RPS".index(move2)) % 3]


def rps_subtract(move1, move2):
    return "RPS"[("RPS".index(move1) - "RPS".index(move2)) % 3]


def rps_special(move1, move2):
    return "S" if move1 == move2 == "R" else "P"


def execute_operation(op, stack, ip):
    if op in "RPS":
        stack.append(op)
    elif op == "~":
        stack.append(random.choice("RPS"))
    elif op == "!":
        return stack.pop()
    elif op == ">":
        stack.append(rps_increment(stack.pop()))
    elif op == "<":
        stack.append(rps_decrement(stack.pop()))
    elif op == "+":
        b, a = stack.pop(), stack.pop()
        stack.append(rps_add(a, b))
    elif op == "-":
        b, a = stack.pop(), stack.pop()
        stack.append(rps_subtract(a, b))
    elif op == "^":
        b, a = stack.pop(), stack.pop()
        stack.append(rps_special(a, b))
    elif op == "X":
        stack.pop()
    elif op == "8":
        stack.append(stack[-1])
    elif op == "%":
        stack[-1], stack[-2] = stack[-2], stack[-1]
    elif op == "[":
        stack.append(stack[-2])
    elif op == "@":
        depth = "RPS".index(stack.pop())
        stack.append("R")  # Placeholder, actual value set in run_program
    elif op == "?":
        depth = "RPS".index(stack.pop())
        stack.append("R")  # Placeholder, actual value set in run_program
    else:
        raise NotImplementedError(op)
    return None


def run_program(program, k, opponent_moves):
    stack = []
    moves = []
    log = []
    ip = 0

    def log_state():
        round_log.append(
            {
                "stack": list(stack),
                "ip": ip,
            }
        )

    for round in range(k):
        round_log = []
        j = 0
        while True:
            op = program[ip]
            if op in "ABC":
                log_state()
                ip = 0
                j += 1
                continue
            try:
                move = execute_operation(op, stack, ip)
            except Exception as e:
                log.append(
                    {
                        "states": round_log,
                        "error": str(e),
                        "my_history": list(reversed(moves)),
                        "opponent_history": opponent_moves[:round],
                    }
                )
                return moves, log

            log_state()
            if op == "@" and stack:
                depth = "RPS".index(stack[-1])
                stack[-1] = moves[depth] if depth < len(moves) else "R"
            elif op == "?" and stack:
                depth = "RPS".index(stack[-1])
                stack[-1] = (
                    opponent_moves[depth] if depth < len(opponent_moves) else "R"
                )
            if move:
                moves.append(move)
                log_state()
                log.append(
                    {
                        "states": round_log,
                        "move": move,
                        "my_history": list(reversed(moves)),
                        "opponent_history": opponent_moves[:round],
                    }
                )
                ip += 1
                break
            ip += 1
            j += 1
            assert j < 100
    return moves, log


def run_game(k, prog1, prog2, seed):
    random.seed(seed)
    moves1, log1 = run_program(prog1["A"], k, [])
    moves2, log2 = run_program(prog2["A"], k, moves1)

    score = sum(
        (a == "R" and b == "S") or (a == "P" and b == "R") or (a == "S" and b == "P")
        for a, b in zip(moves1, moves2)
    ) - sum(
        (b == "R" and a == "S") or (b == "P" and a == "R") or (b == "S" and a == "P")
        for a, b in zip(moves1, moves2)
    )

    match_log = "".join(
        f"{m1}{m2}{'=' if m1 == m2 else ('>' if (m1+m2) in ['RP', 'PS', 'SR'] else '<')}"
        for m1, m2 in zip(moves1, moves2)
    )

    full_log = {"<": log1, ">": log2}

    return score, match_log, full_log


# Example usage:
if __name__ == "__main__":
    prog1 = {"A": "R>!P>!S>!A"}
    prog2 = {"A": "S!R!P!"}
    score, match_log, full_log = run_game(3, prog1, prog2, 42)
    print(f"Score: {score}")
    print(f"Match log: {match_log}")
    print("Full log:")
    import json

    print(json.dumps(full_log, indent=2))
