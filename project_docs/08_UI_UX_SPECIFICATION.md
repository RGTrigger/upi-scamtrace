# 8. UI/UX Specification — Locked Visual and Functional Contract

## 8.1 Product UI Direction (LOCKED)
The UI must use the approved **Deep Emerald + Champagne + Warm Ivory** theme on every page and state.

| Token | Hex | Required use |
|---|---|---|
| Deep Emerald | `#142923` | Main sidebar, primary navigation, hero/banner surfaces, primary dark surfaces |
| Champagne Gold | `#C6A76A` | Primary CTA accents, selected navigation, highlights, key icons, focus/active details |
| Warm Ivory | `#F5F2EA` | Main workspace background and light content surfaces |
| White/ivory card | `#FFFCF5` (or visually sampled equivalent) | Cards and panels |
| Main text | `#17231E` | High-contrast text on light surfaces |
| Muted text | `#66716A` | Secondary labels |
| Risk colors | restrained red/amber/green | Risk semantics only; always pair with text/icon |

Do not substitute the theme with a generic blue-and-white cybersecurity palette. Do not change the palette between pages. Red/amber/green may be used only for risk/status meaning and must not replace the emerald/gold brand palette.

## 8.2 Reference Images Are the Implementation Target
The approved UI reference PNGs are included under `ui_reference_images/` and indexed in `28_UI_REFERENCE_IMAGE_INDEX.md`. They are the exact implementation target, not loose inspiration.

**Strict visual requirement:** reproduce each reference image faithfully, preserving every visible element and layout decision in the actual Streamlit app. The images are not decorative inspiration and must not be ignored or replaced by a different layout. Match:
- page composition and hierarchy
- sidebar width, selected state, logo/branding placement
- header height and account controls
- page title/subtitle
- card/panel positions, sizes, spacing, borders, radii, shadows
- typography hierarchy, icon style, chart placement
- labels, button positions, and visible content
- selected navigation/tab states and page-to-page flow
- exact approved color palette

Do not invent a different UI or omit visible sections. If a reference contains sample metrics or fictional case details, preserve the **layout** but replace values with honest app data; label synthetic/demo values. Never hardcode illustrative statistics as real results.

Target visual comparison viewport: **1600 × 900 desktop** (or the closest supported browser viewport). Build and compare screenshots at this viewport. Do not accept avoidable differences. Capture screenshots and compare side-by-side plus overlay/diff; iterate until visually faithful. If a residual difference is caused by Streamlit/browser constraints, document it explicitly. Do not redesign or silently substitute another layout.

## 8.3 No Page Scrolling — Mandatory
**The primary application page must fit within one viewport and must not have vertical or horizontal page scrolling at the target desktop viewport.** This is a strict acceptance requirement, not a preference.

- At 1600 × 900, all primary page sections, navigation, visible cards, controls, and key actions must fit on-screen. This is a strict pass/fail requirement.
- Do not solve overflow by hiding required content, clipping controls, or placing the whole page in a scroll container.
- Use compact spacing, carefully sized cards, responsive columns, concise labels, and progressive disclosure (tabs, expanders, dialogs) for secondary detail.
- Case/event lists and long evidence detail may use a clearly bounded **internal panel** only when necessary; the overall page itself must remain fixed to the viewport.
- Do not use a full-page long form. New Investigation must use compact evidence-type tabs and bounded inputs consistent with its reference.
- At smaller viewports, reflow content without horizontal page overflow; if all content cannot fit vertically, preserve usability with internal panels and document the minimum supported viewport. Do not claim the no-scroll gate passed at a viewport where it was not checked.
- Never hide browser scrollbars as a substitute for fitting the layout.

## 8.4 Motion and Interaction
Implement functional interactions, not static mockups:
- Sidebar navigation changes pages with a brief, restrained transition (fade/slide, approximately 120–220 ms) where supported.
- Buttons have hover, focus, pressed, disabled, and loading states.
- Tabs visibly change selected state and content.
- Case rows/cards open the selected case; investigation tabs switch the active analysis section.
- Start Investigation shows progress and per-agent status; completion/error states update in place.
- Charts/graphs have useful hover/selection behavior where supported.
- Confirmation dialogs are required for destructive actions.
- Respect `prefers-reduced-motion`; provide a no-animation mode.
- Animations must not delay important actions, obscure data, or imply analysis has completed before it has.
- Do not create fake loading animations or fake live-agent status.

