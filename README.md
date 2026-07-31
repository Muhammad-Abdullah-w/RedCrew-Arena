# RedCrew Arena

**A research-grade CrewAI project for adversarial prompting, indirect prompt
injection, least-agency enforcement, and reproducible security evaluation.**

RedCrew Arena combines CrewAI's role-based agents and sequential crews with a
security architecture in which model output is never trusted to authorize tool
execution. It includes a pinned public benchmark adapter, a new multi-agent
attack suite, deterministic defenses, reproducible results, tests, CI, Docker,
and a full report.

## What is genuinely included

- **2,108 public-derived attack cases**: 1,054 InjecAgent base cases and 1,054 enhanced cases, synthesized from 17 user cases and 62 attacker cases.
- **72 new CrewAI-specific cases**: goal hijacking, stealth output manipulation, data exfiltration, tool misuse, memory poisoning, and insecure-code regression.
- **29 clean controls** for utility and false-positive measurement.
- **Six defenses**: baseline, prompt hardening, detector-abort, exact tool policy, independent reviewer, and combined defense-in-depth.
- **13,254 executed offline runs** across all cases and profiles.
- **Live CrewAI mode** that generates structured plans but leaves authorization to deterministic policy code.
- **Reports and charts** with raw CSV/JSONL traces and an explicit result manifest.
- **20 automated tests passing** with **93% measured line coverage** in the bundled validation run.

## Important result boundary

The bundled results were **actually executed**, but with a deterministic
attack-following oracle. They test the surrounding security control plane and
are not claims about GPT, Claude, Gemini, or another live LLM. Public model
numbers in the research report are cited from the original benchmark papers and
are clearly labeled as external reported results.

## Architecture

```text
Red-team Crew -> attack corpus/mutations
                         |
User task + untrusted tool content
                         |
              CrewAI planner (proposal)
                         |
              structured ActionPlan
                         |
     detector -> least privilege -> reviewer
                         |
                audit-only sandbox
                         |
       BASR / SASR / CSASR / VOR / utility
```

The core rule is: **agents may propose; deterministic policy authorizes.**

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
pytest
redcrew benchmark --output results
```

Open:

- `results/EXECUTED_RESULTS.md`
- `results/summary.csv`
- `reports/RedCrew_Arena_Research_Report.pdf`

## Live CrewAI experiment

```bash
pip install -e ".[live]"
cp .env.example .env
# add the provider key and pin an exact model
redcrew live ia-user-01__ia-dh-01__enhanced --defense combined --model provider/exact-model-id
```

The live command saves raw output, parsed plan, policy reasons, and approval
status. It never performs the proposed external action.

## Offline defense profiles

| Profile | Behavior |
|---|---|
| baseline | Attack-following stress oracle, no defense |
| prompt_hardening | Detect and remove suspicious untrusted instructions, then continue the user task |
| detector_abort | Abort the entire run when injection is detected |
| tool_policy | Exact user-task capability allow-list |
| independent_reviewer | Independent deterministic review of tools and output |
| combined | Sanitization, least privilege, and independent review |

## Metrics

The project reports clean utility, utility under attack, BASR, SASR, CSASR,
VOR, detector recall/false positives, blocked rate, and absolute/relative
defense effectiveness. Definitions are in `docs/METRICS.md`.

## Online/public benchmark context

The report compares the project's design with the published InjecAgent and
AgentDojo results. These external numbers are not mixed into the executed result
tables. The public sources establish that indirect prompt injection remains a
material risk for tool-integrated agents and that tool filtering can be highly
effective while still leaving residual risk when required and attacker tools
overlap.


## Scientific limitations

- The offline oracle intentionally follows attacks; it does not estimate the probability that a specific LLM will comply.
- The exact tool allow-list is structurally strong on InjecAgent because many attacks need tools unrelated to the user task.
- The 29 clean controls are sufficient for regression testing, not for a high-confidence production false-positive estimate.
- Live model conclusions require repeated runs, pinned versions, confidence intervals, and raw traces.


## License and citation

Release validation: `VALIDATION.md`. Project code: Apache-2.0. The compact InjecAgent-derived records retain their
MIT notice in `THIRD_PARTY_LICENSES/`. Cite both RedCrew Arena and the upstream
benchmark when publishing derived work.
