import os
import pytest
import json
import subprocess
from typing import Dict, List, Tuple
from rps import run_game

test_suite = [
    # Basic moves, scoring, and random
    (3, {"A": "R!A"}, {"A": "P!A"}),  # R vs P
    (3, {"A": "P!A"}, {"A": "S!A"}),  # P vs S
    (3, {"A": "~!A"}, {"A": "R!A"}),  # Random vs constant
    # Increment, decrement, and cycling
    (3, {"A": "R>!P>!S>!A"}, {"A": "S!R!P!"}),  # R->P->S->R
    # Addition, subtraction, and special operations
    (4, {"A": "RP-!SP+!RR^!RP^!A"}, {"A": "R!A"}),  # S, R, S, P vs R, R, R, R
    # Stack operations (duplicate, swap, copy)
    (3, {"A": "R8S%[!!!"}, {"A": "R!A"}),  # RR, PR, RRP vs SSSSS
    # Subroutines
    (3, {"A": "R!B", "B": "P!C", "C": "S!A"}, {"A": "R!A"}),  # A->B->C->A
    # Access own and opponent's history
    (
        9,
        {"A": "RPS!!!P@S@S@R@R@R@!!!!!!A"},
        {"A": "R!A"},
    ),
    # Access opponent's history
    (
        9,
        {"A": "SSS!!!P?S?S?R?R?R?!!!!!!A"},
        {"A": "SPR!!!RRRRRR!!!!!!"},
    ),  # RPSR + opponent's PSR
    # Complex strategy
    (5, {"A": "R!P?>>!A"}, {"A": "R!S!P!A"}),  # Counter to opponent's previous move + 2
    # Error cases
    (1, {"A": "-!A"}, {"A": "R!A"}),  # Stack underflow
    (1, {"A": "Q!A"}, {"A": "R!A"}),  # Unknown command
    # Edge cases for @ and ?
    (
        1,
        {"A": "S@!"},
        {"A": "R!A"},
    ),  # Access own moves (including non-existent)
    (
        2,
        {"A": "R!P@!"},
        {"A": "R!A"},
    ),  # Access own moves (including non-existent)
    (
        2,
        {"A": "R!S@!"},
        {"A": "R!A"},
    ),  # Access own moves (including non-existent)
    (
        3,
        {"A": "R!R!S@!"},
        {"A": "R!A"},
    ),  # Access own moves (including non-existent)
    (
        3,
        {"A": "R!R!P@!"},
        {"A": "R!A"},
    ),  # Access own moves (including non-existent)
    (
        3,
        {"A": "R!P!P?!S?!R?!A"},
        {"A": "P!S!R!"},
    ),  # Access opponent's moves (including non-existent)
]

SEED = 42  # Constant seed for all tests
RESULTS_FILENAME = "test_results.json"


def simplify_log(prog, full_log):
    simplified_log = []
    for round_log in full_log:
        if "error" in round_log:
            # If there's an error, add it to the simplified log and stop processing
            simplified_log.append(f"Error: {round_log['error']}")
            break

        round_states = []
        for state in round_log["states"]:
            if prog[state["ip"]] in "ABC":
                round_states.append(prog[state["ip"]])
            stack_str = "".join(state["stack"])
            if not round_states or stack_str != round_states[-1]:
                round_states.append(stack_str)
        simplified_log.append(round_states)
    return simplified_log


def run_test_suite(
    test_suite: List[Tuple[int, Dict[str, str], Dict[str, str]]]
) -> List[Dict]:
    results = []
    for k, prog1, prog2 in test_suite:
        score, match_log, full_log = run_game(k, prog1, prog2, SEED)
        result = {
            "input": {"k": k, "<": prog1, ">": prog2},
            "matches": match_log,
            "score": score,
            "log": full_log,
        }
        if not os.environ.get("DEBUG"):
            result["log"] = {
                    "<": simplify_log(prog1["A"], full_log["<"]),
                    ">": simplify_log(prog2["A"], full_log[">"]),
                }
        results.append(result)
    return results


def get_head_commit_file_content(file_path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "show", f"HEAD:{file_path}"], universal_newlines=True
        )
    except subprocess.CalledProcessError:
        return ""


def save_results(results: List[Dict], filename: str):
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)


def test_rps_stack_machine():
    # Run the current test suite
    current_results = run_test_suite(test_suite)

    # Save current results to disk
    save_results(current_results, RESULTS_FILENAME)

    # Get the previous results from the HEAD commit
    previous_content = get_head_commit_file_content(RESULTS_FILENAME)

    if not previous_content:
        pytest.fail(
            f"No previous test results found in HEAD commit. Run tests and commit {RESULTS_FILENAME} first."
        )

    previous_results = json.loads(previous_content)

    # Compare the number of test cases
    if len(current_results) != len(previous_results):
        pytest.fail(
            f"Number of test cases changed. Previous: {len(previous_results)}, Current: {len(current_results)}"
        )

    # Compare results and generate error message in one pass
    changes = []
    for curr, prev in zip(current_results, previous_results):
        if curr["matches"] != prev["matches"]:
            change = (
                f"<: {curr['input']['<']['A']}\n"
                f">: {curr['input']['>']['A']}\n"
                f"- matches: {prev['matches']}\n"
                f"+ matches: {curr['matches']}"
            )
            changes.append(change)
            for p in "<>":
                if "log" not in prev:
                    prev["log"] = {"<": [[]], ">": [[]]}
                p, c = prev["log"][p][-1], curr["log"][p][-1]
                if isinstance(c, str) != isinstance(p, str):
                    changes.append("- " + (p if isinstance(p, str) else ""))
                    changes.append("+ " + (c if isinstance(c, str) else ""))

    # If changes were found, join them into a single error message and fail
    if changes:
        error_message = "Test results changed:\n\n" + "\n".join(changes)
        pytest.fail(error_message)

    # If we got here, all tests passed and results match
    assert True


if __name__ == "__main__":
    pytest.main([__file__])
