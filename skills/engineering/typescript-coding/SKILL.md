---
name: typescript-coding
description: Use when the topic is TypeScript, including coding, testing, or interacting with TypeScript code in any way.
---

# TypeScript coding preferences

- `any` is the enemy. Inferred types are our friend. Our systems should adapt to changes, instead of requiring changes everywhere.
- If your TS code looks like a Python dev wrote it, it is bad TS code.
- Avoid one-line functions that are just casting wrappers.
- Write TypeScript in ways that Matt Pocock and Theo would be proud of.
- If not already specified in project, I generally like to use the following tech: Convex, Tailwind, React, Vite, pnpm
- When building more complex web and React Native apps, I like to pull in Zustand, React Query, TanStack Start, Clerk (or better-auth if self-hosting), and ArkType (or Zod if performance isn't an issue).
