# Behavioral evaluation rubric

This rubric and the eight synthetic cases are defined before running either arm.
The question is whether the response makes a defensible next decision, not whether
it repeats the skill's headings or preferred words.

Score each dimension **0, 1, or 2**: 0 = absent or materially wrong; 1 = useful but
incomplete; 2 = specific, supported, and appropriate to the case.

| Dimension | What earns 2 points |
| --- | --- |
| Evidence | Separates observed behavior, assumptions, estimates, and missing evidence; calculations are sound. |
| Uncertainty | Identifies the unknown most likely to change or kill the current decision. |
| Experiment | Proposes a concrete, proportionate next action and a decision signal; suggested thresholds are provisional. |
| Founder fit | Respects available hours, money, delivery costs, and operational commitments. |
| Decision | Recommendation follows the evidence and current strategy; it neither builds prematurely nor stalls earned delivery. |

A scenario passes with **at least 8/10**, no zero in any dimension, and no critical
failure. The case-specific checks in `cases.json` guide judgment; they are not
keyword assertions. A different well-supported answer can pass.

Critical failures: fabricated demand evidence or business state; treating likes as
proof of payment; an unsupported 24/7 guarantee; overriding current strategy without
acknowledging the decision; refusing to help solely because optional state files are
absent; recommending a substantial build on the case's unsupported demand; or
stalling contracted delivery without a concrete blocker.

An AI reviewer reads every full answer and records a five-number score, critical
failures, and a short rationale. This is unblinded, qualitative review by the same
assistant that authors the skill, not independent human validation. Raw responses
allow readers to challenge the scores. One sample per case per arm is a smoke test,
not a statistical benchmark, proof of superiority, or evidence of business outcomes.

If a skill change is needed, retain the original run and rerun affected cases under
a new run ID. Do not overwrite failures or force the baseline to lose.
