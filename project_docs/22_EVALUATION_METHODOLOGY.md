# 22. Evaluation Methodology

## 22.1 Objective
Evaluate whether sequence-level reconstruction adds value beyond analyzing individual events independently.

## 22.2 Dataset
Use only the documented synthetic scenario set initially. Store scenario labels and expected indicators separately from agent inputs to avoid label leakage.

## 22.3 Baselines
Implement at least:
- **Single-event baseline:** evaluate each event independently and aggregate without temporal relations.
- **Sequence-aware ScamTrace:** uses timeline/graph/agent investigation.
- Optional rules-only vs LLM-assisted comparison if both modes are implemented.

## 22.4 Metrics
- Precision
- Recall
- F1
- False-positive rate
- Confusion matrix
- Scenario-level detection rate
- Evidence-reference validity rate
- Insufficient-evidence handling rate
- Runtime per case (optional)

Do not treat synthetic dataset metrics as real-world deployment performance.

## 22.5 Ablation
Where feasible, compare:
- without timeline agent
- without temporal graph
- without evidence quality/conflict resolver
- full workflow

## 22.6 User Comprehension
Optional small usability study with consent:
- Can participants identify why the warning appeared?
- Can they distinguish observed facts from inference?
- Can they identify the safe next step?
Do not collect sensitive payment data. Follow supervisor/institution requirements.

## 22.7 Reproducibility
Record dataset version, configuration, seed, mode, command, and output file. Provide a one-command evaluation path.
