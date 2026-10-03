# Task Scheduler

A command-line task scheduler that orders tasks so every dependency is finished first, and picks the most urgent task whenever there is a choice. Built for the GDG-USAR Tech Team task (DSA, Task 3).

## Features
- Create tasks with a **priority** (1 = highest, 5 = lowest) and a **deadline** (YYYY-MM-DD)
- Add **dependencies** ("Deploy" needs "Build UI" first)
- Produces a **valid completion order**
- Uses a **min-heap** to choose the most urgent ready task (priority, then deadline)
- **Detects circular dependencies** and prints the exact loop
- Input validation: empty names, duplicates, bad priority, bad date, unknown tasks, self-dependency

## How to run
Requires Python 3.8+ (no extra packages).

```
python Task_Scheduler.py
```
(On Windows, use `py Task_Scheduler.py` if `python` is not recognised.)

Menu: `1` add task, `2` add dependency, `3` show tasks, `4` run scheduler, `5` load demo data, `6` exit.

## Example
Demo data: Design DB -> Build API -> (Build UI, Write Tests) -> Deploy

Output:
```
1. Design DB  (priority 1, due 2026-10-10)
2. Build API  (priority 2, due 2026-10-15)
3. Write Tests  (priority 2, due 2026-10-20)
4. Build UI  (priority 3, due 2026-10-18)
5. Deploy  (priority 1, due 2026-10-25)
```
Write Tests runs before Build UI because both are ready at the same time and Write Tests has the higher priority.

Cycle example: add "Design DB depends on Deploy" and run again:
```
CIRCULAR DEPENDENCY DETECTED
Cycle: Build UI -> Deploy -> Design DB -> Build API -> Build UI
```

## How it works
1. **Graph:** tasks are nodes; "A depends on B" is an edge B -> A, stored as an adjacency list.
2. **In-degree:** count the unfinished prerequisites of each task.
3. **Kahn's algorithm:** tasks with in-degree 0 are ready. Put them in a min-heap keyed by (priority, deadline, name). Pop the best one, add it to the order, and reduce the in-degree of tasks that depend on it. Repeat.
4. **Cycle check:** if the final order has fewer tasks than exist, the leftover tasks are in a cycle. We walk backwards through their prerequisites until a task repeats to find the loop.

## Complexity
V = number of tasks, E = number of dependencies.
- **Time:** O((V + E) log V). Each task enters and leaves the heap once (log V each), and each edge is processed once.
- **Space:** O(V + E) for the adjacency list, in-degree table and heap.

## Files
- `Task_Scheduler.py` - the program
- `DECISIONS.md` - design decisions and edge cases
- `AI_USAGE.md` - how AI tools were used
