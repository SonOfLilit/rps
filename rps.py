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
        if stack:
            return stack.pop()
    elif op == ">":
        if stack:
            stack.append(rps_increment(stack.pop()))
    elif op == "<":
        if stack:
            stack.append(rps_decrement(stack.pop()))
    elif op == "+":
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_add(a, b))
    elif op == "-":
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_subtract(a, b))
    elif op == "^":
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_special(a, b))
    elif op == "X":
        if stack:
            stack.pop()
    elif op == "8":
        if stack:
            stack.append(stack[-1])
    elif op == "%":
        if len(stack) >= 2:
            stack[-1], stack[-2] = stack[-2], stack[-1]
    elif op == "c":
        if len(stack) >= 2:
            stack.append(stack[-2])
    elif op == "@":
        if stack:
            depth = "RPS".index(stack.pop())
            stack.append("R")  # Placeholder, actual value set in run_program
    elif op == "?":
        if stack:
            depth = "RPS".index(stack.pop())
            stack.append("R")  # Placeholder, actual value set in run_program
    return None


def run_program(program, k, opponent_moves):
    stack = []
    moves = []
    log = []
    ip = 0
    program_length = len(program)

    for round in range(k):
        round_log = []
        while ip < program_length:
            op = program[ip]
            pre_state = {"stack": list(stack), "ip": ip}
            if op in "ABC":
                ip = 0
                round_log.append(pre_state)
                break
            move = execute_operation(op, stack, ip)
            post_state = {"stack": list(stack), "ip": ip}
            round_log.append(pre_state)
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
                log.append(
                    {
                        "states": round_log + [post_state],
                        "move": move,
                        "my_history": list(reversed(moves)),
                        "opponent_history": opponent_moves[:round],
                    }
                )
                ip += 1
                break
            ip += 1
        if len(moves) < round + 1:
            moves.append("R")
            log.append(
                {
                    "states": round_log + [{"stack": ["R"], "ip": ip}],
                    "move": "R",
                    "my_history": list(reversed(moves)),
                    "opponent_history": opponent_moves[:round],
                }
            )
    return moves, log


def run_game(k, prog1, prog2, seed):
    random.seed(seed)
    moves1, log1 = run_program(prog1["A"], k, [])
    moves2, log2 = run_program(prog2["A"], k, moves1)

    score = sum(
        (moves1[i] == "R" and moves2[i] == "S")
        or (moves1[i] == "P" and moves2[i] == "R")
        or (moves1[i] == "S" and moves2[i] == "P")
        for i in range(k)
    ) - sum(
        (moves2[i] == "R" and moves1[i] == "S")
        or (moves2[i] == "P" and moves1[i] == "R")
        or (moves2[i] == "S" and moves1[i] == "P")
        for i in range(k)
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
