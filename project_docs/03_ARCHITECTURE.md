# 3. System Architecture

## 3.1 High-Level Architecture

```text
                         UPI SCAMTRACE
                              |
                    +---------v---------+
                    |   Streamlit UI    |
                    | Dashboard / Cases |
                    +---------+---------+
                              |
                    +---------v---------+
                    | Application Core  |
                    | Services / Config |
                    +---------+---------+
                              |
                    +---------v---------+
                    |     LangGraph     |
                    | Agent Orchestration|
                    +---------+---------+
                              |
       +----------------------+----------------------+
       |          |           |          |         |
       v          v           v          v         v
   Message     Link/QR     Payment    Timeline   Normalizer
   Agent       Agent       Agent      Agent      Agent
       \          |           |          |         /
        +---------+-----------+----------+--------+
                              |
                    +---------v---------+
                    | Journey Investigator|
                    +---------+---------+
                              |
                    +---------v---------+
                    | Evidence Quality  |
                    | Conflict Resolver |
                    +---------+---------+
                              |
                    +---------v---------+
                    | Risk & Explanation|
                    +---------+---------+
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
      Temporal Evidence Graph             SQLite Store
             |                                 |
             +----------------+----------------+
                              |
                    +---------v---------+
                    | Evaluation/Export |
                    +-------------------+
```

## 3.2 Layer Responsibilities

### Streamlit UI
Presentation, case intake, visualization, controls, and user-facing explanations. No core risk logic should live in page scripts.

### Application Core
Coordinates services, configuration, validation, repositories, and error handling.

### LangGraph
Defines explicit typed state, nodes, edges, conditional paths, and persistence checkpoints if used.

### Specialist Agents
Perform bounded analysis tasks and return validated Pydantic outputs. They must reference source event IDs.

### Temporal Graph
Stores event/entity nodes and evidence-backed relations. Graph construction is deterministic where possible; model-suggested links require validation.

### Risk/Explanation Layer
Aggregates evidence, uncertainty, contradictions, and recommendations. It should not simply trust free-form LLM prose.

### SQLite
Stores cases, events, evidence, agent runs, relations, and assessments.

### Optional LLM Provider
Used for language understanding and synthesis. Offline deterministic rules remain available.

## 3.3 Separation of Concerns
Use distinct layers:
- UI
- application services
- schemas/models
- repositories/database
- parsers
- agents
- LangGraph workflow
- graph analysis
- risk aggregation
- evaluation
- optional integrations
- configuration/utilities

## 3.4 Deployment Shape
Initial target is a local Streamlit application. No cloud deployment is required for the supervisor demo. Optional deployment notes may be provided only after local behavior is verified.
