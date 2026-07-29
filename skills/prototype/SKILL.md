---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, from the user's prompt, surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** -> [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** -> [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module -> logic; a page or component -> UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate prototype code close to where it will actually be used, but name it so a casual reader can see it is a prototype, not production. For throwaway UI routes, obey the project's routing convention.
2. **One command to run.** Use whatever the project's existing task runner supports: `pnpm <name>`, `python <path>`, `bun <path>`, or equivalent.
3. **No persistence by default.** State lives in memory. If the question explicitly involves a database, use a scratch database or local file with a clear `PROTOTYPE - wipe me` name.
4. **Skip polish.** No tests, no error handling beyond what makes the prototype runnable, no abstractions. Learn fast.
5. **Surface state.** After every action (logic) or variant switch (UI), print or render full relevant state.
6. **Capture it when done.** Record the validated decision in the active OpenSpec change or spec. Fold that decision into real code, then preserve the prototype as runnable evidence on a throwaway `prototype/<name>` branch that is never merged. Add the branch reference and verdict to the OpenSpec artifact. Main keeps only the validated decision.
