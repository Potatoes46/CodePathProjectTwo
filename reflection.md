# PawPal+ Project Reflection

## 1. System Design

The user should be able to generate a schedule, add tasks, and add pets and their owners as associated value types.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design includes the four classes of "task", "pet", "owner", and "scheduler". Task is just a single care activity like a walk or feeding and holds info like duration, priority, and preferred time. Pet stores a specific animal's profile and its list of tasks and can sort them by priority when needed. Owner holds the human's info and most importantly how much time they have available in the day. Scheduler is the main class that takes an Owner and Pet and figures out which tasks fit in the available time and explains the resulting plan. The relationships are pretty straightforward where Owner has one or more Pets, Pet has zero or more Tasks, and Scheduler reads from both Owner and Pet to build the schedule without either of them knowing it exists.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler currently considers three main constraints which are time availability, priority, and preferred time of day. Time is the hardest constraint since tasks simply cannot be scheduled if they exceed the owner's available minutes for the day. Priority acts as the tiebreaker for ordering, with high priority tasks always getting picked first. Preferred time is the softest constraint and is more of a labeling preference than something that strictly blocks scheduling. Priority ended up mattering most because in a pet care context missing a high priority task like feeding is a bigger deal than missing a low priority one like grooming, so it made sense to let that drive the selection order.



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The Scheduler class does a solid job of keeping all the scheduling logic in one place, which makes it easy to find and change without touching Pet or Owner. That said, there are some real tradeoffs worth noting. The greedy approach in build_schedule() is simple and fast but it can produce a suboptimal schedule since it just picks tasks in priority order without ever backtracking to see if a different combination would actually fit more work into the time window. The conflict detection in detect_conflicts() also runs in O(n²) time since it compares every pair of tasks, which is totally fine for a pet care app with a handful of tasks but would slow down noticeably if the task list ever got large. Another tradeoff is that Scheduler is built around a single pet at a time, so doing cross-pet conflict detection requires manually passing in the other pet's tasks as an argument rather than the scheduler just knowing about all pets from the start. Overall the design prioritizes simplicity and readability over raw power, which is probably the right call for a project at this scale.

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
