---
name: warriors-work-principles
description: Use when researching, designing, creating, optimizing, or delivering visual work, presentations, documents, websites, or other verifiable artifacts in this user's environment.
---

# Warriors 工作守则

Use this workflow as the default operating method for research, design, creation, implementation, and delivery tasks. The goal is not merely to follow tools mechanically, but to make the reasoning behind the result visible and to finish with a verified artifact.

## Core rule

Do not treat a Skill call, prompt, plan, or successful tool response as the design or as completion. A real task should move through research, analysis, design judgment, plan, execution, verification, and iteration.

## Required workflow

Scale the workflow to the requested stage and scope. For a local revision, reuse the approved concept and existing evidence, inspect only affected constraints, and execute the requested change. Analysis-only requests end with analysis. Do not turn every task into a new concept search or approval gate.

Before substantive work, select and read the minimum applicable skills. Revisit that selection at execution when the output format and production route are known; step 5 is not permission to postpone the initial skill preflight.

### 1. Research first

- Inspect the task context, existing files, references, prior decisions, constraints, audience, use case, format, and acceptance criteria.
- If the user supplies references, analyze them first. If not, proactively find relevant product, visual, web, or technical references when research would improve the result.
- Distinguish confirmed facts, extracted patterns, assumptions, and risks.
- Classify every input before using it: content source, layout reference, style/material reference, or research reference. Do not let a reference silently replace the user's actual content or constraints.
- For new creative directions, build a short subject inventory from verified facts: distinctive artifacts, language, place, people, materials, numbers, constraints, or rituals. Use it to drive the concept and asset search. Never invent client details to make the inventory distinctive. For reproduction or local edits, inventory the features and geometry that must be preserved instead.
- Inventory real execution resources: supplied assets and their roles, permitted asset sources and rights, available generation/editing tools, and the actual export/render path. Resolve a critical missing production capability with a representative check before building a full batch. Do not promise unavailable photos, footage, data, or native editability.

### 2. Analyze references into reusable design knowledge

Do not stop at “looks good” or “feels premium.” Explain concrete observations such as:

- information architecture and page structure;
- visual hierarchy and attention path;
- content density, spacing, and browsing rhythm;
- image, text, button, and whitespace relationships;
- typography, color, shape, shadow, material, and motion language;
- navigation, filtering, feedback, loading, and error behavior;
- mobile touch targets, readability, responsive behavior, and accessibility;
- what is brand-specific, what is reusable, and what should not be copied.

For every important reference, answer: What problem does it solve? Why does the solution work? Which principle applies here? What should be rejected?

For each planned section, frame the content as **claim -> evidence -> treatment**:

- **Claim:** what the audience should understand, believe, or do;
- **Evidence:** the supplied fact, image, example, number, demonstration, or interaction that supports it;
- **Treatment:** the layout, sequence, visual device, or motion that makes the evidence legible.

Here a claim can be an instructional point, decision, comparison, or task, not just persuasion. For new structures, remove filler or replace unsupported claims with justified content. Preserve all required user, organizer, quoted, and regulatory content; flag missing evidence instead of deleting or inventing it. Do not impose a marketing-page sequence on a deck or working tool.

### 3. Make an independent design judgment

- Do not blindly imitate references or push every decision back to the user.
- Propose a clear direction based on the audience, content, use case, platform, and desired emotion.
- For open-ended work, provide two or three genuinely different approaches with trade-offs and recommend one.
- Ground those approaches in inspected examples or known reusable patterns. Distinguish them by composition, information structure, material or motion logic, and asset requirements, rather than merely swapping colors. Choose by subject fit and feasibility; do not randomly select or blend incompatible directions. Inspect references directly when visual judgment depends on them, rather than treating their captions as evidence.
- Explain why the recommendation fits the task.
- For open creative work, write the central concept as a sentence: **[a specific thing from the subject] becomes [a concrete design device].** Test it against a comparable subject; if it still works unchanged, deepen the concept or state why a familiar treatment is appropriate. Reference reproduction, standardized reporting, and task-focused tools need fidelity or efficiency, not forced novelty.
- For an interactive product, identify the meaningful action the user must complete and make it work. For a video or animated slide, identify the intended change and viewing sequence. Static work needs no invented interaction or motion.

### 4. Show the design logic before making

Before creating the final artifact, present an appropriately sized design proposal containing:

- goal and core experience;
- references and the specific lessons extracted from them;
- selected direction and rejected alternatives;
- page, composition, or system structure;
- information hierarchy and user path;
- visual language, color, typography, spacing, and density;
- key components or key-frame logic;
- output specifications and quality criteria.

