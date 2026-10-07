"""Module 04 exercises. Fill the TODOs, run:  python 04-control-flow/exercises.py"""


# 1. Return "fizz" for multiples of 3, "buzz" for multiples of 5, "fizzbuzz" for both, else the number as a string.
def fizzbuzz(n: int) -> str:
    # TODO
    ...


# 2. Return the grade letter: 90+ "A", 80+ "B", 70+ "C", else "F".
def grade(score: int) -> str:
    # TODO
    ...


# 3. Return the sum of all numbers from 1 to n (use a loop, not the formula).
def sum_to(n: int) -> int:
    # TODO
    ...


# 4. Return the list of even numbers from 1..n using a comprehension.
def evens_up_to(n: int) -> list:
    # TODO
    ...


# 5. Return True if n is prime (n >= 2), using a loop up to the square root.
def is_prime(n: int) -> bool:
    # TODO
    ...


# 6. Return the index of the first item greater than limit, or -1 if there is none. (use enumerate)
def first_above(nums: list, limit: int) -> int:
    # TODO
    ...


# 7. Return the first n Fibonacci numbers: n=6 -> [0, 1, 1, 2, 3, 5]
def fibonacci(n: int) -> list:
    # TODO
    ...


# 8. Given payments [100, 100, 50, ...] and a target, return how many payments are needed to reach it
#    (stop as soon as the running total >= target). Return -1 if never reached. (use break / else)
def payments_needed(payments: list, target: int) -> int:
    # TODO
    ...


# 9. Return a dict {n: n*n} for n in 1..k using a dict comprehension.
def squares_dict(k: int) -> dict:
    # TODO
    ...


# 10. Count how many numbers in nums are divisible by 3 and positive, using a generator or comprehension with sum().
def count_pos_div3(nums: list) -> int:
    # TODO
    ...


# 11. Flatten a list of lists: [[1, 2], [3], []] -> [1, 2, 3] (nested comprehension)
def flatten(rows: list) -> list:
    # TODO
    ...


# 12. Gameya mini-logic: given a start week (int) and the current week (int) and the total weeks, return
#     "not started" if current < start, "finished" if current > total, else "week N of TOTAL".
def gameya_status(start: int, current: int, total: int) -> str:
    # TODO
    ...


if __name__ == "__main__":
    assert [fizzbuzz(n) for n in (3, 5, 15, 7)] == ["fizz", "buzz", "fizzbuzz", "7"]
    assert [grade(s) for s in (95, 85, 75, 10)] == ["A", "B", "C", "F"]
    assert sum_to(10) == 55 and sum_to(0) == 0
    assert evens_up_to(10) == [2, 4, 6, 8, 10]
    assert [n for n in range(20) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19]
    assert first_above([1, 5, 9, 12], 8) == 2
    assert first_above([1, 2], 8) == -1
    assert fibonacci(6) == [0, 1, 1, 2, 3, 5]
    assert fibonacci(0) == []
    assert payments_needed([100, 100, 50, 300], 250) == 3
    assert payments_needed([10, 10], 100) == -1
    assert squares_dict(4) == {1: 1, 2: 4, 3: 9, 4: 16}
    assert count_pos_div3([3, 6, -3, 4, 9, 0]) == 3
    assert flatten([[1, 2], [3], []]) == [1, 2, 3]
    assert gameya_status(1, 0, 10) == "not started"
    assert gameya_status(1, 11, 10) == "finished"
    assert gameya_status(1, 4, 10) == "week 4 of 10"
    print("All checks passed")
