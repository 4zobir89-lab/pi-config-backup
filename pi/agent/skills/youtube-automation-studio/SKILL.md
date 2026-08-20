---
name: youtube-automation-studio
description: |
  Full autopilot for a faceless YouTube explainer channel, powered by the Higgsfield MCP. Turns one sentence into a finished long-form video: researches what's working, picks the topic, writes a retention-engineered script, renders it end-to-end with Higgsfield, then packages it — titles, thumbnails, dubbing, ~20 shorts, a 30-day plan — tracking every credit, failures included. First run sets the channel up in two questions; afterwards it decides for you. Use whenever the user wants a faceless / AI-narrated / explainer YouTube video or channel, asks what's actually working in explainer videos right now, wants video topic ideas, a YouTube script, to render a video from a topic or script, titles/thumbnails/packaging, to translate or dub a video, shorts from a video, a content calendar or 30-day plan, says "start video N from the plan", or asks what their generations cost — even if they never mention Higgsfield.
---

# YouTube Automation Studio — faceless channel autopilot

One chat, one pipeline: topic → research → script → rendered video → packaging → shorts → plan. The user typed one sentence; everything else is your job. This skill exists because the manual version of this work (60 prompts, 60 generations, matching styles, syncing narration) is why people quit — so never hand the user a piece of that work if a tool or a decision of yours can absorb it.

## The autopilot contract

The user chose an autopilot. That means:

- **Decide, announce, move.** Every decision you make gets exactly one line with the reason ("Style: Mixed Media — documentary collage look, fits the history lane."), then you proceed. No option lists, no "would you like…".
- **Questions are for setup only — with five sanctioned widget moments.** After first-run setup, the skill asks questions at exactly five moments, each in an interactive AskUserQuestion widget, never elsewhere: (1) the **duration question**, once, right after the user approves the script (see the pipeline gate); (2) the **translation questions**, once, right after the final video is delivered — "translate this video?" plus "into which language?" (Spanish always among the options), both in a single widget call; (3) the **packaging question**, once, right after the translation step resolves — "generate titles and thumbnails?"; (4) the **pick questions**, once, right after the 3 titles + 3 thumbnails are delivered — "which title?" plus "which thumbnail?", both in a single widget call; (5) the **shorts question**, once, right after the user has picked — "create shorts from this video with Higgsfield Shorts Studio?". Blockers aside: if you are genuinely blocked (no YouTube URL for shorts, balance too low, MCP not connected), state what's needed in one line and stop — a blocker, not a question.
- **One gate: the script.** The render is never fired on the skill's own initiative. After the script is written, present it (per `references/script.md`), then STOP and wait for the user's explicit go ("proceed", "go", "render it"). This is a checkpoint, not a question — everything before it (setup, research, script) is free and touches no Higgsfield MCP tools; the first MCP call and the first paid generation both happen after the go.
- **Short output.** The user is watching a pipeline run, not reading a report. One line per decision, compact tables for status, no walls of text. When asked something (like "what's working right now"), answer in a few sentences and a short list — never twenty options.
- **Override beats default.** Anything the user states (topic, length, language, style, voice) wins over profile and policy, instantly. Channel-level overrides (style, voice, language, niche) also update `profile.md`; video-level ones don't.
- **Never re-ask what the conversation already answered.** If the user's request implies the niche or topic, the setup flow skips that question.

## Requirements

The Higgsfield MCP connector is normally required (tools like `get_workflow_instructions`, `generate_video`, `explainer_video`). If those tools are missing, say so and give the fix in two lines: grab the MCP link at higgsfield.ai → Claude: Settings → Connectors → Add custom connector → paste link → Connect. **But in this environment the generation tools are unavailable — so instead of stopping, switch to Prompt-only mode below.**

Web research uses the host's own web search / fetch tools (best-effort; if none exist, write from domain knowledge and mark every fact as an unverified prior). Files below live in the working folder.

## Prompt-only mode — the text deliverable (no MCP, no generation tools)

Default mode in this environment. No MCP calls, no CLI, no paid jobs, no ledger — the deliverable is **pure text** the user can feed into any video generator later (Higgsfield, Veo, Runway, Kling, Sora, ElevenLabs…).

### The flow — max 3 questions, then ship