The user should understand why the result will look and behave as proposed before execution begins.

Record the proposal as one short decision contract in the existing project record when a record is needed: preserved constraints, changed structure, chosen direction and rationale, real assets available, unknowns, output format, and rejection criteria. Reuse it during execution to prevent drift. For reference-sensitive work, state exactly what the reference governs and what remains your own decision. The proposal does not create an extra approval gate; respect existing authorization and any confirmation explicitly requested by the user.

### 5. Choose Skills minimally and flexibly

- Search available Skills before acting and select the most suitable Skill for the current stage.
- If multiple Skills overlap, use only the best match. Combine Skills only when their responsibilities are distinct.
- Do not invoke Skills for display or ceremony, and do not let a Skill's fixed workflow replace design judgment.
- Read and follow the selected Skill's `SKILL.md`; higher-priority instructions and current task constraints take precedence.

### 6. Write prompts or specifications only after the direction is clear

Prompts, code specifications, parameters, and production instructions must encode the confirmed design judgment. Include the subject, structure, hierarchy, style, constraints, output requirements, and exclusions as needed. When the user asks for an artifact, a prompt is an execution instrument and does not replace that artifact. When the user explicitly requests only a prompt, specification, or analysis, deliver that requested output and stop.

### 7. Execute the real deliverable

- For a new visual system, uncertain export path, or costly batch, execute a representative slice with real content and realistic density first. Inspect it, then reuse its validated assets and design parameters across the batch. A local revision with a proven production path needs no new pilot or approval gate.
- When the user asks for a design, image, webpage, document, presentation, code, or other artifact, perform the actual generation, implementation, rendering, export, or edit.
- Do not return only suggestions, prompts, pseudo-code, or a plan.
- If execution fails, diagnose, adjust, and retry when safe. Stop only when an external blocker or a missing user decision genuinely prevents progress.
- Provide a viewable result, file link, or exact path.

### 8. Verify with evidence

- Check that the real file exists and that its format, dimensions, structure, and content are correct.
- Visually inspect images and rendered documents; test webpages at mobile sizes and verify key interactions; build, run, or test code; review important spreadsheet data and formulas.
- Compare the result with the proposal, extracted reference lessons, and acceptance criteria.
- Never rely only on a successful exit status, API response, or filename.
- Review the artifact in separate passes: first-second/first-screen impression, hierarchy and composition, content completeness and proof, legibility and accessibility, responsive or playback behavior, and collisions/overflow. Use the passes that fit the medium; do not apply webpage-specific rules to a PPT or video without a reason.
- For original creative work, ask the subject-specificity test: after hiding the logo or title, can the work still be distinguished from a competitor? For faithful reproduction or formal reporting, test reference fidelity, information hierarchy, and subject accuracy instead.
- For visual creation or substantial redesign, read [visual-review.md](references/visual-review.md) and inspect the actual output using its medium-specific passes. A mechanical pass only establishes the measured conditions; it cannot establish design quality.

### 9. Revise and re-check

Actively look for missing content, weak hierarchy, wrong density, layout overflow, visual inconsistency, template-like output, incorrect formatting, runtime errors, and divergence from the agreed direction. Fix issues and verify again before claiming completion.

Prioritize broken requirements and content errors, then usability/legibility, then concept and composition, then detail. Each revision round names at most three highest-impact problems with observable evidence, fixes them, and rechecks the affected output plus critical invariants. Keep a concise before/after record when useful. Stop when the agreed criteria pass; do not manufacture revisions or endlessly chase a subjective score. If progress stalls, a capability is missing, or another attempt would exceed authorized scope or cost, report the specific unresolved item and evidence honestly.

## Example: mobile content-community UI

For a request such as “design a Xiaohongshu-style mobile website UI”:

1. Find or inspect relevant mobile content-feed, image-stream, lifestyle, and community references.
2. Show what each reference teaches about layout, density, navigation, cards, typography, color, and interaction.
3. Separate product-specific traits from reusable principles and original design decisions.
4. Propose distinct directions such as editorial content, community exploration, or refined brand presentation, then recommend one.
5. Show the structure, hierarchy, design system, and key component logic.
6. Optimize the prompt or implementation specification.
7. Build the real visual or interactive prototype.
8. Inspect it at mobile sizes, revise issues, and show the result.

## Communication standard

Keep progress updates concise and identify the current phase: research, analysis, design, execution, or verification. Never say “complete” when only a prompt was written, a Skill was invoked, or a tool was started. Final communication should lead with the real result and briefly state what was verified.
