# Module 03: Collections (list, tuple, dict, set)

## 1. Choosing a collection
| Type | Ordered | Mutable | Duplicates | Use it for |
|---|---|---|---|---|
| `list` `[1, 2]` | yes | yes | yes | A sequence you add to and change |
| `tuple` `(1, 2)` | yes | **no** | yes | A fixed record, a return of several values |
| `dict` `{"a": 1}` | yes (insertion order) | yes | keys unique | Look things up by a key |
| `set` `{1, 2}` | no | yes | **no** | Membership tests, removing duplicates, set maths |

## 2. Lists
```python
nums = [5, 3, 8]
nums.append(1)  # add at the end
nums.insert(0, 9)  # add at index
nums.extend([7, 7])  # add many
nums.remove(7)  # removes first 7
last = nums.pop()  # removes and returns the last (pop(0) removes the first)
nums.sort()  # in place, returns None!
sorted(nums)  # new list, original untouched
nums.reverse()
len(nums), 8 in nums, nums.index(8), nums.count(7)
```
- Indexing and slicing like strings: `nums[0]`, `nums[-1]`, `nums[1:3]`, `nums[::-1]`. Slicing makes a **copy**.
- `sort(key=...)`: `people.sort(key=lambda p: p["age"])`. `sorted(words, key=len, reverse=True)`.
- Unpacking: `a, b = [1, 2]`, `first, *rest = [1, 2, 3]`.

### Mutability and aliasing (the big one)
```python
a = [1, 2]
b = a  # same list, two names
b.append(3)
print(a)  # [1, 2, 3]
c = a.copy()  # or a[:] or list(a): a new (shallow) copy
```
Passing a list to a function passes the **same object**, so mutating it in the function changes the caller's list. Nested lists: `.copy()` is shallow; use `copy.deepcopy` for nested data.

Common trap: `[[0] * 3] * 3` creates three references to the **same** row. Use `[[0] * 3 for _ in range(3)]`.

## 3. Tuples
Immutable. `point = (3, 4)`, `x, y = point`. A one-item tuple needs a comma: `(5,)`. Functions that "return several values" return a tuple. Tuples can be dict keys (lists cannot). Immutable means the tuple can't change which objects it holds; a list inside a tuple can still change.

## 4. Dicts
```python
user = {"name": "Mohamed", "age": 30}
user["city"] = "Cairo"  # add or update
user["name"]  # KeyError if missing
user.get("phone")  # None if missing
user.get("phone", "n/a")  # default
"name" in user  # checks keys
del user["age"]
user.pop("city", None)
for k in user:
    ...
for k, v in user.items():
    ...
user.keys(), user.values()
user.setdefault("tags", []).append("x")
{**user, "role": "admin"}  # merge (3.9+: user | other)
```
- Keys must be hashable (str, int, tuple of hashables; not list/dict/set).
- Counting pattern: `counts[w] = counts.get(w, 0) + 1`. (Later: `collections.Counter`.)
- Dicts keep insertion order (guaranteed since 3.7).

## 5. Sets
```python
s = {1, 2, 3}
s.add(4)
s.discard(9)  # discard does not raise if missing
a | b  # union
a & b  # intersection
a - b  # difference
a ^ b  # symmetric difference
list(set(items))  # dedupe (order not kept)
```
`{}` is an empty **dict**; an empty set is `set()`.

## 6. Comprehensions (preview, full in Module 04)
```python
squares = [n * n for n in range(5)]
evens = [n for n in range(10) if n % 2 == 0]
by_name = {p["name"]: p for p in people}
unique_lengths = {len(w) for w in words}
```

## 7. Useful built-ins on collections
`len`, `sum`, `min`, `max`, `sorted`, `reversed`, `enumerate(seq, start=1)`, `zip(a, b)`, `any(...)`, `all(...)`.

## Check your understanding
1. Why does `b = a; b.append(3)` change `a`? How do you avoid that?
2. `sort()` vs `sorted()`: what does each return?
3. Which collection would you use to check "has this user been seen before?" in a loop of a million items, and why?
4. What happens on `d["missing"]` and how is `d.get("missing")` different?
5. Why can a tuple be a dict key but a list can't?
6. What is the result of `{1, 2, 3} & {2, 3, 4}`?

Then do `exercises.py`.

## Revision companion (optional)
An interactive summary of this lesson, generated with Google NotebookLM: [Mastering Python Collections](https://notebooklm.link.google/nfBMqTXIerPx). Use it for a quick recap after you finish the lesson and the exercises. This lesson stays the source of truth; the link is hosted by Google and may change.
