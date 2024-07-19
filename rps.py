import random

def execute_operation(op, stack, history, opponent_history):
    if op in 'RPS':
        stack.append(op)
    elif op == '~':
        stack.append(random.choice('RPS'))
    elif op == '!':
        if stack:
            return stack.pop()
    elif op in '<>':
        if stack:
            x = stack.pop()
            stack.append('RPS'[('RPS'.index(x) + (1 if op == '>' else -1)) % 3])
    elif op in '+-':
        if len(stack) >= 2:
            y, x = stack.pop(), stack.pop()
            stack.append('RPS'[('RPS'.index(x) + ('RPS'.index(y) * (1 if op == '+' else -1))) % 3])
    elif op == '^':
        if len(stack) >= 2:
            y, x = stack.pop(), stack.pop()
            stack.append('S' if x == y == 'R' else 'P')
    elif op == 'X':
        if stack:
            stack.pop()
    elif op == '8':
        if stack:
            x = stack[-1]
            stack.append(x)
    elif op == '%':
        if len(stack) >= 2:
            stack[-1], stack[-2] = stack[-2], stack[-1]
    elif op == 'c':
        if len(stack) >= 2:
            stack.append(stack[-2])
    elif op == '@':
        if stack:
            depth = 'RPS'.index(stack.pop())
            stack.append(history[depth] if depth < len(history) else 'R')
    elif op == '?':
        if stack:
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
        if len(moves) < len(opponent_moves) + 1:
            moves.append('R')  # Default move if program doesn't produce a move
            history.insert(0, 'R')
    return moves

def run_game(k, prog1, prog2):
    moves1 = run_program(prog1['A'], k, [])
    moves2 = run_program(prog2['A'], k, moves1)
    
    score = sum((moves1[i] == 'R' and moves2[i] == 'S') or
                (moves1[i] == 'P' and moves2[i] == 'R') or
                (moves1[i] == 'S' and moves2[i] == 'P')
                for i in range(k))
    
    match_log = ''.join(f"{m1}{m2}{'=' if m1 == m2 else ('>' if (m1+m2) in ['RP', 'PS', 'SR'] else '<')}"
                        for m1, m2 in zip(moves1, moves2))
    
    return score, match_log, {}  # Empty dict for program_logs as they're not implemented in this outline
