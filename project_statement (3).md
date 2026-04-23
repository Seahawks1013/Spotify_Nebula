# CPTR 242 — Semester Project: *Algorithms Through Worlds*
### Data Structures & Algorithms via Large-Scale Applications

**Proposal Due:** Monday, April 20 by 1:00 PM  
**Project Days:** Every Thursday (in-class check-in + development time)  
**Team Size:** 1–2 students (groups of 3 with instructor permission)  
**Language:** Any (Python, C++, C#/Unity, JavaScript — see Tech Stack below)

---

## Overview

Over the next six weeks, you will design and build an **interactive, performance-focused application**
rooted in a game, simulation, or generative art context. Your project must demonstrate mastery of at
least one core data structure — implemented from scratch or meaningfully extended — and must be capable
of efficiently managing **at least one million elements** under CRUD (Create, Read, Update, Delete)
operations.

The emphasis is on the *backend*: how data is stored, accessed, and mutated. Visualization is required,
but it exists to *illuminate* your data structures — not to be the product itself.

---

## Project Themes (Choose One)

Each theme is a launchpad. You may adapt freely within the spirit of the theme.

| # | Theme | Core DS / Algorithm |
|---|-------|-------------------|
| 1 | **Generative Galaxy** — spiral/elliptical galaxy generator | Arrays, vectors, memory layout (AoS vs SoA) |
| 2 | **Particle Systems Engine** — fire, smoke, sparks | Dynamic arrays vs linked lists, amortized analysis |
| 3 | **Spatial Partitioning** — asteroid/star field with collision | Quadtrees, spatial hashing, uniform grids |
| 4 | **Boids / Flocking Simulation** — birds, fish, drones | Neighbor search, spatial grid optimization |
| 5 | **Pathfinding in a Game World** — 2D grid with agents | Graphs, BFS/DFS, Dijkstra, A\* |
| 6 | **Procedural Terrain Generation** — Perlin/simplex noise | Recursion, divide & conquer, memoization |
| 7 | **Game Object Management** — OOP → ECS refactor | Data-oriented design, cache efficiency |
| 8 | **Physics Engine Lite** — 2D sandbox, many objects | Sweep and prune, BVH, collision detection |
| 9 | **Multiplayer / Networking Simulation** — lag + reconciliation | Event queues, state sync |
| 10 | **Game AI & Decision Trees** — strategy game AI | Trees, minimax, heuristics |
| ★ | **Capstone: Living Galaxy Simulator** — combines all concepts | System design, profiling, DS tradeoffs |

The Capstone theme (★) is recommended only for ambitious groups of 2–3 with a clear scope plan.

---

## Requirements

### 1. Core Data Structure Implementation
- Implement (or meaningfully extend) at least one of: **hash table, BST, heap, or graph**
- Your structure must support all four CRUD operations
- Must handle at least **~1,000,000 elements** without unacceptable performance degradation
- You may use open-source libraries as scaffolding (see Resources), but the DS logic must be
  yours or clearly understood and explained

### 2. Space & Time Complexity Analysis
For each of the four CRUD operations (**Create, Read, Update, Delete**), your written analysis must:
- State the **Big-O notation** for both time and space
- **Explain in plain English** why the complexity is what it is — trace through the logic of your
  specific implementation, not just the textbook definition
- Describe the **best, average, and worst cases** where they differ
- Include a **benchmark table** with measured wall-clock times at 10K, 100K, and 1M elements
- Discuss how your complexity compares to the naive approach and **why the tradeoff is worth it**
  (or isn't, in some cases)

A complexity analysis that only states notation without explanation will not receive full credit.

### 3. Visualization
Your visualization must make the data structure or algorithm *visible* — not just pretty. Examples:
- Draw spatial partitions live (quadtree cells, grid buckets)
- Animate pathfinding expanding across a grid
- Plot frame time vs. particle count as particles grow
- Show cache-miss rates before/after ECS refactor

Visualization tools by stack:

| Stack | Recommended Tools |
|-------|------------------|
| Python | [Pygame](https://www.pygame.org/), [matplotlib](https://matplotlib.org/), [NumPy](https://numpy.org/) |
| C++ | [SFML](https://www.sfml-dev.org/), [SDL2](https://www.libsdl.org/), [raylib](https://www.raylib.com/) |
| C#/Unity | Unity ECS ([Entities package](https://docs.unity3d.com/Packages/com.unity.entities@latest/)) |
| JavaScript | [p5.js](https://p5js.org/), [D3.js](https://d3js.org/), [three.js](https://threejs.org/) |

### 4. Final Reflection Write-Up
A short document (1–2 pages) submitted with your final code addressing:
- What data structure(s) did you use and why?
- What tradeoffs did you encounter?
- What surprised you about performance at scale?
- When does your optimization matter — and when doesn't it?

---

## Weekly Journal & Code Check-Ins

Every Thursday at the start of project day, you will submit a **weekly journal entry** and push a
**tagged commit** to your project repository. Both are required — a commit without a journal entry
(or vice versa) is incomplete.

### Journal Entry Format

Each entry should be **300–500 words** and follow this structure:

---

**Week N Journal — [Team Name / Names]**

**1. What I/we built this week**
Describe what you worked on concretely. What does the code do now that it didn't last week?

**2. Code highlight**
Paste or link to one meaningful function, method, or block from this week's commit.
Explain in 2–3 sentences what it does and why you made the design choices you did.

**3. Complexity checkpoint**
What is the current Big-O behavior of your core operation(s)?
Has it changed from last week? Why or why not?

**4. What broke / what was hard**
Be honest. What didn't work? What took longer than expected? What are you still unsure about?

**5. Plan for next week**
What is the one concrete thing you must have working by next Thursday?

---

### Git Commit Requirements

- Your repository must be on **GitHub** (or another Git host approved in your proposal)
- By Thursday at the start of class, push a commit tagged `week-N` (e.g., `week-1`, `week-2`)
- The commit must reflect **genuine progress** — not just a README update
- Tag your commit from the terminal:
```bash
  git tag week-N
  git push origin week-N
```
- For teams: both members must have **at least one commit** in the week's history.
  Uneven commit histories will prompt a conversation about contribution.

### Submission
Submit your journal entry as a markdown file (`journal/week-N.md`) committed to your repo,
or as a D2L text submission — whichever your instructor specifies.

You are expected to spend at least 5 hours a week (1 hour a day) working on the project.

---

## Proposal (Due Monday, April 20 by 1:00 PM)

Submit a **single document** (PDF or markdown) containing:

1. **Team members** (names + whether you need 3-person permission)
2. **Chosen theme** and a 2–3 sentence description of your specific application idea
3. **Core data structure(s)** you plan to implement
4. **Language and tech stack**
5. **GitHub repo link** (placeholder repo with a README is fine)
6. **Rough weekly plan** — what do you expect to have working by each Thursday?
7. **Stretch goal(s)** — what would a great version look like beyond the minimum?

Proposals that are vague or unrealistically scoped will be returned for revision before approval.

---

## Weekly Project Days (Thursdays)

Each Thursday is dedicated project time. Arrive with:
- Your `week-N` commit already pushed and journal entry submitted
- Something running (even if broken) to show or discuss
- A specific question or blocker if you're stuck

| Week | Rough Milestone Target |
|------|----------------------|
| 1 (Apr 20) | Proposal approved; repo set up; basic data load or scaffold running |
| 2 (May 1) | Core CRUD operations functional; naive version benchmarked |
| 3 (May 8) | Optimized structure in place; 1M element test passing |
| 4 (May 15) | Visualization integrated and meaningful |
| 5 (May 22) | Complexity analysis written; benchmarks collected |
| 6 (May 29) | Polish, reflection write-up, final demo prep |

*Dates are approximate — confirm against the course calendar.*

---

## Final Presentation

At the end of Week 6, each team will give a **10-minute live demo + explanation** (+ 3 min Q&A).
Your presentation must include:

1. **Demo** — show your application running at scale (aim for 1M elements live if feasible)
2. **Data structure walkthrough** — explain your implementation at the code level
3. **Complexity explanation** — walk through the Big-O for each CRUD operation *in your own words*
4. **Benchmark results** — show your timing/memory allocation table and what it tells you
5. **What you'd do differently** — one honest reflection on a design decision

All team members must speak. You will be asked follow-up questions on your complexity analysis.

---

## Grading Rubric

Total: **100 points**

---

### 1. Proposal — 10 points

| Score | Criteria |
|-------|----------|
| 9–10 | Theme, DS choice, stack, timeline, and stretch goals are all clearly defined. Scope is realistic and shows genuine planning. Repo link included. |
| 7–8 | Most elements present; one area is vague or underdeveloped (e.g., timeline is hand-wavy, DS choice is unclear). |
| 5–6 | Proposal is present but significantly incomplete or the scope is unrealistic without revision. |
| 0–4 | Missing, submitted late, or lacks enough detail to evaluate. |

---

### 2. Complexity Analysis (CRUD) — 35 points
*This is the intellectual core of the project. Each of the four operations is worth up to 8 points,
with 3 bonus points for exceptional benchmark discussion.*

**Per operation (Create / Read / Update / Delete) — 8 points each:**

| Score | Criteria |
|-------|----------|
| 7–8 | Big-O stated correctly. Plain-English explanation traces through the actual implementation logic (not just a textbook definition). Best/average/worst cases addressed where relevant. Matches the observed benchmark data. |
| 5–6 | Big-O is correct but explanation is shallow or generic. Cases partially addressed. Minor disconnect between analysis and benchmarks. |
| 3–4 | Big-O stated but explanation is missing or incorrect. No case analysis. Benchmarks not connected to the analysis. |
| 0–2 | Notation only, no explanation. Or analysis is substantially wrong. |

**Benchmark discussion — 3 points:**

| Score | Criteria |
|-------|----------|
| 3 | Benchmark table present for all four operations at 10K/100K/1M. Results are interpreted: student explains *what the numbers mean* and whether they match theoretical expectations. |
| 2 | Table present but interpretation is thin or only covers some operations. |
| 1 | Table present, no interpretation. |
| 0 | No benchmark data. |

---

### 3. Weekly Journals & Commit History — 25 points
*6 journal entries × ~4 points each, with small deductions for missing commits.*

**Per journal entry — 4 points:**

| Score | Criteria |
|-------|----------|
| 4 | All five prompts answered with genuine specificity. Code highlight is meaningful (not trivial). Complexity checkpoint shows active thinking. `week-N` tag pushed with real progress. Both members have commits (if team). |
| 3 | Most prompts answered well; one section is thin or generic. Commit present but modest. |
| 2 | Entry is surface-level throughout, or a significant section is missing. Commit present. |
| 1 | Entry submitted but very incomplete. Commit missing or trivial (e.g., only README). |
| 0 | Not submitted. |

> **Note:** AI tool usage must be disclosed in the journal entry for the week it was used.
> Undisclosed AI use discovered later will result in a zero for that entry.

---

### 4. Final Presentation — 30 points

| Category | Points | 全 (Full) | Partial | Minimal/Missing |
|----------|--------|-----------|---------|-----------------|
| **Live demo** — app runs at scale, CRUD operations visible | 8 | App runs cleanly at or near 1M elements. All four CRUD ops demonstrated. | App runs but at reduced scale, or one operation not shown. | Crashes, not shown, or trivially small dataset. |
| **DS walkthrough** — code-level explanation | 6 | Walks through actual implementation code. Design choices explained clearly. | Explains at a high level without code. | Vague or skipped. |
| **Complexity explanation** — verbal Big-O for all 4 ops | 10 | All four operations explained in own words with correct reasoning. Handles follow-up questions confidently. | 2–3 operations explained well; one weak or skipped. Partial follow-up answers. | One or fewer explained correctly. Unable to answer follow-ups. |
| **Benchmark results** — shown and interpreted | 4 | Table shown. Student explains what the numbers mean and whether results matched expectations. | Table shown, minimal interpretation. | Not shown or no interpretation. |
| **Reflection** — honest design retrospective | 2 | Specific, genuine reflection on one real design decision or mistake. | Generic ("we would plan better"). | Missing. |

> All team members must speak during the presentation. Unequal participation will be noted
> and may affect individual scores at the instructor's discretion.

---

### Summary

| Component | Points |
|-----------|--------|
| Proposal | 10 |
| Complexity Analysis (CRUD × 4 + benchmarks) | 35 |
| Weekly Journals + Commit History | 25 |
| Final Presentation | 30 |
| **Total** | **100** |

---

## Helpful Open-Source Resources

**Data Structures & Algorithms**
- [abseil-cpp](https://github.com/abseil/abseil-cpp) — Google's C++ DS library (hash maps, btree)
- [PBDS (Policy-Based DS)](https://gcc.gnu.org/onlinedocs/libstdc++/ext/pb_ds/) — GCC's augmented BSTs and hash tables
- [networkx](https://networkx.org/) — Python graph library for prototyping graph algorithms
- [boost::graph](https://www.boost.org/doc/libs/release/libs/graph/) — C++ graph library

**Spatial Structures**
- [libqtree](https://github.com/alexbol99/quadtree) — JavaScript quadtree
- [nanoflann](https://github.com/jlblancoc/nanoflann) — C++ fast KD-tree for nearest neighbor search
- [py-trees](https://github.com/splintered-reality/py_trees) — Python behavior tree library

**Benchmarking & Profiling**
- [Google Benchmark](https://github.com/google/benchmark) — C++ microbenchmarking
- [Valgrind/Callgrind](https://valgrind.org/) — C++ profiling and cache analysis
- [memory_profiler](https://github.com/pythonprofilers/memory_profiler) — Python memory profiling
- [timeit](https://docs.python.org/3/library/timeit.html) — Python built-in benchmarking

**Procedural Generation / Noise**
- [libnoise](https://libnoise.sourceforge.net/) — C++ coherent noise (Perlin, etc.)
- [noise](https://github.com/caseman/noise) — Python Perlin/simplex noise

**Physics / Simulation**
- [Box2D](https://box2d.org/) — 2D physics engine (C++, many ports)
- [pymunk](http://www.pymunk.org/) — Python wrapper for Chipmunk2D physics

---

## Academic Integrity

- Code must be your own. Using open-source libraries as *dependencies* is fine and encouraged;
  submitting library internals as your own implementation is not.
- AI tool usage must be disclosed in your **weekly journal** for the week it was used.
- All team members are expected to understand and be able to explain every part of the submission.

---

*Questions? Bring them to Thursday project day or email me.*