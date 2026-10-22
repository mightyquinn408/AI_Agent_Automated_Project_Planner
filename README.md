# Project Planning Crew

A modern CrewAI version of the DeepLearning.AI lesson **Automated Project:
Planning, Estimation, and Allocation**. Three agents turn a project brief into a
validated plan:

1. a project planner creates the task breakdown;
2. an estimation analyst estimates effort and risk;
3. a resource strategist schedules work and assigns the supplied team.

The final task returns a Pydantic `ProjectPlan`. Each run writes that result
as a Markdown report and a versioned JSON document.

## Requirements

- `uv`
- Python 3.10–3.13 (the included `.python-version` selects Python 3.13)
- an OpenAI API key

Install the locked dependencies:

```bash
uv sync
```

Copy the environment template and add your key:

```bash
cp .env.example .env
```

Never commit `.env`.

## Run

Run the included mobile-app planning example:

```bash
uv run crewai run
```

The same entry point can be invoked directly:

```bash
uv run project_planning_crew
```

Crew execution makes paid OpenAI API requests. The example uses
`openai/gpt-4o-mini`, configured in
`src/project_planning_crew/config/agents.yaml`.

## Customize

- Edit `example_inputs()` in `src/project_planning_crew/main.py` to supply a
  different project type, objective, industry, team, or requirements.
- Edit `src/project_planning_crew/config/agents.yaml` to change agent behavior
  or models.
- Edit `src/project_planning_crew/config/tasks.yaml` to change the workflow
  instructions.
- Edit `src/project_planning_crew/models.py` when the structured result needs a
  different contract.

## Outputs

A successful run overwrites these files:

- `outputs/project_plan.md` is the readable report, including totals, tasks,
  assignments, dependencies, allocation rationale, milestones, and risks.
- `outputs/project_plan.json` is the client contract. It is UTF-8 JSON with
  two-space indentation and this stable shape:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-10-21T17:46:00Z",
  "project": {
    "project_type": "Cross-platform mobile app",
    "project_objectives": "Build a full-featured iOS client for this planning crew",
    "industry": "Technology",
    "team_members": ["Jane Doe (Software Engineer)"],
    "project_requirements": ["Load the plan from JSON shipped in the app"]
  },
  "plan": {
    "tasks": [],
    "milestones": [],
    "risks": []
  }
}
```

`generated_at` is UTC. Team members and requirements are arrays normalized from
the multiline crew inputs. `plan` contains the validated tasks, milestones, and
risks. Clients should branch on `schema_version` instead of parsing the
Markdown file.

## Deploy to CrewAI AMP

This is a classic CrewAI project: `[tool.crewai] type = "crew"`, a committed
`uv.lock`, `@CrewBase` in `src/project_planning_crew/crew.py`, and `run()` in
`src/project_planning_crew/main.py`.

Check the project locally before deploying:

```bash
uv run crewai deploy validate
```

`run()` accepts the five project inputs used by the YAML configuration. When
they are omitted, it uses the included website example. Its return value is
the same versioned JSON document written to `outputs/project_plan.json`, which
is what an AMP execution returns to an API client.

Deploy from this directory after authenticating:

```bash
crewai login
crewai deploy create
```

Add `OPENAI_API_KEY` to the deployment's environment variables. Keep the key
out of git. The local `.env` file is used by `crewai deploy create` to offer
that variable, but it is not part of the repository.

## Development

Run the offline checks:

```bash
uv run ruff check .
uv run pytest
```

These tests validate configuration, schema behavior, and crew wiring without
calling an LLM.

## Course notebook

The original download was valid Jupyter notebook JSON saved with a `.json`
extension. It is retained as `notebooks/L_1-2.ipynb` for lesson context and
historical outputs. The notebook uses the older CrewAI 0.75 API; the runnable
application is the package under `src/`.
