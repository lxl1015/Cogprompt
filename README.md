## Run CogPrompt

Run the system from the project root using:

```
python -m src.main
```

## Evaluation Results

We evaluated CogPrompt against five baseline tutoring methods (LLM-only, YA-TA, LPITutor, KAPING, LLM+CDM) on three datasets: Linux (real undergraduate course), Math1, and Math2. Performance was scored by an LLM-as-a-judge (phi4:14B) across five dimensions: Accuracy (Acc), Personalization (Per), Pedagogy (Ped), Engagement (Eng), and Supportiveness (Sup).

### Overall Performance

| Method        | Math1 Acc | Per  | Ped  | Eng  | Sup  | Math2 Acc | Per  | Ped  | Eng  | Sup  | Linux Acc | Per  | Ped  | Eng  | Sup  |
| ------------- | --------- | ---- | ---- | ---- | ---- | --------- | ---- | ---- | ---- | ---- | --------- | ---- | ---- | ---- | ---- |
| LLM-only      | 3.08      | 1.98 | 2.48 | 1.39 | 3.76 | 3.01      | 1.87 | 2.39 | 1.38 | 3.70 | 3.62      | 2.43 | 3.27 | 1.74 | 4.04 |
| YA-TA [9]     | 3.58      | 2.88 | 3.13 | 2.03 | 4.24 | 3.67      | 2.80 | 3.05 | 2.08 | 4.24 | 3.89      | 2.86 | 3.44 | 1.91 | 4.23 |
| LPITutor [26] | 3.74      | 2.60 | 3.68 | 2.15 | 4.31 | 3.76      | 2.55 | 3.74 | 2.32 | 4.27 | 4.04      | 2.85 | 3.97 | 2.20 | 4.36 |
| KAPING [12]   | 3.72      | 2.77 | 3.86 | 2.32 | 4.24 | 3.72      | 2.74 | 3.88 | 2.25 | 4.25 | 3.91      | 2.85 | 3.98 | 2.31 | 4.38 |
| LLM+CDM [23]  | 3.78      | 3.10 | 3.80 | 2.66 | 4.53 | 3.81      | 3.00 | 3.77 | 2.59 | 4.51 | 3.99      | 3.33 | 3.30 | 2.71 | 4.57 |
| **CogPrompt** | 3.91      | 3.33 | 3.90 | 3.34 | 4.80 | 4.00      | 3.18 | 4.03 | 3.33 | 4.82 | 4.18      | 3.52 | 4.11 | 3.29 | 4.83 |

> Scores are on a 1–5 scale. CogPrompt consistently outperforms baselines across all datasets and dimensions, demonstrating improvements in both accuracy and personalized instructional alignment.

### Key Observations

- **Personalization:** CogPrompt achieves the highest personalization scores, confirming the value of integrating learner cognitive states with structured knowledge.
- **Instructional Quality:** Pedagogy, Engagement, and Supportiveness metrics indicate CogPrompt produces more structured and supportive tutoring guidance.
- **Baselines:** LLM+CDM improves over LLM-only by adding cognitive awareness, but without graph-based reasoning it is less effective in aligning feedback with concept dependencies.