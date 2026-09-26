# Research notes on workflow, tooling, and publication

Read on 2026-09-26. Each entry records a complete reading of the linked guide page. These notes distinguish advice from introductions and resource directories. External manuals, talks, products, and examples linked by those pages were not reviewed. Tool examples describe the guide's coverage, not a requirement to adopt or install them.

## Work within the project's documentation workflow

### Docs as Code

[Source](https://www.writethedocs.org/guide/docs-as-code/). Substantive advice followed by books and talks.

Use issue tracking, version control, plain-text sources, review, and automated checks to give documentation the same development workflow as code. Writers and developers should share responsibility for it. Request documentation while feature knowledge is fresh; a project can require it before merging features. This is an approach to collaboration, not a reason to replace an established authoring system.

### DocOps

[Source](https://www.writethedocs.org/guide/doc-ops/). Substantive overview with resource links.

Plan how documentation is created, maintained, and released across writing, engineering, product, and support. Assign responsibility for priorities, contributor training, content, versioning, build scripts, themes, and tool maintenance. Keep contribution easy. These operational responsibilities apply to wikis and content management systems as well as Docs as Code.

### Choosing tools for documentation

[Source](https://www.writethedocs.org/guide/choosing-tools/). Decision checklist.

Start with existing tools and reader destinations. Assess required outputs, available skills, time and money, review access, contributor count, reuse, version control, automation, translations, and import/export needs. Provide a preview or staging area regardless of editor choice. Budget for customization and reviewer training as well as licenses. Name who will handle upgrades and failures, and plan how to repair links when pages move or disappear. A static site generator has setup and maintenance costs too.

### Tools for documentation writing

[Source](https://www.writethedocs.org/guide/tools/). Mostly a directory of tools and child guides.

The page introduces Sphinx and lists alternative generators, then points to testing guidance. Its examples show that tool choice depends on project needs. Do not read its emphasis on Sphinx as a universal recommendation. Consult the tool's own current documentation when implementation details matter.

### Testing your documentation

[Source](https://www.writethedocs.org/guide/tools/testing/). Substantive checks with tool examples.

Automate documentation builds, link checks, and established style rules. Run useful checks on commits so failures appear before publication. Build success is a useful baseline; stronger warning checks make sense once existing documentation can pass them. Check links through the documentation tool or the rendered site. Prose linting can enforce agreed terminology and style. The named CI providers and configuration commands are examples, not required infrastructure.

## Make published documentation usable and verifiable

### Search engine optimization for documentation

[Source](https://www.writethedocs.org/guide/seo/). Short advice section followed by a resource directory.

Use headings that describe readers' goals and actions. Divide material into sections people can scan. Give the site a clear hierarchy and navigation, preserve accessibility, and include appropriate page metadata. These practices help readers as well as search engines. The page warns that search algorithms change, so do not treat particular ranking tactics as permanent writing rules.

### API documentation tools

[Source](https://www.writethedocs.org/guide/api/api-documentation-tools/). Tool-specific introduction and API Blueprint walkthrough.

An API description can generate reference documentation and support automated comparison with implementation behavior. Organize related endpoints, their HTTP actions, and reusable request/response structures. Show example requests and responses. The page describes API Blueprint, Apiary, and related tools rather than a complete API writing method. Its live-API examples do not establish a safe execution policy. Apply the project's authorization and environment restrictions when verifying examples; use a suitable test environment.

## Preserve the chosen markup and publication system

### Introduction to Markdown

[Source](https://www.writethedocs.org/guide/writing/markdown/). Syntax tutorial.

Markdown offers readable plain-text sources with headings, lists, links, images, and code formatting. Use those structures to make longer documents navigable. Follow the project's renderer and dialect when using extensions. This page is a starting reference for syntax, not a reason to add custom HTML or switch formats. Its prose calls code delimiters apostrophes, but the examples correctly use backticks.

### Introduction to reStructuredText

[Source](https://www.writethedocs.org/guide/writing/reStructuredText/). Syntax tutorial with a rationale.

reStructuredText supports semantic markup, content reuse, output filtering, and extension through directives. Keep paragraph and list indentation consistent. Use a consistent heading adornment for each level and make it at least as long as the heading. Preserve literal formatting for code. Use its stronger structural facilities where the existing documentation system needs them.

### Introduction to XML

[Source](https://www.writethedocs.org/guide/writing/xml/). Introductory explanation and small examples.

XML gives content explicit structure through tags and attributes and stores it as plain text. Its relevant documentation lesson is to distinguish structured source data from its presentation. The guide demonstrates custom elements and styling; it does not prescribe XML for ordinary documentation or provide a full structured-authoring workflow.

### Introduction to AsciiDoc

[Source](https://www.writethedocs.org/guide/writing/asciidoc/). Publishing overview and extensive syntax examples.

AsciiDoc supports several publication formats and provides headings, cross-references, code blocks, tables, admonitions, tables of contents, and includes. Reuse source material with includes when the existing project uses this facility. Keep content in the source format and let the publishing system handle presentation. Read this page as a syntax reference when editing AsciiDoc, not a migration recommendation.

### Introduction to Sphinx

[Source](https://www.writethedocs.org/guide/tools/sphinx/). Tool-specific getting-started instructions.

Fit new material into the existing topic structure. Add a new page to a reachable `toctree` so readers can find it. Split a topic into files when its size warrants it. Build and inspect the generated output. Plain reStructuredText previews may miss Sphinx-specific markup, so use the real project build to verify it. The page also introduces MyST and cross-project references. Follow current project setup instructions rather than copying its system-wide installation command.

### Sphinx themes

[Source](https://www.writethedocs.org/guide/tools/sphinx-themes/). Resource directory with selection criteria.

The directory favors mobile support, readable typography, straightforward installation, maintenance, and documentation. It describes several navigation and layout options. These criteria are more reusable than the theme list. Evaluate the existing theme against actual reader needs before proposing a replacement.

### Community perspectives on Sphinx

[Source](https://www.writethedocs.org/guide/tools/sphinx-community/). Reported experience and learning resources.

Account for the learning cost of reStructuredText, navigation trees, and theme customization. Strong code integration and cross-references do not remove those costs. A comprehensive reference may still leave beginners needing a tutorial. This is useful evidence when choosing tools or preparing contributor instructions, rather than a claim that one tool suits everyone.

## Interpret the guide's scope and editorial standards

### About Write the Docs

[Source](https://www.writethedocs.org/guide/about/). Navigation page only.

This page links the vision, example approaches, and community pages covered below. It adds no separate writing rules.

### Vision

[Source](https://www.writethedocs.org/guide/about/vision/). Statement of purpose.

Documentation should help people use work and learn what they need. Make it easy to begin contributing. Prefer practical guidance that is concise and straightforward to follow. Write with translation in mind so knowledge is accessible across languages.

### Interesting approaches to documentation

[Source](https://www.writethedocs.org/guide/about/alternatives/). Resource directory only.

The page points to comparisons between designs and implementations, conference notes, teaching material, and examples of documentation. These illustrate possible formats; the page does not establish a required writing method. Linked examples were outside this reading's scope.

### Documentation community

[Source](https://www.writethedocs.org/guide/about/community/). Community directory and invitation to contribute.

The page lists places to discuss documentation and contribute to the community. It adds no operational requirement for writing a project's documentation, and following this skill does not require joining a channel or contacting anyone.

### Contributing to the Write the Docs guide

[Source](https://www.writethedocs.org/guide/contributing/). Guide-specific editorial instructions.

Use a friendly, encouraging tone. Attribute links and explain their usefulness. Emphasize general principles and consequential choices; explain why a recommendation matters instead of presenting taste as a rule. Discuss tools through concrete use cases, outcomes, and limitations. Avoid promotion. The page's file-format and submission instructions apply to contributions to Write the Docs itself.
