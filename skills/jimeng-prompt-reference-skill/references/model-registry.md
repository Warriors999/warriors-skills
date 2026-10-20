# Model and platform registry

This file is a routing aid, not a promise that a platform supports every field listed by a third-party source. Refresh entries when the platform, model version, or official documentation changes.

## Status vocabulary

- `verified`: current official documentation or current interface test supports the claim.
- `portable`: a principle is supported by another platform's first-party guide and may be used as a cautious baseline.
- `empirical`: observed in the user's own generation/export result; valid for that setup, not automatically universal.
- `unknown`: no reliable evidence; do not turn it into a precise instruction.

## 即梦／Dreamina

Last reviewed: 2026-10-12. Distinguish manual-derived prompt organization, observed UI behavior, and actual generated video evidence. The Seedance 2.5 public manual showed a September 21 update; see the local reference supplement for scope. Known UI names include 全能参考, 首尾帧, 智能多帧, 智能编辑 and 超长视频. In one logged-out observation, switching from 全能参考 to 智能多帧 changed the displayed model from Seedance 2.0 mini to Seedance 1.0 Fast. This is not a promise for every model/account.

Local output convention: list all provided references with stable 图片1/图片2, 视频1, 音频1 placeholders for the user to replace. Pure text placeholders do not prove UI binding, and chronology is separate from upload numbering. No browser inspection is required for each prompt-only request.

Current local status: `verified` for the high-level prompt organization summarized from the current Seedance 2.5 manual, chapter 3; see `references/jimeng-seedance-2.5.md`. It is still `unknown` for version-specific syntax and capability claims. The following items are not treated as official until checked against the current interface or official documentation:

- all-in-one reference and multi-reference image count;
- first-and-last-frame field semantics and which uploaded image is first or last;
- prompt weight syntax and special control tokens;
- fixed duration, frame rate, resolution, or aspect-ratio limits;
- true Alpha-channel video export.

Safe baseline: use the mode exposed by the current interface, put dimensions/duration/reference count in the interface controls, use short observable motion language, and test one change at a time. Mark the result as `empirical` if it is based on the user's export.

## Runway

Status: `portable` for the general image-to-video principles in the Runway Academy Prompting Guide: the image carries static composition and identity; text emphasizes motion, camera behavior, and temporal progression; start simple and avoid contradictory instructions. This does not transfer Runway-specific controls to 即梦.

## Square-Zero-Labs video prompting skill

Source identifier: `Square-Zero-Labs/video-prompting-skill@video-prompting`, inspected 2026-08-27. Status: `portable` for model/mode routing, reference-role mapping, and separating static facts from changes. Status: `unknown` for any platform-specific field outside the source's target ecosystem.

Do not import its model names, API fields, reference limits, duration limits, pricing, login instructions, or Alpha claims into an 即梦 answer.

## RunComfy / Seedance skill family

Status: `portable` only for the general ideas of reference-led identity, one main action, and explicit multimodal roles. Treat model routing, syntax, parameter names, limits, and interface steps as tool-specific and do not reuse them for 即梦.

## Green screen and Alpha

Status: `portable` post-production guidance. A pure green background, clean edges, spill reduction, matte quality, and an actual Alpha-capable export are separate checks. A prompt can request a uniform green background; it cannot prove that the rendered video contains an Alpha channel.
