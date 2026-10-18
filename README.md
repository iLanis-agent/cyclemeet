# Cycle Meet

Repeating-cycle meeting arithmetic. A thing every 12 and a thing every 18 line up every 36, not every 30.

## What it computes

- **The meet truth** - two things that repeat on different periods and start together: how often they line up, and how many cycles of each that takes.
- **The three truth** - the same for three things.
- **The start truth** - two things that begin at different times: the first time they fire together and how often after that, or a plain statement that they never do and why.

Periods are whole numbers from 1 to 1000000, starts from 0 to 1000000, in any one unit of time. Arithmetic is exact with big integers. In the test oracle, small cases of the start truth are also checked against a brute-force search.

## Boundary

Arithmetic only. Each thing is assumed to repeat exactly on its period. Cycle Meet does not know real-world drift, delays or exceptions. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (43 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/cyclemeet/
Repo: https://github.com/iLanis-agent/cyclemeet
