# Evaluate decisions, not catchphrases

There are two separate kinds of checks:

- **Package checks** run on every push and pull request on Windows and Linux.
  They verify the installable files and documentation, without model credentials.
- **Behavioral smoke tests** run manually through a logged-in Codex CLI. They
  consume Codex quota. The [rubric](RUBRIC.md) evaluates judgment from full responses.

Read the [published report](REPORT.md) and the eight [synthetic cases](cases.json).
The report links both arms' raw responses, including any failures.

## Reproduce a run

Prerequisites: Python 3.11+, a logged-in Codex CLI (tested with 0.154.0), and access
to the chosen model. Use the same CLI, model, reasoning effort, cases, and rubric
for both arms. Pin this repository to the release you want to evaluate.

```sh
python scripts/run_evals.py --arm baseline --model gpt-6-astra --out evals/results/my-run/baseline
python scripts/run_evals.py --arm skill --model gpt-6-astra --out evals/results/my-run/skill
```

Choose an available model if necessary and report that change. To rerun one case,
add `--case 04-paid-service` and use a new output directory. `--jobs 1` runs serially;
the default is two concurrent calls. Each call times out after ten minutes. Existing
result directories are never overwritten.

The runner ignores user configuration, requests `skip_host_skill_discovery`,
disables plugins, skill search, memory, and external tools, and starts each sample
in a fresh empty temporary directory. Authentication remains in the existing
Codex login store; it is neither copied nor published. The baseline receives only
the common evaluation instruction. The skill arm receives the same instruction
plus the exact skill text. The runner records that text and its SHA-256 hash.

This tests prompt-guided behavior, **not automatic skill selection or filesystem
retrieval**. The state-conflict case supplies file contents inside the prompt.
Installed-skill discovery is checked separately during release verification.
The isolation feature is version-sensitive. In the published run, a separate
`skills/list` audit still returned the common global catalog even with the flag;
it returned no `solo-operator` entry before installation in either configuration.
Do not interpret the flag as proof that every global instruction was removed.
Both arms retain Codex's built-in instructions and may share unrelated skill metadata.
Run controls before installing the target skill, or verify that your baseline
cannot discover it. Do not use an installed target as an allegedly clean control.
The runner refuses a baseline when it finds `solo-operator` in either standard
global skills directory. Check any custom discovery paths separately.

The output includes prompts, final responses, completion/usage events, timings,
requested model, configuration, and content hashes. Local stderr is saved only
when a call fails; inspect it for private paths or service details before sharing.
A zero runner exit code means responses completed without observed tool calls;
it does **not** mean their business advice passed the rubric.

Read every answer and score the five dimensions in the rubric. Publish the score
and rationale for each arm. A baseline may already pass every case. Do not change
the criteria after seeing results to manufacture an improvement.
