test_suite = [
    # Basic moves, scoring, and random
    (3, {'A': 'R!A'}, {'A': 'P!A'}),  # R vs P
    (3, {'A': 'P!A'}, {'A': 'S!A'}),  # P vs S
    (3, {'A': '~!A'}, {'A': 'R!A'}),  # Random vs constant

    # Increment, decrement, and cycling
    (3, {'A': 'R>!P>!S>!A'}, {'A': 'S!R!P!'}),  # R->P->S->R

    # Addition, subtraction, and special operations
    (4, {'A': 'RP-!SP+!RR^!RP^!A'}, {'A': 'R!R!R!R!'}),  # S, R, S, P vs R, R, R, R

    # Stack operations (duplicate, swap, copy)
    (5, {'A': 'R8!X!RP%!X!RPc!X!X!A'}, {'A': 'S!S!S!S!S!'}),  # RR, PR, RRP vs SSSSS

    # Subroutines
    (3, {'A': 'R!B', 'B': 'P!C', 'C': 'S!A'}, {'A': 'R!A'}),  # A->B->C->A

    # Access own and opponent's history
    (8, {'A': 'R!P!S!R!P!P@!S@!R@!A'}, {'A': 'R!P!S!R!P!S!R!P!'}),  # RPSRPPRP vs RPSRPSRP

    # Access opponent's history
    (8, {'A': 'R!P!S!R!P!P?!S?!R?!A'}, {'A': 'S!P!R!S!P!S!R!P!'}),  # RPSR + opponent's PSR

    # Complex strategy
    (5, {'A': 'R!P?>>!A'}, {'A': '~!A'}),  # Counter to opponent's previous move + 2

    # Error cases
    (1, {'A': '-!A'}, {'A': 'R!A'}),  # Stack underflow
    (1, {'A': 'Q!A'}, {'A': 'R!A'}),  # Unknown command

    # Edge cases for @ and ?
    (3, {'A': 'R!P!P@!S@!R@!A'}, {'A': 'R!P!S!'}),  # Access own moves (including non-existent)
    (3, {'A': 'R!P!P?!S?!R?!A'}, {'A': 'P!S!R!'}),  # Access opponent's moves (including non-existent)
]
