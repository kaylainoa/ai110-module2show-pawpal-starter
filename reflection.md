# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

A pet owner using PawPal+ should be able to:

1. **Add a pet (and owner profile).** The owner enters their own info once, then adds one or more pets with basic details (name, species, breed) so the app knows who it's planning care for.
2. **Add and manage care tasks for a pet.** For each pet, the owner adds recurring or one-off care tasks — walks, feeding, meds, enrichment, grooming — specifying at minimum how long the task takes and how important it is (priority).
3. **Generate and view today's plan.** The owner asks PawPal+ to build a schedule for the day. The app selects and orders tasks based on priority and available time, shows the resulting plan with times, and explains why each task was included/ordered the way it was.

**a. Initial design**

My initial UML has four classes:

- **Owner** — holds the pet owner's name, their list of `Pet`s, and free-form scheduling preferences. Responsible for owning/managing pets (`add_pet`, `get_pet`); it doesn't know anything about tasks or scheduling directly.
- **Pet** — holds basic identity info (name, species, breed) and its own list of `Task`s. Responsible for managing which tasks belong to it (`add_task`, `remove_task`).
- **Task** — the smallest unit of work: title, duration, priority, category, whether it recurs, and whether it's done. Responsible only for its own state (`mark_complete`); it has no knowledge of the pet or owner it belongs to.
- **Scheduler** — takes a `Pet` and an available time budget, and is responsible for turning that pet's task list into an ordered daily plan (`build_plan`) plus a human-readable explanation of the choices (`explain_plan`). It's kept separate from `Pet`/`Task` so the "planning" logic doesn't leak into simple data-holder classes.

The relationships are Owner 1→many Pet, Pet 1→many Task, and Scheduler reads from Pet/Task without owning them (dependency, not composition).

**b. Design changes**

After writing the skeleton, I reviewed `pawpal_system.py` for missing relationships and logic bottlenecks and made two changes:

1. **Removed the duplicated `available_minutes`.** `Scheduler` originally took `available_minutes` in `__init__` *and* again as a `build_plan` argument — two sources of truth with no clear rule for which wins. I made `Scheduler` stateless and pass `available_minutes` only as a `build_plan` argument.
2. **Generalized `build_plan` to accept a task list instead of a single `Pet`.** Since I'd already decided an `Owner` can have multiple pets, a `Scheduler` that only accepted one `Pet` had no way to build a combined daily plan across an owner's pets. I changed the signature to `build_plan(tasks: list[Task], available_minutes: int)` and added `Owner.all_tasks()` to gather tasks across all pets, so the same method works for a single pet's plan or a combined household plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only flags tasks that share the *exact same* `time` string (e.g. two tasks both at `"08:00"`). It does not check whether one task's duration overlaps into another task's start time — e.g. a 30-minute "Morning walk" at `08:00` and a 10-minute "Feeding" at `08:15` would not be flagged, even though the walk is still running when the feeding is supposed to start.

I chose this on purpose: exact-match comparison is a simple string/dict lookup (`O(n)`, no interval math), while true overlap detection needs sorting tasks by start time and comparing each task's `[start, start + duration]` window against its neighbors — more code and more edge cases (back-to-back tasks, zero-duration tasks, etc.) for a starter app. Exact-match conflicts are also the more common real mistake a pet owner would make (accidentally double-booking the same time slot), so catching that case covers most of the practical value. It's a reasonable v1 tradeoff, but a known gap: it would miss a genuinely overlapping schedule that doesn't start at the same minute.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
