# Summary
A short description of what this PR does and why.

## Related issues
Closes #<issue_number>
Relates to #<issue_number>

## Type of change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] Feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Refactor (no behavioral changes)
- [ ] Performance
- [ ] Documentation
- [ ] Tests only
- [ ] CI/CD / Chore

## Context / Approach
What’s the motivation and context? Any design decisions, trade-offs, or alternatives considered?

## How to test
Provide clear, reproducible steps.

1. Setup:
   - Commands/env vars needed to run locally
2. Execute:
   - Steps, API calls, or CLI commands to verify
3. Validate:
   - What output/behavior to expect

<details>
<summary>Example commands (adapt as needed)</summary>

```sh
# create/activate env (choose your flow)
# uv
uv sync
uv run python -m pytest -q
# or venv/pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q

# run app (if needed for manual verification)
python main.py
```
</details>

## Screenshots / Logs (optional)
Add images, terminal output, or traces that help reviewers.

## API contract changes
- [ ] No API changes
- [ ] Yes — updated OpenAPI/docs and affected clients
If yes, summarize the change and link to updated docs/schemas.

## Breaking changes
- [ ] None
- [ ] Yes (describe migration steps)

## Deployment / Migration notes
Any migrations, feature flags, environment variables, or operational steps?

## Security considerations
Auth, permissions, secrets, PII, rate limiting, DOS vectors, etc.

## Checklist
- [ ] Self-reviewed the code
- [ ] Added/updated tests
- [ ] Updated documentation where needed
- [ ] Lint/format pass locally
- [ ] Type checks/build pass (if applicable)
- [ ] Backward compatible (unless noted above)
- [ ] Added release notes (below)

## Release notes (1–2 lines, user-facing)
What should appear in the changelog/release notes?