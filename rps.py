import random


# Utility functions for RPS conversions
def rps_to_int(move):
    """Convert RPS move to integer representation."""
    return {"R": 2, "P": 0, "S": 1}[move]


def int_to_rps(num):
    """Convert integer representation to RPS move."""
    return {2: "R", 0: "P", 1: "S"}[num % 3]


def rps_increment(move):
    """Increment RPS move."""
    return int_to_rps((rps_to_int(move) + 1) % 3)


def rps_decrement(move):
    """Decrement RPS move."""
    return int_to_rps((rps_to_int(move) - 1) % 3)


def rps_add(move1, move2):
    """Add two RPS moves."""
    return int_to_rps((rps_to_int(move1) + rps_to_int(move2)) % 3)


def rps_subtract(move1, move2):
    """Subtract two RPS moves."""
    return int_to_rps((rps_to_int(move1) - rps_to_int(move2)) % 3)


def rps_special(move1, move2):
    """Special operation: S if both R, else P."""
    return "S" if move1 == move2 == "R" else "P"


def rps_compare(move1, move2):
    """Compare two RPS moves. Returns '>' if move1 wins, '<' if move2 wins, '=' if tie."""
    if move1 == move2:
        return "="
    return ">" if rps_to_int(move1) == (rps_to_int(move2) - 1) % 3 else "<"


def execute_operation(op, stack, own_history, opponent_history):
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
        a, b = stack.pop(), stack.pop()
        stack.append(rps_add(a, b))
    elif op == "-":
        a, b = stack.pop(), stack.pop()
        stack.append(rps_subtract(a, b))
    elif op == "^":
        a, b = stack.pop(), stack.pop()
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
        depth = rps_to_int(stack.pop())
        if depth >= len(own_history):
            raise ValueError(f"Not enough history to access depth {depth}")
        stack.append(own_history[-depth - 1])
    elif op == "?":
        depth = rps_to_int(stack.pop())
        if depth >= len(opponent_history):
            raise ValueError(f"Not enough opponent history to access depth {depth}")
        stack.append(opponent_history[-depth - 1])
    else:
        raise ValueError(f"Unknown operation: {op}")
    return None


def run_program_step(program, stack, subroutine, ip, own_history, opponent_history):
    states = []

    while True:
        if ip >= len(program[subroutine]):
            raise ValueError(
                f"Program counter out of bounds in subroutine {subroutine}"
            )

        op = program[subroutine][ip]

        if op in "ABC":
            states.append({"stack": list(stack), "ip": f"{subroutine}{ip}", "op": op})
            subroutine = op
            ip = 0
            continue

        try:
            move = execute_operation(op, stack, own_history, opponent_history)
        except Exception as e:
            return (
                {
                    "states": states,
                    "error": str(e),
                    "move": None,
                    "my_history": "".join(own_history),
                    "opponent_history": "".join(opponent_history),
                },
                subroutine,
                ip,
            )

        states.append({"stack": list(stack), "ip": f"{subroutine}{ip}", "op": op})

        if move:
            return (
                {
                    "states": states,
                    "move": move,
                    "my_history": "".join(own_history),
                    "opponent_history": "".join(opponent_history),
                },
                subroutine,
                ip + 1,
            )

        ip += 1


def run_game(k, prog1, prog2, seed):
    random.seed(seed)
    moves1, moves2 = [], []
    log1, log2 = [], []
    stack1, stack2 = [], []
    subroutine1, subroutine2 = "A", "A"
    ip1, ip2 = 0, 0

    for _ in range(k):
        round_log1, subroutine1, ip1 = run_program_step(
            prog1, stack1, subroutine1, ip1, moves1, moves2
        )
        round_log2, subroutine2, ip2 = run_program_step(
            prog2, stack2, subroutine2, ip2, moves2, moves1
        )

        log1.append(round_log1)
        log2.append(round_log2)

        if round_log1["move"] is None or round_log2["move"] is None:
            break

        moves1.append(round_log1["move"])
        moves2.append(round_log2["move"])

    score = sum(rps_compare(a, b) == "<" for a, b in zip(moves1, moves2)) - sum(
        rps_compare(a, b) == ">" for a, b in zip(moves1, moves2)
    )

    match_log = "".join(m1 + m2 + rps_compare(m1, m2) for m1, m2 in zip(moves1, moves2))

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
