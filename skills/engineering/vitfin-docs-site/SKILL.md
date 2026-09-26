---
name: vitfin-docs-site
description: Maintain Vitfin's Astro documentation site. Use when changing its MDX examples, publication catalog, navigation, rendering, build, or Algolia DocSearch integration.
---

# Vitfin docs site

Use this skill for site behavior and publishing work in
`/home/vichr/projects/vitfin/docs`. Use `docs-writer` as well when writing or
reviewing Markdown or MDX content.

## Read the local setup

Read `docs/site-guide.md`, `docs/package.json`, `docs/astro.config.mjs`, and
the files affected by the request before editing. Check the current code for
behavior rather than relying on this skill for version numbers. The docs are a
separate static Astro application. MDX supplies worked examples, React powers
interactive examples and DocSearch, and Tailwind and CSS style the site.

## Publish pages

`docs/catalog.json` is the explicit publication list and navigation order.
The content collection loads only its `source` entries, including repository
files outside `docs/`. Add or change a catalog entry when a page's source,
route, title, description, or group changes. Do not assume that adding a file
publishes it. Keep private notes and local records out of the catalog.

Routes and base paths come from the catalog and `DOCS_BASE_PATH`. Keep links
in Markdown and MDX relative to their source files. The `remarkDocs` plugin
maps links to published sources onto site routes and sends unpublished source
links to GitHub. Check links and anchors when moving a file or heading.
The page layout supplies the rendered `h1` from the catalog; published source
headings at level one are removed during rendering.

For a worked example, follow an existing file in `docs/learn/`. `Example.astro`
accepts explanatory content in its default slot and a table, diagram, or
component in its `example` slot. Keep essential facts server rendered. Add a
React island only when interaction helps readers compare outcomes. Mermaid
diagrams render to SVG during the build through Playwright Chromium.

## Maintain search

The header uses Algolia DocSearch only when all three public build settings
are present: `PUBLIC_ALGOLIA_APP_ID`, `PUBLIC_ALGOLIA_INDEX_NAME`, and
`PUBLIC_ALGOLIA_SEARCH_KEY`. Otherwise it links to the page index. The key
must be a public search-only key for the docs index. Do not put an admin or
write key in a `PUBLIC_` setting. Search indexing and crawling are external;
a local build cannot prove that live results work. Read `docs/site-guide.md`
before changing search setup or crawler instructions.

## Verify changes

Use the checks that cover the edited behavior. `pnpm --dir docs build` runs
Astro checks, creates the static site, and validates local links and anchors.
Use `pnpm --dir docs test` for changes to navigation, search, or interactive
examples. The build needs Playwright Chromium for Mermaid rendering. The docs
development server and preview channel are separate from the private app;
follow project instructions before touching any live or daily-driver channel.
