# Module 04: Control flow

## 1. if / elif / else
```python
score = 72
if score >= 90:
    grade = "A"
elif score >= 70:
    grade = "B"
else:
    grade = "C"
```
- The colon and the indentation define the block. No parentheses needed around the condition.
- One-line conditional expression: `label = "adult" if age >= 18 else "minor"`.
- Conditions use truthiness: `if items:`, `if not name:`.
- `match` (3.10+) is structural pattern matching; learn it later. `if/elif` covers this week.

## 2. for loops
```python
for n in [1, 2, 3]:
    print(n)

for i in range(5):  # 0..4
    ...
for i in range(1, 11, 2):  # 1, 3, 5, 7, 9
    ...

for i, name in enumerate(["a", "b"], start=1):
    print(i, name)

for a, b in zip([1, 2], ["x", "y"]):
    ...
for key, value in my_dict.items():
    ...
```
`for` works on anything iterable (list, string, dict, range, file). Do **not** loop with `range(len(x))` just to index; use `enumerate`.

## 3. while loops
```python
count = 0
while count < 3:
    count += 1

while True:  # loop until we break
    answer = input("> ")
    if answer == "quit":
        break
```
Make sure something inside changes the condition, or you loop forever (Ctrl+C stops it).

## 4. break, continue, else
- `break` leaves the loop. `continue` skips to the next iteration.
- `for ... else`: the `else` runs only if the loop **did not** `break`. Handy for searches.
```python
for n in nums:
    if n == target:
        print("found")
        break
else:
    print("not found")
```

## 5. Comprehensions
```python
squares = [n * n for n in range(10)]
evens = [n for n in range(10) if n % 2 == 0]
labels = ["even" if n % 2 == 0 else "odd" for n in range(5)]
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
lookup = {w: len(w) for w in words}
unique = {w.lower() for w in words}
```
A comprehension is a loop that builds a collection. If it gets hard to read, use a normal `for` loop.

## 6. Patterns you will use constantly
```python
# accumulate
total = 0
for p in payments:
    total += p

# filter then build
paid = [m for m in members if m["paid"]]

# find first match
first_late = next((m for m in members if not m["paid"]), None)

# loop with index and a guard
for i, m in enumerate(members, 1):
    if not m["name"]:
        continue
```

## 7. Truthiness in conditions, again
`if x:` is true for non-empty/non-zero. If `0` is a valid value, test explicitly: `if x is not None:`.

## 8. Exercises hint
Write the plain loop first; turn it into a comprehension only when it works.

## Check your understanding
1. What is the difference between `break` and `continue`?
2. When does the `else` of a `for` loop run?
3. Why prefer `enumerate` over `range(len(x))`?
4. Rewrite `result = []; for n in nums: if n > 0: result.append(n*2)` as a comprehension.
5. How do you stop an infinite `while True` loop from the code, and from the terminal?

Then do `exercises.py` and the week project.

## Revision companion (optional)
An interactive summary of this lesson, generated with Google NotebookLM: [Python Control Flow](https://notebooklm.link.google/BypzOY5qK266). Use it for a quick recap after you finish the lesson and the exercises. This lesson stays the source of truth; the link is hosted by Google and may change.
