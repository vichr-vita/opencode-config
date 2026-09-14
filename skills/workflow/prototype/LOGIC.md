# Logic Prototype

A tiny interactive terminal app that lets the user drive a state model by hand. Use this when the question is about **business logic, state transitions, or data shape**.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where the user wants to **press buttons and watch state change**.

If the question is "what should this look like", use [UI.md](UI.md).

## Process

### 1. State the question

Before writing code, record the state model and question in the prototype README or a top-of-file comment.

### 2. Pick the language

Use whatever the host project uses. If the project has no obvious runtime, ask. Match existing tooling; do not add a package manager or runtime for the prototype.

### 3. Isolate logic in a portable module

Put the logic behind a small, pure interface that could be lifted into real code later. The TUI is throwaway; the logic module should be portable.

Choose the shape that fits the question:

- **Pure reducer**: `(state, action) => state` for discrete events and one state value.
- **State machine** for explicit states, transitions, and legal actions.
- **Small pure function set** over a plain data type for stateless transformations.
- **Class or module with a clear method surface** when logic genuinely owns ongoing internal state.

Keep it pure: no I/O, terminal code, or `console.log` control flow. The TUI imports it; nothing flows back.

### 4. Build the smallest TUI that exposes state

On every tick, clear the screen (`console.clear()`, `print("\033[2J\033[H")`, or equivalent) and render the whole frame.

Each frame contains:

1. **Current state**, pretty-printed and diff-friendly. Use bold for field names or headers and dim for secondary context. Native ANSI codes are sufficient.
2. **Keyboard shortcuts** at the bottom, such as `[a] add user  [d] delete user  [t] tick clock  [q] quit`.

Behaviour:

1. Initialise one in-memory state object and render it.
2. Read one keystroke or line, then dispatch to a handler.
3. Re-render the full frame after every action.
4. Loop until quit.

Keep the frame on one screen.

### 5. Make it runnable in one command

Add a script to the project's task runner (`package.json`, `Makefile`, `justfile`, or `pyproject.toml`). If none exists, put the command at the top of the prototype README.

### 6. Hand it over

Give the user the run command. Let them drive it and react. Add actions as needed.

### 7. Capture the answer and prototype

Record the verdict and settled question in the active OpenSpec artifact, following [SKILL.md](SKILL.md). Lift validated logic into real code. Preserve the TUI shell on the throwaway prototype branch.

## Anti-patterns

- **Adding tests.** A prototype that needs tests is no longer a prototype.
- **Using the real database.** Use memory unless persistence is the question.
- **Generalising.** Answer one question.
- **Blurring logic and TUI.** Keep terminal concerns out of portable logic.
- **Shipping the TUI.** Keep only validated logic.
