# =========================================
# Predictive Parsing Table (LL(1))
# =========================================

from collections import defaultdict

# Grammar
grammar = {
    "E": ["TR"],
    "R": ["+TR", "ε"],
    "T": ["FY"],
    "Y": ["*FY", "ε"],
    "F": ["(E)", "id"]
}

start_symbol = "E"
non_terminals = grammar.keys()

# Initialize FIRST and FOLLOW
FIRST = defaultdict(set)
FOLLOW = defaultdict(set)


# FIRST of symbol
def first(symbol):
    if symbol not in grammar:
        return {symbol}
    return FIRST[symbol]


# Compute FIRST sets
def compute_first():
    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for prod in grammar[nt]:
                i = 0
                while i < len(prod):
                    before = len(FIRST[nt])
                    FIRST[nt] |= first(prod[i]) - {"ε"}
                    after = len(FIRST[nt])

                    if "ε" not in first(prod[i]):
                        break
                    i += 1
                else:
                    FIRST[nt].add("ε")

                if after > before:
                    changed = True


# Compute FOLLOW sets
def compute_follow():
    FOLLOW[start_symbol].add("$")

    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for prod in grammar[nt]:
                for i, symbol in enumerate(prod):
                    if symbol in grammar:
                        before = len(FOLLOW[symbol])

                        if i + 1 < len(prod):
                            FOLLOW[symbol] |= first(prod[i + 1]) - {"ε"}
                            if "ε" in first(prod[i + 1]):
                                FOLLOW[symbol] |= FOLLOW[nt]
                        else:
                            FOLLOW[symbol] |= FOLLOW[nt]

                        if len(FOLLOW[symbol]) > before:
                            changed = True


# Build Predictive Parsing Table
def build_parsing_table():
    table = defaultdict(dict)

    for nt in grammar:
        for prod in grammar[nt]:
            prod_first = set()
            i = 0

            while i < len(prod):
                prod_first |= first(prod[i]) - {"ε"}
                if "ε" not in first(prod[i]):
                    break
                i += 1
            else:
                prod_first.add("ε")

            for terminal in prod_first - {"ε"}:
                table[nt][terminal] = prod

            if "ε" in prod_first:
                for terminal in FOLLOW[nt]:
                    table[nt][terminal] = "ε"

    return table


# Run steps
compute_first()
compute_follow()
parsing_table = build_parsing_table()

# Display Parsing Table
print("Predictive Parsing Table:\n")
for nt in parsing_table:
    for t in parsing_table[nt]:
        print(f"M[{nt}, {t}] = {nt} → {parsing_table[nt][t]}")
