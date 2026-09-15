# Writing

Use natural, clear prose with complete sentences.
Apply the `unslop` skill to human-facing writing.

# Coding preferences - general

- Keep things simple. Channel "yagni" energy unless told otherwise.
- Typesafety is useful, take advantage of it.
- Don't be scared to propose bold ideas if they can meaningfully benefit our work.
- Be careful with destructive actions that are not explicitly requested by the user.
- Tests are good! Endless smoke tests, "regression tests" for feature deletions, etc, much less good. Tests should be focused, not slop.
- Comments are a great way to clarify functionality and how code is used. Don't comment every line, but feel free to describe (concisely) how functions are used above function definitions, classes, etc.
- Keep comments up to date! When making changes, it's important to keep things in sync.

# Questions are read-only

- A question is a request for an answer, not for changes. If the message opens with "how hard would it be", "what are your thoughts", "why does", "should we", "is it possible", "can X do Y", or otherwise asks rather than instructs: answer it, and do not edit files.
- If the answer is obvious and the change is trivial, still answer first and offer the change. Ask before making it.

# Match ceremony to the task

- Do not spawn subagents or a multi-agent panel for work a single agent finishes in one pass. Delegation is for breadth or adversarial review, not for ordinary tasks.
- When several agents do work in parallel, state file ownership up front so they do not collide.

# Visual and design work

- Do not edit real components first. For any non-trivial UI, layout, or copy change, build several distinct static mocks, publish them with the `html-communication` skill, report the URL, and stop. Wait for a pick before implementing.
- Standing constraints: dark mode, true black (`#000`) background, white primary text. Information-dense, no decorative card/pill chrome, no light-gray subtitle lines above sections. Minimal copy. No em dashes.
- Avoid continuously repainting CSS animations (pulse, shimmer, blur, spinners); they peg the GPU on high-refresh displays.

# Blast radius

- Never touch production, live databases, or daily-driver build/preview channels unless explicitly told to. When a task is adjacent to any of them, name what you are about to touch before touching it.

# Pull Requests

- Make sure titles follow conventions from the repo. They should be simple and easy to understand. Conventional commit styles in projects that use them, i.e. "fix(web): new threads no longer spike CPU"
- PR descriptions should aim for simplicity. Open with a minimal, clear description of the problem. Follow up with how you solved it.
- Add a blurb to the end of the PR description about what model and harness is making the changes. Use the signature format: `<model> in behalf of <first name of author from gh> via <harness>`
- Open a real PR, not a draft. Drafts do not get review-bot coverage.
- Rebase onto latest `main` before opening. Stale branches conflict and waste a review round.
