# The RPS Machine

We're building a simple forth-like stack machine emulator for writing Rock, Paper, Scissors playing algorithms.

The machine accepts as input a number k and two dictionaries from A, B, C to strings, runs k rounds of iterated RPS between the programs they represent, and returns the score and a full run log (for each program, for each move played, a list of machine states after each opcode that resulted in that move being played).

R=2 P=0 S=1, all math is mod 3.

The commands are:

```
R (-- R) push an R
P (-- P) push a P
S (-- S) push an S
~ (-- x) Push a random value
! (x -- ) Play the top of the stack
> (x -- x+1)
< (x -- x-1)
- (x y -- x-y)
+ (x y -- x+y)
^ (x y -- S if x=y=R else P)
X (x -- )
8 (x -- x x)
% (x y -- y x)
[ (x y -- x y x)
A ( -- ) Call A (with tail call optimization)
B ( -- ) Call B (with tail call optimization)
C ( -- ) Call C (with tail call optimization)
@ (i -- x) Push our i-th last output value
? (i -- x) Push opponent's i-th last output value
```

Before implementing the machine, design a test suite as a list of inputs that exercise each feature of the machine separately (the first might be `(3, {'A': 'R!A'}, {'A': 'R!P!S!''})`).

To run the test suite, run a full game for each input, then save a JSON file of all results, like `[{"input": ..., "matches: "RR=RP>RS<", logs: {"<": [...], ">": ...}}, ...]`.