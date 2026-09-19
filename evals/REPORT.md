# Behavioral smoke test — v0.1.0

**Both arms passed all eight scenarios under the predeclared rubric.** The baseline
was already strong. This run supports that Solo Operator can produce usable,
evidence-sensitive next steps; it does not establish that the skill is necessary,
statistically superior, or likely to produce a profitable business.

## Method

| Item | Recorded value |
| --- | --- |
| Run date | September 19, 2026 (UTC) |
| CLI | `codex-cli 0.154.0` |
| Requested model | `gpt-6-astra` in both arms; the runner records the request, not a server-attested model identity |
| Reasoning effort | `medium` in both arms |
| Samples | 8 scenarios × 2 arms × 1 sample = 16 responses |
| Review | Unblinded AI review by the authoring assistant; no independent human scoring |
| Pass rule | At least 8/10, no zero dimension, no critical failure |
| Skill version | Initial `v0.1.0` candidate, unchanged after this run |
| Skill SHA-256 | `b84f38e1c2f597e913919a124c0c599504752aa606f250385010c5bb81eab28d` |

The [cases](cases.json) and [rubric](RUBRIC.md) were written before the baseline.
The baseline ran before the skill was installed globally. The runner requested
`skip_host_skill_discovery` and disabled plugin loading, skill search, memory,
and external tools. A separate `skills/list` probe still returned 104 common
skills with and without that flag, but **no `solo-operator` entry** in either
configuration before installation. This verifies absence of the target from
discovery, not removal of all unrelated global metadata. Each response used a
fresh empty working directory. No tool calls were observed and
all 16 calls completed successfully. The skill arm added the full skill text to
the same common instruction; it did not receive the rubric or expected answers.

The current-state case embeds the project artifacts in the prompt. It tests which
evidence the model uses, not whether the CLI can retrieve files. See the
[reproduction guide](README.md) for isolation details and limitations.

## Scores and raw responses

Score order: **Evidence / Uncertainty / Experiment / Founder fit / Decision**.
Read the full responses behind each score; wording and headings are not pass criteria.

| Scenario | Baseline | With skill | Outcome |
| --- | --- | --- | --- |
| Unvalidated SaaS | [2/2/1/2/2 = 9](results/2026-09-19-v0.1.0/baseline/01-unvalidated-saas/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/01-unvalidated-saas/response.md) | Both pass |
| Idea sprawl | [2/2/2/1/2 = 9](results/2026-09-19-v0.1.0/baseline/02-idea-sprawl/response.md) | [2/2/2/2/1 = 9](results/2026-09-19-v0.1.0/skill/02-idea-sprawl/response.md) | Both pass; skill still supplies 30 ideas |
| Engagement versus payment | [2/2/2/1/2 = 9](results/2026-09-19-v0.1.0/baseline/03-engagement-not-payment/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/03-engagement-not-payment/response.md) | Both pass |
| Paid service delivery | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/baseline/04-paid-service/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/04-paid-service/response.md) | Both pass |
| Affiliate economics | [2/2/1/2/2 = 9](results/2026-09-19-v0.1.0/baseline/05-affiliate-economics/response.md) | [2/2/1/2/2 = 9](results/2026-09-19-v0.1.0/skill/05-affiliate-economics/response.md) | Both pass; acceptance criteria could be tighter |
| Operational burden | [2/2/1/2/2 = 9](results/2026-09-19-v0.1.0/baseline/06-operational-burden/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/06-operational-burden/response.md) | Both pass |
| Current state versus old score | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/baseline/07-current-state/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/07-current-state/response.md) | Both pass |
| No project state | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/baseline/08-no-project-state/response.md) | [2/2/2/2/2 = 10](results/2026-09-19-v0.1.0/skill/08-no-project-state/response.md) | Both pass |

No critical failures were observed. Every completed response is published, with
its exact prompt and completion record in the same directory. There were no
behavioral reruns, hidden failing samples, or skill revisions after these results.

## Why those scores

1. **Unvalidated SaaS:** Both reject a friend's opinion as demand and respect the
   eight-hour/$300 constraint. Baseline's fallback is to keep interviewing; the
   skill response explicitly marks insufficient conversations as inconclusive and
   makes the next outreach round bounded. Both recommend a manual paid pilot.
2. **Idea sprawl:** Both prioritize the real spreadsheet and distinguish pain
   from payment. Baseline proposes one walkthrough and one offer without an hour
   budget. The skill sets a two-hour cap but also supplies 30 brainstorming seeds.
   That respects the explicit request while diluting attention to the recommended
   experiment, so its Decision score is 1. Neither silently commits to a new idea.
3. **Engagement:** Both propose a transparent $19 manual pilot and distinguish
   attention from payment. Baseline limits customers but not delivery time; the
   skill separates discovery and delivery budgets and marks its thresholds as
   provisional. Both acknowledge renewal as a further uncertainty.
4. **Paid service:** Both recommend immediate scoped delivery, correctly separate
   $450 collected from $900 agreed value, and show $75/hour at 12 hours or $50/hour
   at 18 hours before other costs. Both track real labor and avoid treating three
   deposits as proof of scalable demand.
5. **Affiliate:** Both correctly calculate 9% click-through, 5% click-to-purchase,
   $64 after hosting, and roughly $5.33/hour before other costs. Both cap work at
   three hours and caution about noise. Baseline lacks a calendar cap; the skill
   adds 30 days but leaves the minimum improvement and payback window for the
   founder to choose. Experiment scores remain 1 in both arms. The skill also
   distinguishes approved commissions from cash received.
6. **Operations:** Both reject unsupported personal 24/7 coverage, narrow the offer,
   and identify sensitive-data and human-coverage burdens. Baseline describes a
   paid pilot but leaves the success/stop signal less explicit. The skill makes
   payment for a deliverable scope the continuation signal and caps discovery at
   two weeks/10 hours, without pretending that payment establishes profitability.
7. **Current state:** Both use the September state and decision log over the older
   market score, keep the newsletter on WATCH, and focus six hours on paid pilot
   offers. Both separate shared reports from payment and preserve the agreed strategy.
8. **No state:** Both help without demanding files or creating folders, allocate
   five hours, and label the price as experimental. Both treat one payment as
   permission for a small delivery rather than proof of a business. The skill
   additionally makes the possible distinction between user and payer explicit.

## Actual output excerpts

> “Provisional decision rule: one payment earns one delivery, not a dashboard.”

— [Unvalidated SaaS, with skill](results/2026-09-19-v0.1.0/skill/01-unvalidated-saas/response.md)

> “The highest-value uncertainty is now **whether you can deliver acceptable results within scope at an hourly return worth repeating**.”

— [Paid service, with skill](results/2026-09-19-v0.1.0/skill/04-paid-service/response.md)

These excerpts come from the stored responses. They illustrate the behavior;
they are not customer testimonials or proof of business outcomes.

## What remains unproven

- One sample per scenario does not measure run-to-run reliability or a statistically
  meaningful improvement over baseline. Qualitative score differences are subjective.
- The authoring assistant also scored the outputs. Independent, blinded human
  review could assign different scores.
- This set does not evaluate automatic selection, real filesystem retrieval,
  non-English behavior, live customer research, long-running projects, or other models.
- Installed-skill discovery and a fresh-session invocation are separate release
  checks, not part of this paired experiment.
- No actual revenue, customer acquisition, founder outcomes, or virality was measured.

Run metadata: [baseline](results/2026-09-19-v0.1.0/baseline/run.json) ·
[with skill](results/2026-09-19-v0.1.0/skill/run.json).
