# Simple scorecard — Solo Operator

> **Result:** the skill improved the number of cases with a strong, founder-fit experiment from **3/8** to **7/8**. Evidence handling was already strong without the skill, and the skill had one decision-focus regression in the idea-sprawl case.

This is a plain-language secondary summary of the published `2026-09-19-v0.1.0` run. It reuses the original five dimension scores; it does not make another model call.

## The three questions

| Simple question | No skill | With skill | Change |
| --- | ---: | ---: | ---: |
| Can it separate evidence from uncertainty? | 8/8 (100%) | 8/8 (100%) | +0 case |
| Does it propose a bounded test that fits the founder? | 3/8 (38%) | 7/8 (88%) | +4 cases |
| Does the decision follow the evidence? | 8/8 (100%) | 7/8 (88%) | -1 case |
| All three in the same answer | 3/8 (38%) | 6/8 (75%) | +3 cases |

The original five-point review averaged **9.375/10** without the skill and **9.750/10** with it. Both arms passed all eight cases under the original pass rule.

## Case-by-case view

`E` = evidence separated, `T` = bounded founder-fit test, `D` = decision follows evidence.

| Case | No skill (E/T/D) | With skill (E/T/D) | Raw answers |
| --- | --- | --- | --- |
| Unvalidated SaaS | ✅/—/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/01-unvalidated-saas/response.md) · [skill](results/2026-09-19-v0.1.0/skill/01-unvalidated-saas/response.md) |
| Idea sprawl | ✅/—/✅ | ✅/✅/— | [baseline](results/2026-09-19-v0.1.0/baseline/02-idea-sprawl/response.md) · [skill](results/2026-09-19-v0.1.0/skill/02-idea-sprawl/response.md) |
| Engagement versus payment | ✅/—/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/03-engagement-not-payment/response.md) · [skill](results/2026-09-19-v0.1.0/skill/03-engagement-not-payment/response.md) |
| Paid service | ✅/✅/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/04-paid-service/response.md) · [skill](results/2026-09-19-v0.1.0/skill/04-paid-service/response.md) |
| Affiliate economics | ✅/—/✅ | ✅/—/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/05-affiliate-economics/response.md) · [skill](results/2026-09-19-v0.1.0/skill/05-affiliate-economics/response.md) |
| Operational burden | ✅/—/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/06-operational-burden/response.md) · [skill](results/2026-09-19-v0.1.0/skill/06-operational-burden/response.md) |
| Current state versus old score | ✅/✅/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/07-current-state/response.md) · [skill](results/2026-09-19-v0.1.0/skill/07-current-state/response.md) |
| No project state | ✅/✅/✅ | ✅/✅/✅ | [baseline](results/2026-09-19-v0.1.0/baseline/08-no-project-state/response.md) · [skill](results/2026-09-19-v0.1.0/skill/08-no-project-state/response.md) |

## Two concrete examples

### Operational burden: the skill makes the stop signal easier to see

- **No skill:** “Treat this as an actively managed service until evidence proves otherwise.”
- **With skill:** “KILL the personal 24/7 guarantee. TEST a bounded administrative service.”
- [Read the full baseline response](results/2026-09-19-v0.1.0/baseline/06-operational-burden/response.md) · [Read the full skill response](results/2026-09-19-v0.1.0/skill/06-operational-burden/response.md)

### Idea sprawl: the skill still has a tradeoff

- **No skill:** “Give this one walkthrough and one concrete offer.”
- **With skill:** “For the exciting-ideas request, here are 30 brief brainstorming seeds—not validated opportunities.”
- [Read the full baseline response](results/2026-09-19-v0.1.0/baseline/02-idea-sprawl/response.md) · [Read the full skill response](results/2026-09-19-v0.1.0/skill/02-idea-sprawl/response.md)

## How to read this

The clearest positive signal is experiment design: the skill more often adds an explicit time, workload, price, or continuation cap. It does not create a new evidence advantage here because the baseline already handled the evidence cases well. The idea-sprawl answer also shows a real tradeoff: the skill followed the request for 30 ideas, but that diluted the immediate decision, so the decision check is marked as not strong.

## Limits

- The scorecard is a deterministic re-analysis of one sample per case, not a new benchmark.
- The underlying scores are the same unblinded qualitative AI review by the authoring assistant; they were not independently rescored for this page.
- The eight cases are synthetic, and both arms passed the original threshold. This does not establish statistical superiority, real customer outcomes, or profitability.
- The simple checks are intentionally easy to understand; they should be followed by repeated, blinded evaluation before making a stronger claim.

Source: [full report](REPORT.md) · [rubric](RUBRIC.md) · [reproduction guide](README.md)
