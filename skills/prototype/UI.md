# UI Prototype

Generate **several radically different UI variations** on one route, switchable from a floating bottom bar. The user compares variants, chooses one or combines parts, then discards the rest.

If the question concerns logic or state, use [LOGIC.md](LOGIC.md).

## Choose placement

Strongly prefer mounting variants inside an existing page. Real headers, sidebars, data, auth, and density expose design problems hidden by an isolated route.

### Existing page, preferred

Render variants on the same route, selected by a `?variant=` search parameter. Keep existing data fetching, params, and auth; swap only the rendered subtree. New sections or flow steps that naturally belong in an existing page also use this shape.

### New page, last resort

When no existing page is plausible, create a clearly named throwaway route using project routing conventions, such as `/prototype/<name>`. Use the same `?variant=` pattern.

## Process

### 1. State the question and variant count

Default to three variants; cap at five. Record one line describing what is varied, where it is mounted, and how variants are selected.

### 2. Generate radically different variants

Respect page purpose, available data, and project component/styling system. Give each variant a clear exported component name such as `VariantA`.

Variants must differ structurally: layout, information hierarchy, and primary affordance. Colour or copy changes alone do not count. Redo variants that converge on the same structure.

### 3. Wire variants together

Create one switcher on the route:

```tsx
// Pseudo-code: adapt to the project's framework.
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A', 'B', 'C']} current={variant} />
  </>
);
```

Keep existing data fetching above the switcher. A new prototype route mounts the same switcher.

### 4. Build the floating switcher

Create a fixed bottom-centre bar containing previous arrow, current variant label, and next arrow.

- Update URL search parameter through framework router so selection is shareable and reload-stable.
- Support left and right arrow keys, except while an `input`, `textarea`, or `[contenteditable]` has focus.
- Make bar visually distinct from evaluated design.
- Hide it in production builds.
- Keep switcher in one shared component.

### 5. Hand it over

Surface URL and variant keys. Let user compare and request combinations.

### 6. Capture answer and clean up

Record winning variant, rationale, and settled question in active OpenSpec artifact, following [SKILL.md](SKILL.md). Fold winner into real code. Preserve full variant set and switcher on throwaway prototype branch; remove losing variants and switcher from main.

## Anti-patterns

- **Variants differing only in colour or copy.** Vary structure.
- **Sharing layouts across variants.** Shared primitives are fine; shared layout defeats exploration.
- **Using real mutations.** Prefer read-only data or stubs.
- **Promoting prototype directly.** Rewrite winner with production tests and error handling.
