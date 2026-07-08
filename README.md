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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
