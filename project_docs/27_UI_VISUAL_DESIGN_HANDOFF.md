# 27. UI Visual Design Handoff — Strict Reference Implementation Contract

## 27.1 Locked identity and palette
Use this exact theme on every page and state:
- Deep Emerald `#142923`: sidebar, hero/banner, primary dark surfaces
- Champagne Gold `#C6A76A`: primary CTAs, selected states, highlights, key icons
- Warm Ivory `#F5F2EA`: page canvas and light surfaces
- Supporting card surface: `#FFFCF5` or sampled equivalent from reference
- Main text: `#17231E`; muted text: `#66716A`
- Risk semantics: restrained red/amber/green, paired with labels/icons

Do not substitute blue/white, purple, or another brand palette. Keep all six pages consistent with the images.

## 27.2 Absolute visual source-of-truth rule
The supplied PNGs are the **actual UI specification**. Reproduce the screen shown in each image—not a similar interpretation. Required fidelity includes:
- same page composition, section order, and information hierarchy
- same sidebar and active item, header, page title/subtitle, and branding
- same card/panel count, placement, relative size, grid, and spacing
- same visible labels, button text, icons, chart types, and table columns
- same tabs, selected states, badges, and content grouping
- same visual palette, typography hierarchy, borders, radii, and shadows
- same page-to-page flow and location of controls

Do not remove sections, relocate visible elements, rename labels, invent extra panels, or change the theme because an alternate design seems better. If the reference includes a control, implement its action. If its backend behavior is not yet available, show a visibly disabled/coming-soon state without changing its placement.

**Exactness process:** inspect source → build page → capture at 1600×900 → compare side-by-side and overlay/diff → adjust → repeat. Keep reference PNGs unchanged. Never use the screenshot as a background in place of a functioning UI. Codex must not claim exact visual fidelity without recorded comparison.

## 27.3 Strict no-page-scroll requirement
At **1600×900**, each primary page and the investigation workspace must fit within one viewport with **no page-level vertical or horizontal scrolling**. This is a hard acceptance gate.
- All visible page sections, navigation, controls, and primary actions must fit.
- Do not hide scrollbars, clip content, cover overflow, or remove required elements to pass.
- Use compact layout, fixed viewport-aware sizing, columns, tabs, and progressive disclosure while preserving reference composition.
- Bounded internal panels may scroll only where the reference implies a list/detail region; the overall page must remain fixed.
- Capture evidence that document/page scroll dimensions do not exceed viewport dimensions at 1600×900.
- At smaller widths, responsive reflow is required; document the minimum supported viewport and test it. Do not claim the no-scroll gate passed outside tested dimensions.

## 27.4 Navigation contract
Primary sidebar, exact order:
1. Dashboard
2. New Investigation
3. Case History
4. Analytics
5. Settings
6. About Project

Case-specific tabs appear only after selecting a case from Case History: Scam Timeline, Evidence & Agent Analysis, Evidence Graph, Scam Tracker / Journey Tracker, Final Assessment, Report & Actions. Keep Case History active in the primary sidebar while inside the case workspace.

## 27.5 Interactions and motion
- Functional buttons, tabs, filters, case rows, upload controls, and navigation.
- Restrained transitions around 120–220 ms where technically supported; avoid animations that alter layout or delay actions.
- Hover, focus, pressed, disabled, and loading states.
- Respect reduced-motion preferences; provide no-motion behavior.
- Loading/progress must reflect actual work, never fake agent activity or completion.
- Confirm destructive actions.

## 27.6 Data honesty while matching reference
For deterministic demo mode, seed synthetic records that match the sample labels/layout shown in the images and visibly identify them as demo data. In normal use, compute metrics from persisted cases/evaluation data. If no data exists, preserve the reference layout but show honest zero/empty-state values. Do not hardcode example percentages as real analytics.

## 27.7 UI verification checklist
- [ ] All six approved reference PNGs present, opened, and mapped correctly.
- [ ] Palette tokens exactly match approved hex values.
- [ ] Each page layout compared at 1600×900 with side-by-side and overlay/diff.
- [ ] All visible labels and sections retained.
- [ ] Main and nested navigation states correct.
- [ ] No page-level scroll and no clipped content at 1600×900.
- [ ] Every visible control has a real action or honest disabled state.
- [ ] Animations and reduced-motion behavior verified.
- [ ] Narrow viewport reflow checked.
- [ ] Demo metrics are labeled synthetic; live metrics are data-derived.
- [ ] Comparison screenshots and results recorded in verification report.
