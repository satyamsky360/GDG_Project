"""
Task Scheduler - GDG-USAR Tech Team Task (DSA)

Idea:
  - Tasks are nodes in a graph. "A depends on B" is an edge B -> A.
  - Kahn's algorithm (topological sort) gives a valid order.
  - A min-heap picks the MOST URGENT task among those that are ready.
  - If some tasks never become ready, they form a cycle -> we report it.

Complexity (V = tasks, E = dependencies):
  Time  : O((V + E) log V)   -> each task is pushed/popped from the heap once
  Space : O(V + E)           -> adjacency list + in-degree + heap
"""

import heapq
from datetime import datetime


class TaskScheduler:
    def __init__(self):
        self.tasks = {}          # name -> (priority, deadline)
        self.graph = {}          # prerequisite -> list of tasks that depend on it
        self.prereqs = {}        # task -> list of its prerequisites

    # ---------- Adding data ----------
    def add_task(self, name, priority, deadline):
        """priority: 1 (highest) to 5 (lowest). deadline: YYYY-MM-DD."""
        if not name:
            raise ValueError("Task name cannot be empty.")
        if name in self.tasks:
            raise ValueError(f"Task '{name}' already exists.")
        if not 1 <= priority <= 5:
            raise ValueError("Priority must be between 1 (highest) and 5 (lowest).")
        try:
            date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format.")

        self.tasks[name] = (priority, date)
        self.graph[name] = []
        self.prereqs[name] = []

    def add_dependency(self, task, depends_on):
        """'task' can only start after 'depends_on' is finished."""
        if task not in self.tasks or depends_on not in self.tasks:
            raise ValueError("Both tasks must exist first.")
        if task == depends_on:
            raise ValueError("A task cannot depend on itself.")
        if depends_on in self.prereqs[task]:
            raise ValueError("This dependency already exists.")

        self.graph[depends_on].append(task)   # edge: depends_on -> task
        self.prereqs[task].append(depends_on)

    # ---------- Core algorithm ----------
    def schedule(self):
        """Returns (order, cycle). If cycle is not None, no valid order exists."""
        # Step 1: in-degree = how many unfinished prerequisites each task has
        in_degree = {t: len(self.prereqs[t]) for t in self.tasks}

        # Step 2: put all tasks with no prerequisites in a min-heap.
        # Heap compares (priority, deadline, name) -> most urgent comes out first.
        heap = []
        for t, d in in_degree.items():
            if d == 0:
                heapq.heappush(heap, (*self.tasks[t], t))

        order = []
        while heap:
            _, _, task = heapq.heappop(heap)
            order.append(task)
            # Finishing 'task' may unlock the tasks that depend on it
            for nxt in self.graph[task]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    heapq.heappush(heap, (*self.tasks[nxt], nxt))

        # Step 3: if we could not schedule everything, there is a cycle
        if len(order) < len(self.tasks):
            stuck = {t for t in self.tasks if in_degree[t] > 0}
            return order, self._find_cycle(stuck)
        return order, None

    def _find_cycle(self, stuck):
        """Walk backwards through prerequisites until a task repeats."""
        current = next(iter(stuck))
        path = []
        while current not in path:
            path.append(current)
            # every stuck task has at least one stuck prerequisite
            current = next(p for p in self.prereqs[current] if p in stuck)
        cycle = path[path.index(current):]
        cycle.reverse()                    # show in "runs before" order
        return cycle + [cycle[0]]          # close the loop for display

    # ---------- Display ----------
    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
            return
        print(f"\n{'Task':<18}{'Priority':<10}{'Deadline':<13}Depends on")
        print("-" * 60)
        for t, (p, d) in self.tasks.items():
            deps = ", ".join(self.prereqs[t]) or "-"
            print(f"{t:<18}{p:<10}{d!s:<13}{deps}")

    def run(self):
        if not self.tasks:
            print("Add some tasks first.")
            return
        order, cycle = self.schedule()
        if cycle:
            print("\nCIRCULAR DEPENDENCY DETECTED - no valid order exists.")
            print("Cycle:", " -> ".join(cycle))
            print("Remove one of these dependencies and try again.")
        else:
            print("\nValid completion order:")
            for i, t in enumerate(order, 1):
                p, d = self.tasks[t]
                print(f"  {i}. {t}  (priority {p}, due {d})")


def load_demo(s):
    s.add_task("Design DB", 1, "2026-10-10")
    s.add_task("Build API", 2, "2026-10-15")
    s.add_task("Build UI", 3, "2026-10-18")
    s.add_task("Write Tests", 2, "2026-10-20")
    s.add_task("Deploy", 1, "2026-10-25")
    s.add_dependency("Build API", "Design DB")
    s.add_dependency("Build UI", "Build API")
    s.add_dependency("Write Tests", "Build API")
    s.add_dependency("Deploy", "Build UI")
    s.add_dependency("Deploy", "Write Tests")
    print("Demo tasks loaded.")


def main():
    s = TaskScheduler()
    menu = """
=== Task Scheduler ===
1. Add task
2. Add dependency
3. Show tasks
4. Run scheduler
5. Load demo data
6. Exit
"""
    while True:
        print(menu)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                name = input("Task name: ").strip()
                pr = int(input("Priority (1=highest, 5=lowest): "))
                dl = input("Deadline (YYYY-MM-DD): ").strip()
                s.add_task(name, pr, dl)
                print("Task added.")
            elif choice == "2":
                t = input("Task: ").strip()
                d = input("Depends on (must finish first): ").strip()
                s.add_dependency(t, d)
                print("Dependency added.")
            elif choice == "3":
                s.show_tasks()
            elif choice == "4":
                s.run()
            elif choice == "5":
                load_demo(s)
            elif choice == "6":
                print("Bye!")
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