1. **Ask AT MOST 3 questions, in ONE round.** Skip any the conversation already answered (a topic that implies a niche skips Q1; a named language skips Q2):
   - Q1 — Niche (only if the topic doesn't imply one)
   - Q2 — Language (default English)
   - Q3 — Duration (default 10 min; options 6 / 8 / 10)
2. **Research, best-effort.** Use whatever web search/fetch exists; if none, write from domain knowledge and mark every fact as an unverified prior — never invent sources.
3. **Write the retention-engineered script** per `references/script.md` (cold open on the payoff, chapters of ~9–12 blocks, open loops ~every 6 blocks, 20–24 words per block, `N = minutes × 6` blocks).
4. **Produce the full package** (below). No "say go to render", no stopping — the package IS the delivery.

### The package — files to write under `videos/NNN-<slug>/`

| File | Contents |
|---|---|
| `research.md` | facts + sources (or clearly marked priors when no web) |
| `script.md` | human-readable chaptered script with loop annotations |
| `character_sheet.md` | the channel style anchor prompt + one prompt per recurring character (consistency bible) |
| `voiceover.md` | every narration line: spoken text (numbers spelled out), target ≤9.5 s, tone/pace, suggested TTS voice |
| `scene_prompts.md` | every block: SCENE / CAMERA / MOTION / STYLE / NEGATIVE prompts, tool-agnostic |

### Output contract per block (used by voiceover + scene files)

```
Block N (MM:SS–MM:SS)
NARRATION: <20–24 words, spoken form, ≤9.5 s>
SCENE: <subject + action + setting>
CAMERA: <shot type + movement — vary across blocks>
MOTION: <what animates>
STYLE: <channel style anchor — non-photoreal, consistent>
NEGATIVE: <no realism / no on-screen text / no extra characters>
```

### Guardrails

- The script quality gate from `references/script.md` still applies — this text package IS the video.
- Vary shot types across consecutive blocks (wide / detail / diagram / map) — the 10 s visual switch is itself a retention device.
- Reuse the same appearance tokens for a character in every block prompt (consistency).
- Numbers spelled out in narration; no on-screen text in visuals.
- In chat: present the questions first, then the full package inline (script + character prompts + voiceover + scene prompts) — the written reply is the deliverable. Close with one line on how to use the files in any generator.

## Channel memory

All state lives in `explainer-channel/` in the working folder:

```
explainer-channel/
├── profile.md      # the channel: niche, language(s), style preset + style-key job id, voice, defaults
├── ledger.md       # every credit spent, failures included — the "counter"
├── plan.md         # 30-day content calendar (when created)
└── videos/
    └── 001-<slug>/
        ├── research.md    # facts + sources
        ├── script.md      # human-readable chaptered script
        ├── blocks.md      # per-block narration + video prompts (machine-facing)
        ├── production.md  # every job id, status, cost, retries
        └── packaging.md   # titles, thumbnail jobs, the user's pick
```

Read `profile.md` at the start of every run. Log every paid job to `production.md` and `ledger.md` the moment it is submitted — never reconstruct costs from memory.

## First run

If `explainer-channel/profile.md` does not exist, run setup before anything that spends credits: read `references/channel-setup.md` and follow it. Setup asks at most two questions (niche, language) — everything else (visual style, narrator voice, aspect, length policy) you pick for the user and record in the profile, announced in one line each. **Setup, research, and scriptwriting make no Higgsfield MCP calls** — style-key generation and the exact voice pick are deferred to the first render's pre-flight (`produce.md` step 0), after the script gate. The profile records that these choices were delegated to the skill at setup, so downstream workflows must not re-open them.

**Exception:** the trends question ("what's working right now?") is answerable without a profile — answer it first (see `references/topics.md`), then if no profile exists, close with one line: "Say a number and I'll set the channel up around it — two questions, one minute."

## Mode router

Match intent, not exact words. When a mode needs a reference file, read it before acting.

**Environment override:** generation tools are unavailable here → every mode below that ends in a render, packaging, translation, shorts, or plan still produces its **written deliverable only** (per Prompt-only mode above). "Render" becomes scene prompts + voiceover; "package" becomes 3 titles + 3 thumbnail prompts; "translate" becomes translated narration lines; "shorts" becomes 20 short segment prompts; "plan" is unchanged (it's already text). No MCP, no stop for "go".

| The user says (roughly) | Do | Reference |
|---|---|---|
| "what's working in explainers right now" / "topic ideas" | Trends answer: 4 niches, RPM-justified → topics in the picked niche | `references/topics.md` |
| "make a video (about X)" / "start my channel" / one-sentence topic | Research + script, present the script, STOP for explicit go; then render → packaging | all, in order |
| "write the script (for X)" | Research + script, stop before render, end with "say go to render" | `topics.md`, `script.md` |
| "render this" / "go" (script exists) | Production | `references/produce.md` |
| "titles and thumbnails" / "package it" | 3 titles + 3 thumbnails | `references/grow.md` |
| "translate / dub it into X" | Second-language version | `references/grow.md` |
| "make shorts (from it)" | ~20 shorts | `references/grow.md` |
| "plan my first 30 days" | Content calendar | `references/grow.md` |
| "start video N from the plan" | Full pipeline for those rows, statuses updated | `plan.md` + all |
| "how much did this cost" / "the bill" | Ledger + reconciliation | Cost rules below |
| "change the style / voice / language / niche" | Update profile, announce the new pick | `references/channel-setup.md` |

## The pipeline

For "make a video", stages 1–2 run back-to-back (both free). Then the pipeline **stops**: present the script per `references/script.md` and wait for the user's explicit go. Stages 3–6 fire only after that go — no paid generation before it.

| # | Stage | What happens | Cost |
|---|---|---|---|
| 1 | Topic | Live web research, score candidates, pick one + one-line reason. User-given topic skips the pick but not the research. | free |
| 2 | Script | Retention-engineered chaptered script → per-block narration + prompts | free |
| — | **Gate** | Present the script (with the retention-craft note from `script.md`), STOP, wait for "proceed" | free |
| 3 | Duration + pre-flight | Ask the duration question (verbatim copy in `produce.md`, recommend 10 min; re-grid the script if the answer differs), then first-run provisioning if pending (style key + voice pick, per `channel-setup.md` "Deferred provisioning"), then cost estimate via `get_cost`, balance check | provisioning: one image; rest free |
| 4 | Render | Higgsfield video-explainer workflow: style key → N clips → N voice takes → server-side assembly into one MP4 | paid |
| — | **Translate?** | The moment the final MP4 is delivered, ask in ONE AskUserQuestion widget: translate this video? + into which language? (Spanish always an option). Yes → dub per `grow.md` | ask free, dub paid |
| — | **Package?** | Once translation resolves (dub done or declined), ask in ONE AskUserQuestion widget: generate titles and thumbnails? Yes → stage 5 | ask free |
| 5 | Package | 3 titles + 3 thumbnails | paid (images) |
| — | **Pick?** | Ask in ONE AskUserQuestion widget: which title? + which thumbnail? Record the pick in `packaging.md` | ask free |
| — | **Shorts?** | Once picked, ask in ONE AskUserQuestion widget: create shorts with Higgsfield Shorts Studio? Yes → shorts per `grow.md` | ask free, shorts paid |
| 6 | Grow (on request) | Translation/dub · ~20 shorts · 30-day plan | paid |

Stage details live in the references — read them when you reach the stage, not all upfront.

## Cost rules — the counter

The bill at the end of the video is a feature. Treat it like one:

- Before the render fires, estimate with `get_cost: true` (one clip × N + one voice take × N + style key if needed) and check `balance`. Announce as you fire, in one line: "Firing 48 clips + 48 voice takes ≈ N credits (balance: M)." This is an announcement, not a question.
- If balance < estimate: stop, say exactly what's short, call `show_plans_and_credits`. That's a blocker.
- Every submitted job goes in `ledger.md` immediately: date, video, item, job id, credits, status. **Failed jobs stay in the ledger** — the counter includes failures, that's the honesty of it.
- "The bill": read `ledger.md`, reconcile against `transactions` (authoritative), report one compact table — per video, failures included, grand total.

## Failures

A generation will occasionally fail. The policy (also in `produce.md`):

1. First failure → resubmit the same job once. Announce flat: "Block 12 failed. Rerunning — it stays on the counter."
2. Same job fails twice → the prompt is the problem, not luck. Fix it (strengthen the NEGATIVE line, simplify the scene) and resubmit.
3. Third failure → swap in a simpler scene for that block and move on. Never let one block strand a finished video.

## References

- `references/channel-setup.md` — first-run setup: the two questions, the style + voice auto-pick matrices, 16:9 style-key derivation, profile format
- `references/topics.md` — the trends answer, research recipe, topic scoring
- `references/script.md` — retention scriptwriting rules, block conversion
- `references/produce.md` — the render: workflow overrides, batching, job tracking, retries, assembly
- `references/grow.md` — packaging, translation/dubbing, shorts, the 30-day plan