## 8.5 Main Navigation and Page Inventory
The left sidebar must contain exactly these primary destinations, in this order:
1. Dashboard
2. New Investigation
3. Case History
4. Analytics
5. Settings
6. About Project

Do **not** add “Case Investigation,” “Evidence & Agent Analysis,” “Evidence Graph,” or “Scam Tracker” as primary sidebar items. Those are views inside a selected case/investigation.

### Page 1 — Dashboard / Home
Match `ui_reference_images/01_dashboard.png`.
- Hero banner introducing UPI ScamTrace and primary actions: Start New Investigation, View Demo.
- Summary cards for case counts and risk distribution.
- Project-wide risk overview and scam-journey-stage chart.
- Recent investigations table with a route to Case History.
- Multi-agent status panel based on actual configured/available agents.
- If no cases exist, show a polished empty state; never show invented live totals.

### Page 2 — New Investigation / Evidence Intake
Match `ui_reference_images/02_new_investigation.png`.
- Hero with the intake → analysis → report progression.
- Evidence type tabs: Messages/Chat, Call Summary, URL/Link, QR Code, Payment/UPI, Files/Screenshots.
- Support multiple evidence items per case.
- Case title, incident date/period, optional context.
- Validated upload area and clear file size/type errors.
- Clear All and Start Investigation actions.
- Use safe guidance and warnings; never request PIN, OTP, passwords, or bank login credentials.
- No full-page scrolling at target viewport.

### Page 3 — Case History
Match `ui_reference_images/03_case_history.png`.
- Search and filters for date, status, and risk.
- Case list/table with ID, title/scenario, risk label, status, updated time.
- Selecting a case opens its detail/investigation workspace.
- No separate sidebar item for an individual investigation.
- Use real persisted cases; synthetic cases visibly labeled.

### Page 4 — Analytics / Scam Intelligence
Match `ui_reference_images/04_analytics.png`.
- Project-wide metrics across cases, not one case’s evidence detail.
- Overall case/detection trends, high/medium/low/insufficient-evidence distribution.
- Scam type and journey-stage patterns.
- Agent performance and confidence, with dataset/mode context.
- Evidence source/type distribution and multi-evidence correlations.
- Any statistic shown must be computed from persisted data or the labeled evaluation dataset. If the dataset is empty, show an empty state, not placeholder percentages.
- Analytics may display the investigation-workspace tab strip shown in the approved image as a visual motif only if its interaction is clearly separated from global analytics; do not misrepresent global metrics as a selected case’s analysis. The global sidebar must highlight Analytics.

### Page 5 — Settings
Match `ui_reference_images/05_settings.png`.
- General preferences, AI/model configuration, agent controls, security/privacy, notifications, storage/data, appearance.
- Only show settings that are implemented.
- Never expose API keys/secrets; use masked status and environment/config instructions.
- Offline mode must work without provider credentials.
- Display actual storage/config state; do not fabricate version, model, storage, or system values.
- The main sidebar highlights Settings.

### Page 6 — About Project
Match `ui_reference_images/06_about_project.png`.
- Product overview and objective.
- Key features.
- Architecture flow: user-provided/synthetic evidence → specialist agents/LangGraph → timeline/evidence graph/assessment/report.
- Agent roles, technology stack, use cases, project information, limitations, and documentation/source-code links if real.
- Clearly state student prototype; no official UPI/bank affiliation.
- The main sidebar highlights About Project.

## 8.6 Selected-Case Investigation Workspace (Inside Case History)
A user reaches this workspace by selecting a case in Case History. Show case title/ID, risk label, status, and a secondary navigation strip:
1. Scam Timeline
2. Evidence & Agent Analysis
3. Evidence Graph
4. Scam Tracker / Journey Tracker
5. Final Assessment
6. Report & Actions

