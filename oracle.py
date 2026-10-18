#!/usr/bin/env python3
# Cycle Meet oracle - mirrors engine.js. Small cases are also checked by brute force.
import json, math

def _int(x, label, lo, hi):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or math.floor(x) != x or x < lo or x > hi:
        raise ValueError(f"{label} must be a whole number from {lo} to {hi}")
    return int(x)

def _cyc(k): return f"{k} cycle" if k == 1 else f"{k} cycles"

def meet_truth(a, b):
    x = _int(a, "first period", 1, 1000000); y = _int(b, "second period", 1, 1000000)
    l = x // math.gcd(x, y) * y
    return f"Something that repeats every {a} and something that repeats every {b} meet again every {l} ({_cyc(l // x)} of the first, {_cyc(l // y)} of the second)."

def three_truth(a, b, c):
    x = _int(a, "first period", 1, 1000000); y = _int(b, "second period", 1, 1000000); z = _int(c, "third period", 1, 1000000)
    l = x // math.gcd(x, y) * y
    l = l // math.gcd(l, z) * z
    return f"Three things that repeat every {a}, {b} and {c} all meet again every {l} ({_cyc(l // x)} of the first, {_cyc(l // y)} of the second, {_cyc(l // z)} of the third)."

def start_truth(a, start_a, b, start_b):
    x = _int(a, "first period", 1, 1000000); s = _int(start_a, "first start", 0, 1000000)
    y = _int(b, "second period", 1, 1000000); u = _int(start_b, "second start", 0, 1000000)
    head = f"Something that fires at {start_a} and then every {a}, and something that fires at {start_b} and then every {b}, "
    g = math.gcd(x, y); diff = u - s
    brute = None
    if x // g * y <= 2000000:
        t = max(s, u)
        brute = next((t for t in range(max(s, u), max(s, u) + x // g * y + 1) if (t - s) % x == 0 and (t - u) % y == 0), None)
    if diff % g != 0:
        assert brute is None
        return head + f"never fire together: the starts differ by {abs(diff)}, which is not a multiple of {g}, the greatest common divisor of {a} and {b}."
    l = x // g * y; m = y // g
    k = ((diff // g) % m) * (pow((x // g) % m, -1, m) if m > 1 else 0) % m
    t = (s + x * k) % l
    top = max(s, u)
    if t < top:
        t += -(-(top - t) // l) * l
    if brute is not None:
        assert brute == t, (a, start_a, b, start_b, brute, t)
    return head + f"first fire together at {t}, then every {l} after that."

FNS = {"meetTruth": meet_truth, "threeTruth": three_truth, "startTruth": start_truth}
CASES = [
    ("meetTruth", [12, 18]), ("meetTruth", [7, 13]), ("meetTruth", [5, 5]), ("meetTruth", [1, 9]), ("meetTruth", [6, 3]), ("meetTruth", [1, 1]),
    ("meetTruth", [999999, 1000000]), ("meetTruth", [1000000, 1000000]), ("meetTruth", [4, 6]),
    ("meetTruth", [0, 5]), ("meetTruth", [5, 1000001]), ("meetTruth", [2.5, 4]),
    ("threeTruth", [4, 6, 10]), ("threeTruth", [3, 5, 7]), ("threeTruth", [2, 2, 2]), ("threeTruth", [1, 1, 1]), ("threeTruth", [999999, 1000000, 999998]),
    ("threeTruth", [6, 10, 15]), ("threeTruth", [8, 12, 20]), ("threeTruth", [0, 1, 1]), ("threeTruth", [1, 1, 1000001]),
    ("startTruth", [12, 3, 18, 5]), ("startTruth", [12, 3, 18, 9]), ("startTruth", [12, 0, 18, 0]), ("startTruth", [7, 2, 13, 5]), ("startTruth", [5, 3, 5, 3]),
    ("startTruth", [5, 3, 5, 4]), ("startTruth", [6, 4, 4, 0]), ("startTruth", [6, 5, 4, 0]), ("startTruth", [10, 100, 15, 0]), ("startTruth", [1, 0, 1, 0]),
    ("startTruth", [1, 7, 9, 2]), ("startTruth", [9, 2, 1, 7]), ("startTruth", [4, 1, 6, 3]), ("startTruth", [4, 3, 6, 1]), ("startTruth", [24, 5, 36, 17]),
    ("startTruth", [999999, 1, 1000000, 999999]), ("startTruth", [1000000, 1000000, 999999, 0]), ("startTruth", [1000000, 0, 1000000, 1]),
    ("startTruth", [0, 1, 5, 1]), ("startTruth", [5, 1, 5, 1000001]), ("startTruth", [5, -1, 5, 1]), ("startTruth", [5, 1, 5.5, 1]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
