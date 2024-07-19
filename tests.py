test_suite = [
    # Basic moves and scoring
    (3, {'A': 'R!A'}, {'A': 'P!A'}),  # Test R vs P
    (3, {'A': 'P!A'}, {'A': 'S!A'}),  # Test P vs S
    (3, {'A': 'S!A'}, {'A': 'R!A'}),  # Test S vs R

    # Random value
    (5, {'A': '~!A'}, {'A': 'R!A'}),  # Test random vs constant

    # Increment and decrement
    (3, {'A': 'R>!A'}, {'A': 'P!A'}),  # R -> P
    (3, {'A': 'P<!A'}, {'A': 'R!A'}),  # P -> R
    (3, {'A': 'S>!A'}, {'A': 'R!A'}),  # S -> R
    (3, {'A': 'R<!A'}, {'A': 'S!A'}),  # R -> S

    # Addition and subtraction
    (3, {'A': 'RP-!A'}, {'A': 'S!A'}),  # R - P = S
    (3, {'A': 'SP+!A'}, {'A': 'R!A'}),  # S + P = R

    # Special ^ operation
    (3, {'A': 'RR^!A'}, {'A': 'P!A'}),  # RR^ -> S
    (3, {'A': 'RP^!A'}, {'A': 'S!A'}),  # RP^ -> P

    # Duplicate and swap
    (3, {'A': 'R8!X!A'}, {'A': 'PP!A'}),  # Duplicate R, play twice
    (3, {'A': 'RP%!X!A'}, {'A': 'RS!A'}),  # Swap R and P, play both

    # Copy
    (3, {'A': 'RPc!X!X!A'}, {'A': 'RPS!A'}),  # Copy R, play RRP

    # Subroutines
    (3, {'A': 'R!B', 'B': 'P!C', 'C': 'S!A'}, {'A': 'R!A'}),  # Test A->B->C->A

    # Access own history (corrected)
    (4, {'A': 'R!P!S!P@!A'}, {'A': 'R!A'}),  # Play R, P, S, then access previous move (P)
    (5, {'A': 'R!P!S!R!S@!A'}, {'A': 'R!A'}),  # Play R, P, S, R, then access 2 moves ago (P)
    (6, {'A': 'R!P!S!R!P!R@!A'}, {'A': 'R!A'}),  # Play R, P, S, R, P, then access 3 moves ago (S)

    # Access opponent's history (corrected)
    (4, {'A': 'R!P!S!P?!A'}, {'A': 'S!P!R!S!'}),  # Play R, P, S, then opponent's previous move
    (5, {'A': 'R!P!S!R!S?!A'}, {'A': 'P!S!R!P!R!'}),  # Play R, P, S, R, then opponent's move 2 ago
    (6, {'A': 'R!P!S!R!P!R?!A'}, {'A': 'S!P!R!S!P!S!'}),  # Play R, P, S, R, P, then opponent's move 3 ago

    # Complex strategy
    (5, {'A': 'R!P?>>!A'}, {'A': '~!A'}),  # Play counter to opponent's previous move + 2

    # Error case: stack underflow
    (1, {'A': '-!A'}, {'A': 'R!A'}),  # Try to subtract with empty stack

    # Error case: unknown command
    (1, {'A': 'Q!A'}, {'A': 'R!A'}),  # Use an undefined command 'Q'

    # Test all operations maintain R/P/S invariant
    (1, {'A': 'R>>!A'}, {'A': 'R!'}),  # R >> = S
    (1, {'A': 'S<<!A'}, {'A': 'R!'}),  # S << = R
    (1, {'A': 'RP+!A'}, {'A': 'R!'}),  # R + P = S
    (1, {'A': 'SP-!A'}, {'A': 'R!'}),  # S - P = R
    (1, {'A': 'RR^!A'}, {'A': 'R!'}),  # RR^ = S
    (1, {'A': 'RS^!A'}, {'A': 'R!'}),  # RS^ = P

    # Edge cases for @ and ?
    (3, {'A': 'R!P!P@!A'}, {'A': 'R!A'}),  # Access most recent move
    (3, {'A': 'R!P!S@!A'}, {'A': 'R!A'}),  # Access 2nd most recent move (should be R)
    (3, {'A': 'R!P!R@!A'}, {'A': 'R!A'}),  # Access 3rd most recent move (should be R, as there isn't one)
    (3, {'A': 'R!P!P?!A'}, {'A': 'P!S!R!'}),  # Access opponent's most recent move
    (3, {'A': 'R!P!S?!A'}, {'A': 'P!S!R!'}),  # Access opponent's 2nd most recent move
    (3, {'A': 'R!P!R?!A'}, {'A': 'P!S!R!'}),  # Access opponent's 3rd most recent move (should be R, as there isn't one)
]
