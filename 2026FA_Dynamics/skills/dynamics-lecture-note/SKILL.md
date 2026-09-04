---
name: dynamics-lecture-note
description: Create or extend MC2103 Dynamics scrollable Korean lecture-replacement HTML notes from source slide PDFs and English auto-generated transcripts. Use when a lecture needs the established slide-by-slide layout, bilingual exam terminology, ASR reconciliation, or consistency with prior completed lecture notes.
---

# Dynamics Lecture Note

Create a source-grounded study note that can replace attending the English lecture and support English-written exams. Preserve the repository's existing course index, schedule decisions, and public-site structure.

## Required context

Before authoring, read [references/authoring-guide.md](references/authoring-guide.md) completely. Use [assets/lecture01-reference.html](assets/lecture01-reference.html) as the only structural and visual reference. Use [assets/lecture02-reference.html](assets/lecture02-reference.html) only to calibrate content depth for long derivations and problem solving; it is not a second layout reference. Always copy [assets/lecture-page.template.html](assets/lecture-page.template.html) as the starting file and replace its placeholders rather than composing a page from scratch.

Read [references/crimson-design-source.md](references/crimson-design-source.md) only when changing shared color, typography, or spacing tokens. It cannot override the Lecture 1 layout contract. The authoring guide already contains the web-specific adaptation; do not reintroduce fixed PowerPoint coordinates or forced page density.

## Source handling

1. Confirm lecture number, week, date, links, PDF, and transcript set from the local course index. Keep an unlisted date as `날짜 미기재`; never infer it.
2. Inspect and render every PDF page. Use one 1920×1080 image and one `.source-section` per source page, in exact order.
3. Read every English transcript for the lecture. Map timestamps to slides and reconcile technical words against the visible slide and dynamics context.
4. Treat the hierarchy as PDF → transcript/video context → course index → clearly labeled editor enhancement. Never silently turn a guess into course content.

## Authoring invariants

- Produce a continuous scrolling HTML document. Core material must not depend on slide-next buttons, accordions, or JavaScript.
- Keep every source slide, including title, divider, link, and reference pages. Do not invent explanations for pages without concepts.
- Put important nouns, state descriptions, problem verbs, and adjectives in repeated `English(한국어 번역)` form throughout the note, not only in the glossary or first occurrence.
- Explain relationships, assumptions, why each concept matters, and how the concept appears in exam wording. A translated bullet list alone is insufficient.
- Mark material not present in the lecture as `시험용 보강` or `편집자 보강`.
- Include an overview/concept map, a standalone concept summary, slide-by-slide sections, exam English model answers, glossary, ASR correction log, and sources. The standalone summary must be sufficient to understand the lecture's main definitions, relationships, assumptions, and problem-solving flow without reducing the detailed slide explanations.
- Classify each Summary video by its actual transcript content. If it genuinely recaps the current lecture's concepts, use it as supporting evidence for the standalone concept summary after reconciling it with the slides. If it is a future-course roadmap, schedule, or administrative note, keep it in a separately labeled section and do not present it as the lecture's concept summary.
- Use a neutral public tone. Never include assistant persona, user identity, private jokes, or internal tool/process commentary.
- Preserve relative links so the note works under a GitHub Pages repository subpath.

## Visual consistency

Reuse [assets/styles.css](assets/styles.css) and [assets/site.js](assets/site.js) rather than restyling each lecture. Preserve the template's top-level section order, IDs, classes, heading hierarchy, and card nesting exactly. `overview` uses the divider treatment without evidence chips; `exam-english` uses the neutral editorial section with `note-stack > exam-card > answer`; the audit section keeps `id="asr-log"`. The source-slide frame must remain identical across sections and preserve `16:9`. Update the shared CSS only when the change is first applied to Lecture 1 and improves every lecture.

## Validation

Run the repository's validator when available. Otherwise run:

```powershell
python scripts/validate_lecture_site.py <site-directory> <lecture-html-filename> <expected-pdf-page-count>
```

Require all checks to pass, then verify the index and at least the first and last slide asset through a local static HTTP server. Publishing, pushing, or changing repository visibility requires the user's request; skill invocation alone does not authorize external publication.
