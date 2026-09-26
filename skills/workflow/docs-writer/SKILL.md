---
name: docs-writer
description: Write, edit, or review Vitfin documentation for accuracy and clear prose. Use for files in Vitfin's docs directory and any Markdown file in the Vitfin repository, including MDX examples.
---

# Docs writer

Write documentation that matches the current Vitfin code and its existing
terms. Apply the repository's `AGENTS.md` and `unslop` guidance. When editing
the Astro site or its publishing setup, use `vitfin-docs-site` as well.

## Prepare

Before changing content, read the relevant implementation, the current page,
and nearby pages. Check `CONTEXT.md` for domain terms. For published pages,
read `docs/site-guide.md` and `docs/catalog.json` to understand publication
and navigation. Search for pages that reference the behavior or heading being
changed. Ask for clarification
only if the intended change cannot be inferred from the request and code.

## Write

- Start with a short introduction that tells readers what the page covers.
  Follow each heading with an overview paragraph before a list or subheading.
- Address the reader as "you". Use active voice, present tense, standard US
  English, simple words, and a professional, direct tone. Use contractions.
- Distinguish requirements with "must" and recommendations with "we
  recommend". Avoid "should", "please", idioms, hype, and anthropomorphism.
- Use sentence case for headings and bold labels. Refer to the project as
  `Vitfin`. Use precise verbs and keep sentences short.
- Spell out "for example" and "that is" instead of Latin abbreviations.
  Use the serial comma. Write dates unambiguously.
- Wrap prose at 80 characters unless a link or table makes that impractical.
  Use numbered lists for ordered steps and bullets for other lists. Introduce
  procedures with a sentence, start steps with verbs, and state conditions
  before instructions. Mark optional steps explicitly.
- Use bold for UI controls and code font for commands, paths, API names, and
  snippets. Give images descriptive alt text and lowercase hyphenated names.
  Use semantic headings, lists, tables, and details. Avoid manual tables of
  contents. End with "Next steps" only when there is a useful action to take.
- Use "quota" for an administrative allocation and "limit" for a numerical
  ceiling. Check the product's actual terminology before describing either.

Use a GitHub-flavored Markdown alert only when the information needs special
attention. Put a blank line and `<!-- prettier-ignore -->` before an alert in
`.md`, or `{/* prettier-ignore */}` in `.mdx`. Put `[!NOTE]`, `[!TIP]`,
`[!IMPORTANT]`, `[!WARNING]`, or `[!CAUTION]` on the first quoted line, and
start each following line with `>`.

Keep documentation links relative to the current file and check their
targets. The site's link transform preserves published routes and links to
unpublished repository sources. Use descriptive link text. If a heading
changes, find and update inbound anchor links.

For a feature explicitly marked experimental, add a note after its
introduction using the alert format above:

> This is an experimental feature currently under active development.

## Verify

Re-read the changed text for accuracy, flow, terminology, and formatting.
Check new and affected links and anchors. For published pages, run
`pnpm --dir docs build` when the local dependencies are available; it checks
Astro output and local links. Check the package scripts before running a
formatter, and use one only if the repository provides it.
