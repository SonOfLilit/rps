import random

def rps_increment(move):
    return 'PSR'['RPS'.index(move)]

def rps_decrement(move):
    return 'SRP'['RPS'.index(move)]

def rps_add(move1, move2):
    return 'RPS'[('RPS'.index(move1) + 'RPS'.index(move2)) % 3]

def rps_subtract(move1, move2):
    return 'RPS'[('RPS'.index(move1) - 'RPS'.index(move2)) % 3]

def rps_special(move1, move2):
    return 'S' if move1 == move2 == 'R' else 'P'

def execute_operation(op, stack, history, opponent_history):
    if op in 'RPS':
        stack.append(op)
    elif op == '~':
        stack.append(random.choice('RPS'))
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
        if stack and history:
            depth = 'RPS'.index(stack.pop())
            stack.append(history[depth] if depth < len(history) else 'R')
    elif op == '?':
        if stack and opponent_history:
            depth = 'RPS'.index(stack.pop())
            stack.append(opponent_history[depth] if depth < len(opponent_history) else 'R')
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
        if len(moves) < _ + 1:
            moves.append('R')  # Default move if program doesn't produce a move
            history.insert(0, 'R')
    return moves

def run_game(k, prog1, prog2, seed):
    random.seed(seed)
    moves1 = run_program(prog1['A'], k, [])
    moves2 = run_program(prog2['A'], k, moves1)
    
    score = sum((moves1[i] == 'R' and moves2[i] == 'S') or
                (moves1[i] == 'P' and moves2[i] == 'R') or
                (moves1[i] == 'S' and moves2[i] == 'P')
                for i in range(k))
    
    match_log = ''.join(f"{m1}{m2}{'=' if m1 == m2 else ('>' if (m1+m2) in ['RP', 'PS', 'SR'] else '<')}"
                        for m1, m2 in zip(moves1, moves2))
    
    return score, match_log, {}
