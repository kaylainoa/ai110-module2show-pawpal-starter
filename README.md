# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
=== Sorted by time ===
  08:00 — Feeding (Mochi)
  08:00 — Morning walk (Biscuit)
  12:00 — Litter box cleanup (Mochi)
  17:00 — Fetch playtime (Biscuit)
  18:00 — Evening walk (Biscuit)

=== Filtered: Mochi's incomplete tasks ===
  08:00 — Feeding
  12:00 — Litter box cleanup

=== Recurring task: completing Mochi's daily feeding (t2) ===
  t2: Feeding (done), due 2026-07-08
  t4: Litter box cleanup (pending), due 2026-07-08
  t2-2026-07-09: Feeding (pending), due 2026-07-09

=== Conflict detection ===
  WARNING: Conflict at 08:00: Feeding (Mochi), Morning walk (Biscuit), Vet check-in call (Biscuit)

Today's Schedule:
  08:00 — Feeding (10 min) [priority: high] for Mochi
  08:10 — Evening walk (30 min) [priority: high] for Biscuit
  08:40 — Litter box cleanup (15 min) [priority: medium] for Mochi
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The suite (`tests/test_pawpal.py`, 14 tests) covers:

- **Task/Pet basics** — `mark_complete()` flips status; `add_task()` grows the pet's task list.
- **Sorting** — `sort_by_time()` orders tasks chronologically by `HH:MM`, including the empty-list edge case.
- **Filtering** — `filter_tasks()` by pet name and/or completion status.
- **Priority planning** — `build_plan()` sorts shuffled tasks by priority, skips lower-priority tasks once the time budget runs out, and handles an empty task list.
- **Recurring tasks** — completing a `daily` task schedules the next occurrence at `today + 1 day`; a `weekly` task at `today + 1 week`; a one-off task does not recur.
- **Conflict detection** — flags two tasks at the exact same time, ignores completed tasks, and returns no warnings when times don't collide.
- **Multi-pet aggregation** — `Owner.all_tasks()` correctly pools tasks across more than one pet.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 14 items

tests/test_pawpal.py::test_mark_complete_changes_task_status PASSED      [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 14%]
tests/test_pawpal.py::test_sort_by_time_orders_chronologically PASSED    [ 21%]
tests/test_pawpal.py::test_filter_tasks_by_pet_and_completion_status PASSED [ 28%]
tests/test_pawpal.py::test_mark_task_complete_schedules_next_occurrence_for_daily_task PASSED [ 35%]
tests/test_pawpal.py::test_mark_task_complete_does_not_recur_for_one_off_task PASSED [ 42%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time_tasks PASSED [ 50%]
tests/test_pawpal.py::test_detect_conflicts_ignores_completed_tasks PASSED [ 57%]
tests/test_pawpal.py::test_detect_conflicts_with_no_duplicate_times_returns_empty_list PASSED [ 64%]
tests/test_pawpal.py::test_sort_by_time_with_empty_list_returns_empty_list PASSED [ 71%]
tests/test_pawpal.py::test_build_plan_with_no_tasks_returns_empty_plan PASSED [ 78%]
tests/test_pawpal.py::test_build_plan_prioritizes_and_skips_when_time_runs_out PASSED [ 85%]
tests/test_pawpal.py::test_owner_all_tasks_aggregates_multiple_pets PASSED [ 92%]
tests/test_pawpal.py::test_next_occurrence_weekly_adds_seven_days PASSED [100%]

============================== 14 passed in 0.02s ===============================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — the core sorting, filtering, priority-planning, recurrence, and exact-time conflict logic is well covered and passing. The main known gap is that conflict detection only catches exact `HH:MM` matches, not overlapping durations (see `reflection.md`, section 2b), so a fifth star would need interval-overlap tests once that logic exists.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically by their `HH:MM` `time` field. |
| Priority-based planning | `Scheduler.build_plan()` | Sorts by priority then duration and greedily fits tasks into a time budget, skipping lower-priority tasks once time runs out. Ignores already-`completed` tasks. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status (either or both, independently optional). |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same `time` and returns human-readable warning strings instead of raising — see reflection.md 2b for the exact-match-vs-overlap tradeoff. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.mark_task_complete()` | Completing a `daily`/`weekly` task auto-creates the next occurrence, due `today + 1 day` or `today + 1 week`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
