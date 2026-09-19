# Contributing

The most useful contribution is a realistic case where the skill recommends the
wrong next action. Use the issue templates and synthetic or anonymized facts.

Keep the skill focused on one-person business decisions. Explain which behavior
your change improves and why the current instructions do not already cover it.
Do not add business infrastructure, mandatory files, or rules merely to expand
the package. The maintained entrypoint is `skills/solo-operator/SKILL.md`.

Before a pull request:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

For behavior changes, add or update a case and run the affected case with and
without the skill using the [evaluation guide](evals/README.md). Include actual
responses and rubric-based rationale, including failures. Model runs consume
your own Codex quota and are not required for documentation-only fixes.

Never submit credentials, real customer records, account logs, or invented
benchmark results. Clearly label illustrative examples. Preserve the MIT notice.
