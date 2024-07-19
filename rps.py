import random

def set_random_seed(seed):
    random.seed(seed)

def rps_add(a, b):
    return 'RPS'[(('RPS'.index(a) + 'RPS'.index(b)) % 3)]

def rps_subtract(a, b):
    return 'RPS'[(('RPS'.index(a) - 'RPS'.index(b)) % 3)]

def rps_increment(a):
    return 'RPS'[(('RPS'.index(a) + 1) % 3)]

def rps_decrement(a):
    return 'RPS'[(('RPS'.index(a) - 1) % 3)]

def rps_special(a, b):
    return 'S' if a == b == 'R' else 'P'

def rps_random():
    return random.choice('RPS')

def get_history_move(history, depth):
    return history[depth] if depth < len(history) else 'R'

def execute_operation(op, stack, history, opponent_history):
    if op in 'RPS':
        stack.append(op)
    elif op == '~':
        stack.append(rps_random())
    elif op == '!':
        if stack:
            return stack.pop()
    elif op == '>':
        if stack:
            stack.append(rps_increment(stack.pop()))
    elif op == '<':
        if stack:
            stack.append(rps_decrement(stack.pop()))
    elif op == '+':
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_add(a, b))
    elif op == '-':
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_subtract(a, b))
    elif op == '^':
        if len(stack) >= 2:
            b, a = stack.pop(), stack.pop()
            stack.append(rps_special(a, b))
    elif op == 'X':
        if stack:
            stack.pop()
    elif op == '8':
        if stack:
            stack.append(stack[-1])
    elif op == '%':
        if len(stack) >= 2:
            stack[-1], stack[-2] = stack[-2], stack[-1]
    elif op == 'c':
        if len(stack) >= 2:
            stack.append(stack[-2])
    elif op == '@':
        if stack:
            depth = 'RPS'.index(stack.pop())
            stack.append(get_history_move(history, depth))
    elif op == '?':
        if stack:
            depth = 'RPS'.index(stack.pop())
            stack.append(get_history_move(opponent_history, depth))
    return None

def run_program(program, k, opponent_moves):
    stack = []
    history = []
    moves = []
    for _ in range(k):
        for op in program:
            if op in 'ABC':
                program = program[program.index(op):]
                break
            move = execute_operation(op, stack, history, opponent_moves[:len(moves)])
            if move:
                moves.append(move)
                history.insert(0, move)
                break
        if len(moves) < len(opponent_moves) + 1:
            moves.append('R')  # Default move if program doesn't produce a move
            history.insert(0, 'R')
    return moves

def calculate_score(moves1, moves2):
    return sum((moves1[i] == 'R' and moves2[i] == 'S') or
               (moves1[i] == 'P' and moves2[i] == 'R') or
               (moves1[i] == 'S' and moves2[i] == 'P')
               for i in range(len(moves1)))

def generate_match_log(moves1, moves2):
    return ''.join(f"{m1}{m2}{'=' if m1 == m2 else ('>' if (m1+m2) in ['RP', 'PS', 'SR'] else '<')}"
                   for m1, m2 in zip(moves1, moves2))

def run_game(k, prog1, prog2, seed=None):
    set_random_seed(seed)
    moves1 = run_program(prog1['A'], k, [])
    moves2 = run_program(prog2['A'], k, moves1)
    
    score = calculate_score(moves1, moves2)
    match_log = generate_match_log(moves1, moves2)
    
    return score, match_log, {}  # Empty dict for program_logs as they're not implemented in this outline
