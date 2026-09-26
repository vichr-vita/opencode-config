---
name: write-the-docs
description: Writes, edits, and reviews software documentation using the Write the Docs guide. Use for READMEs, tutorials, how-to guides, reference and API docs, release notes, troubleshooting, documentation maintenance, or new docs sites.
---

# Write the docs

Use the [Write the Docs guide](https://www.writethedocs.org/guide/) as the
authority for documentation practice. Treat the product's implementation and
verified behavior as the authority for product facts. Follow local terminology
and formatting conventions without sacrificing accuracy or reader needs.

## Understand the reader and the task

Identify who is reading, what they already know, and what they need to
accomplish. Distinguish using the product from contributing to it. Inspect the
relevant code, existing docs, and available user questions before drafting.
Investigate gaps instead of filling them with plausible claims.

Choose a page purpose and a clear boundary. For a tutorial, establish the
starting conditions and a result the reader can recognize. For a reference,
define which interface and version it covers. Scale the work to the request;
a small correction does not require restructuring the documentation set.

## Structure and write

- Cover the promised scope; disclose omissions. Across the documentation set,
  prioritize likely reader questions over obscure cases.
- Open a page with a short explanation of what the reader can do or learn. Give
  context before a procedure or list when the heading alone is not enough.
- Put prerequisite concepts before dependent steps. Separate learning examples
  from dense lookup material. Use headings and descriptive links to help readers
  find an answer without reading everything.
- Explain concepts even when code also expresses them. Maintain one canonical
  source for each fact; link or reuse it instead of creating competing copies.
- Write concrete instructions in plain language. Address the reader as "you"
  in task guidance, use active voice and present tense, and match the project's
  language conventions. Use the same names as the product and explain unfamiliar
  terms when the audience needs them. State requirements and recommendations
  distinctly.
- Number sequential steps, start each with an action, and place conditions
  before instructions. Mark optional steps. Use code formatting for commands,
  paths, and API names, and bold for named interface controls.
- Include a small, representative example. Keep basic installation short and
  link to advanced setup. Do not invent commands, outputs, defaults, or URLs.
- Make content readable with assistive technology. Use meaningful document
  structure and text alternatives for information conveyed visually. Check
  language and example names for unnecessary assumptions about readers.

For README coverage, release notes, API docs, FAQs, or error messages, read the
matching section of [writing notes](references/writing-notes.md). That file
also records the source rationale and the limits of the guide's advice.

## Default docs site stack

For a new documentation site without an established stack, use Astro for the
static site, MDX for authored pages and embedded components, and Algolia
DocSearch for search. Preserve an existing project's stack unless the user asks
to change it. Keep essential information in rendered content, even when a page
has interactive components.

Provide navigation that works before Algolia is configured. Use only a public
search-only key in browser settings; never expose an admin or write key. An
Astro build does not verify the external index, crawler, or live search results.

## Verify and maintain

Compare claims with implementation evidence. Walk through instructions from
the stated starting conditions. Run relevant existing documentation checks and
verify examples in a safe test environment. Inspect rendered output when markup
or presentation changes. Report what remains unverified.

Check affected links and anchors. When changing a heading, find inbound links
to its anchor and update them. Make the page reachable from likely entry points
and link directly to useful sections. Use relative links where the project's
publishing system expects them. Check available package scripts before running
a formatter. Keep docs close to code, update them with behavior changes, and
preserve needed version distinctions. Invite feedback through the project's
existing channels.

For documentation workflows, tooling, publishing, search, or API test strategy,
read [operations notes](references/operations-notes.md). Do not turn the guide's
tool examples into mandatory dependencies.

## Review an existing document

Review for reader blockers before polishing sentences. Identify unsupported
claims, missing prerequisites, incomplete procedures, and misplaced answers.
For each material finding, give its location, explain the reader's difficulty,
and propose a concrete correction. A review request produces findings unless
the user also asks for edits.

For example, replace a finding such as "improve onboarding" with "The setup
page uses `SERVICE_URL` without explaining where to obtain it. Add that step
before the first request." This is an illustrative review pattern, not a claim
about a particular product.
