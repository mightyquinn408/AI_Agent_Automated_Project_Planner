"""Render a project plan as Markdown and a versioned client JSON document."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import NamedTuple

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from project_planning_crew.models import ProjectPlan

SCHEMA_VERSION = "1.0"
DEFAULT_OUTPUT_DIR = Path("outputs")


class ReportPaths(NamedTuple):
    """Files and client document produced for one crew result."""

    markdown: Path
    json: Path
    document: dict[str, object]


def normalize_lines(value: str) -> list[str]:
    """Turn a multiline prompt string into a client-friendly list."""

    items: list[str] = []
    for line in value.splitlines():
        cleaned = line.strip()
        if cleaned.startswith(("- ", "* ")):
            cleaned = cleaned[2:].strip()
        if cleaned:
            items.append(cleaned)
    return items


def client_document(
    plan: ProjectPlan,
    inputs: dict[str, str],
    generated_at: datetime | None = None,
) -> dict[str, object]:
    """Build the stable JSON contract consumed by external clients."""

    timestamp = generated_at or datetime.now(UTC)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": timestamp.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "project": {
            "project_type": inputs["project_type"],
            "project_objectives": inputs["project_objectives"],
            "industry": inputs["industry"],
            "team_members": normalize_lines(inputs["team_members"]),
            "project_requirements": normalize_lines(inputs["project_requirements"]),
        },
        "plan": plan.model_dump(mode="json"),
    }


def format_hours(value: float) -> str:
    """Render whole-hour estimates without a trailing decimal."""

    return f"{value:g}"


def render_markdown(document: dict[str, object], plan: ProjectPlan) -> str:
    """Render the human-readable report from the client document."""

    tasks = plan.tasks
    summary = {
        "task_count": len(tasks),
        "total_hours": sum(task.estimated_time_hours for task in tasks),
        "milestone_count": len(plan.milestones),
        "start_day": min(task.start_day for task in tasks),
        "end_day": max(task.end_day for task in tasks),
    }
    template_dir = Path(__file__).parent / "templates"
    environment = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["hours"] = format_hours
    return environment.get_template("project_plan.md.j2").render(
        project=document["project"],
        plan=plan,
        summary=summary,
        generated_at=document["generated_at"],
    )


def write_reports(
    plan: ProjectPlan,
    inputs: dict[str, str],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    generated_at: datetime | None = None,
) -> ReportPaths:
    """Write the Markdown report and pretty-printed client JSON document."""

    output_dir.mkdir(parents=True, exist_ok=True)
    document = client_document(plan, inputs, generated_at)
    markdown_path = output_dir / "project_plan.md"
    json_path = output_dir / "project_plan.json"
    markdown_path.write_text(render_markdown(document, plan), encoding="utf-8")
    json_path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return ReportPaths(markdown=markdown_path, json=json_path, document=document)
