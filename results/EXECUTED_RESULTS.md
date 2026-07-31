# Executed benchmark results

> Status: executed locally with the deterministic offline oracle. These are not live LLM results.

## Overall summary

| defense              |   attacked_cases |   clean_controls |   BASR_percent |   SASR_percent |   CSASR_percent |   VOR_percent |   utility_under_attack_percent |   clean_utility_percent |   detector_recall_percent |   detector_false_positive_percent |   blocked_percent |   defense_effectiveness_absolute_pp |   defense_effectiveness_relative_percent |
|:---------------------|-----------------:|-----------------:|---------------:|---------------:|----------------:|--------------:|-------------------------------:|------------------------:|--------------------------:|----------------------------------:|------------------:|------------------------------------:|-----------------------------------------:|
| baseline             |             2180 |               29 |         100    |         100    |          100    |         99.45 |                           0    |                     100 |                     53.03 |                                 0 |              0    |                                0    |                                     0    |
| prompt_hardening     |             2180 |               29 |          57.16 |          57.11 |           57.11 |         56.61 |                          42.89 |                     100 |                     42.89 |                                 0 |              0    |                               42.89 |                                    42.89 |
| detector_abort       |             2180 |               29 |          43.85 |          43.85 |           43.85 |         43.3  |                           0    |                     100 |                     53.03 |                                 0 |             56.15 |                               56.15 |                                    56.15 |
| tool_policy          |             2180 |               29 |           2.84 |           2.25 |            2.25 |          2.29 |                          97.75 |                     100 |                     53.03 |                                 0 |              0    |                               97.75 |                                    97.75 |
| independent_reviewer |             2180 |               29 |           0.55 |           0.55 |            0.55 |          0    |                           0    |                     100 |                     53.03 |                                 0 |             99.45 |                               99.45 |                                    99.45 |
| combined             |             2180 |               29 |           0.64 |           0.55 |            0.55 |          0.09 |                          97.25 |                     100 |                     53.03 |                                 0 |              2.2  |                               99.45 |                                    99.45 |

## Results by suite and setting

| defense              | suite          | setting   |   cases |   BASR_percent |   SASR_percent |   VOR_percent |   utility_under_attack_percent |
|:---------------------|:---------------|:----------|--------:|---------------:|---------------:|--------------:|-------------------------------:|
| baseline             | injecagent     | base      |    1054 |         100    |         100    |        100    |                           0    |
| baseline             | injecagent     | enhanced  |    1054 |         100    |         100    |        100    |                           0    |
| baseline             | redcrew_native | native    |      72 |         100    |         100    |         83.33 |                           0    |
| combined             | injecagent     | base      |    1054 |           0.09 |           0    |          0.09 |                         100    |
| combined             | injecagent     | enhanced  |    1054 |           0.09 |           0    |          0.09 |                         100    |
| combined             | redcrew_native | native    |      72 |          16.67 |          16.67 |          0    |                          16.67 |
| detector_abort       | injecagent     | base      |    1054 |          66.13 |          66.13 |         66.13 |                           0    |
| detector_abort       | injecagent     | enhanced  |    1054 |          17.74 |          17.74 |         17.74 |                           0    |
| detector_abort       | redcrew_native | native    |      72 |         100    |         100    |         83.33 |                           0    |
| independent_reviewer | injecagent     | base      |    1054 |           0    |           0    |          0    |                           0    |
| independent_reviewer | injecagent     | enhanced  |    1054 |           0    |           0    |          0    |                           0    |
| independent_reviewer | redcrew_native | native    |      72 |          16.67 |          16.67 |          0    |                           0    |
| prompt_hardening     | injecagent     | base      |    1054 |          93.55 |          93.55 |         93.55 |                           6.45 |
| prompt_hardening     | injecagent     | enhanced  |    1054 |          17.84 |          17.74 |         17.84 |                          82.26 |
| prompt_hardening     | redcrew_native | native    |      72 |         100    |         100    |         83.33 |                           0    |
| tool_policy          | injecagent     | base      |    1054 |           0.09 |           0    |          0.09 |                         100    |
| tool_policy          | injecagent     | enhanced  |    1054 |           0.09 |           0    |          0.09 |                         100    |
| tool_policy          | redcrew_native | native    |      72 |          83.33 |          68.06 |         66.67 |                          31.94 |

## Interpretation

The exact least-privilege policy eliminates the public InjecAgent attacks in this adapter because the attacker tools are outside the explicit user-task capability set. This is a structural control-plane result, not evidence that a language model is intrinsically robust.

The RedCrew-native suite contains output-only, same-tool, memory, and stealth goal-hijack cases. The residual stealth cases demonstrate why tool allow-listing alone is insufficient and why deterministic output validation or human approval remains necessary.

The detector-abort profile reduces attack success but sacrifices utility whenever it aborts. Prompt sanitization and least-privilege enforcement preserve more user-task utility.

## Manifest

```json
{
  "generated_at": "2025-03-25T15:06:20.765995+00:00",
  "engine": "DeterministicAttackFollowingOracle-v1",
  "profiles": [
    "baseline",
    "prompt_hardening",
    "detector_abort",
    "tool_policy",
    "independent_reviewer",
    "combined"
  ],
  "case_count": 2209,
  "attack_case_count": 2180,
  "clean_control_count": 29,
  "run_count": 13254,
  "dataset_fingerprint": "0a6fd87af4c7771a7e9480977b0a25a4bbe43f58dc6ee7842f129e19fcc63500",
  "limitations": [
    "Offline results evaluate deterministic control-plane defenses, not a live LLM.",
    "The public InjecAgent adapter uses an exact task-tool allow-list, which structurally favors least-privilege defenses.",
    "Live model results must be produced separately with pinned model identifiers and raw traces."
  ]
}
```