The active secondary tab must be visually obvious. The global sidebar remains on **Case History** when opened from Case History. This workspace is not a separate primary page.

### Scam Timeline
Chronological events, timestamps, channel, source/provenance, event type, and expandable detail.

### Evidence & Agent Analysis
Case-specific evidence inventory and agent findings:
- evidence items with event IDs, source, timestamp, provenance, parsing status
- specialist agent outputs, status, confidence/uncertainty, evidence references
- consensus, conflicts, missing evidence, and fallback state
- clear distinction between user-provided facts, parser output, deterministic rules, and model inference

### Evidence Graph
Evidence/event/entity nodes and grounded relations with relation legend and table fallback.

### Scam Tracker / Journey Tracker
Stage-based sequence view; show observed stages, inferred stages, evidence references, gaps, and confidence. Do not imply an official tracking connection.

### Final Assessment
Risk label, deterministic rationale, supporting event IDs, uncertainties, alternative explanations, and safe next steps.

### Report & Actions
Review/export Markdown or JSON; delete case with confirmation; show disclaimer and safe guidance.

## 8.7 Shared Components
- Sidebar brand and active navigation state
- Header/title/subtitle and user controls
- Emerald hero/banner
- Ivory cards with restrained champagne borders/shadows
- Risk badge with text and icon
- Case summary header
- Evidence row/card
- Agent status/finding card
- Empty/loading/error/partial/offline states
- Confirmation dialog and toast/inline feedback
- Chart panel with title, time range/dataset label, and caption
- Primary/secondary/tertiary buttons

## 8.8 Streamlit Implementation Notes
- Use Streamlit multipage routing or a controlled router, but preserve the six primary destinations and case-level tabs.
- Use reusable components and a centralized theme/CSS file; do not duplicate style snippets across pages.
- Use `st.session_state` only for transient UI state; persist case data through repositories.
- Prefer Plotly for charts and a graph visualization with a readable table fallback.
- Use custom CSS carefully for the approved composition, responsive layout, card styling, and transitions. Avoid brittle selectors where possible.
- Validate behavior in the actual Streamlit app, not only in a static HTML mockup.
- If a reference component cannot be reproduced exactly with Streamlit, implement the closest functional equivalent and document the specific limitation; do not silently redesign.

## 8.9 Accessibility and Safety
- Readable contrast and font sizes.
- Keyboard-accessible controls and visible focus.
- Risk never communicated by color alone.
- Plain-language warnings; no certainty beyond evidence.
- No fake “UPI verified,” “bank verified,” or official affiliation badge.
- Show synthetic/demo labels where appropriate.
- User-facing disclaimer: “ScamTrace is a student prototype decision-support tool. It may miss scams or produce false alarms. It does not verify UPI transactions, block or reverse payments, or replace official bank/payment-provider guidance. Verify independently through trusted official channels.”

## 8.10 UI Acceptance Gates
- Six primary pages match their corresponding reference images at target viewport.
- All six use the locked palette consistently.
- Sidebar/page hierarchy is correct.
- Case workspace is nested under Case History, not global navigation.
- Every button/tab/navigation control performs its stated action.
- Transitions are restrained and respect reduced-motion.
- No page-level vertical/horizontal scrolling at 1600×900.
- No content is clipped or hidden to satisfy the no-scroll rule.
- Data shown is actual, synthetic-labeled, or clearly empty; no fake analytics.
- Empty, loading, partial, error, offline, and insufficient-evidence states exist.
- Verify with screenshots from the running app and record actual results.


## 8.8 Exact UI Asset and Screenshot Gate
The PNGs in `ui_reference_images/` must be used as the exact visual targets. Do not change their labels, page composition, section order, colors, or placement. Codex must capture a screenshot for every page at 1600×900, compare against its corresponding source image using side-by-side and overlay/diff, correct discrepancies, and record evidence. The screenshot itself must never replace functional UI. If a control cannot be implemented, keep its visual position and show an honest disabled state. Missing assets or unverified comparisons must be reported, not assumed.
