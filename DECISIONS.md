# Design Decisions

## 1. Algorithm: Kahn's algorithm instead of DFS topological sort
Both give a valid order. I chose Kahn's (BFS-style) because it works naturally with a heap: at every step I have a set of "ready" tasks and can pick the most urgent one. A DFS-based sort gives an order but makes it harder to apply priority between independent tasks.

## 2. Data structure: min-heap keyed by (priority, deadline, name)
Python's `heapq` compares tuples left to right, so lower priority number wins, then the earlier deadline, then the name as a tie-breaker (this also makes the output deterministic). Alternative considered: re-sorting the ready list every step, which is O(V log V) per step instead of O(log V).

## 3. Design change: report the actual cycle, not just "cycle found"
First idea: if the order is shorter than the task count, print "cycle detected". This is not very helpful because the user does not know which dependency to remove. I changed it to walk backwards through the stuck tasks' prerequisites until a task repeats, then print that loop (A -> B -> C -> A). Every stuck task has at least one stuck prerequisite, so the walk always ends in a cycle.

## 4. Edge cases handled
- Task depending on itself (rejected immediately)
- Duplicate task names and duplicate dependencies
- Dependency on a task that does not exist
- Priority outside 1-5 and invalid date format
- Empty task list when running the scheduler

## 5. Trade-off: cycles are detected when scheduling, not when adding
I could reject a dependency the moment it creates a cycle, but that needs a search on every insert. I kept insertion O(1) and detect cycles once in `schedule()`, which also shows the loop clearly.

## 6. Not done (known limitation)
Deadlines affect ordering only as a tie-breaker after priority. The scheduler does not warn that a task will miss its deadline, since there are no task durations.
