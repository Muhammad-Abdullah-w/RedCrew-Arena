# Security policy

## Scope

RedCrew Arena intentionally contains adversarial text. The bundled tools are
simulators and never perform network, filesystem-destructive, financial, email,
or account actions. Live CrewAI mode produces structured plans; the deterministic
policy layer must approve every action before the sandbox records it.

## Reporting a vulnerability

Do not open a public issue for a vulnerability that could enable real-world
harm. Contact the repository maintainer privately and include reproduction
steps, affected version, impact, and a proposed mitigation where possible.

## Safe research rules

- Run only against accounts, systems, and data you own or are authorized to test.
- Keep destructive and external tools disabled in evaluation environments.
- Treat model output as untrusted data.
- Never place real secrets in benchmark contexts.
