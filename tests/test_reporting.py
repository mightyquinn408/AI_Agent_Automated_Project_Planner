import json
from datetime import UTC, datetime

from project_planning_crew.models import Milestone, PlannedTask, ProjectPlan
from project_planning_crew.reporting import SCHEMA_VERSION, write_reports


def sample_plan() -> ProjectPlan:
    return ProjectPlan(
        tasks=[
            PlannedTask(
                task_name="Create wireframes",
                description="Design responsive page wireframes.",
                estimated_time_hours=16,
                assigned_team_members=["Bob Smith"],
                dependencies=[],
                start_day=1,
                end_day=2,
                allocation_rationale="Bob is the team's designer.",
            ),
            PlannedTask(
                task_name="Build pages",
                description="Implement the approved page designs.",
                estimated_time_hours=24,
                assigned_team_members=["Jane Doe"],
                dependencies=["Create wireframes"],
                start_day=3,
                end_day=6,
                allocation_rationale="Jane is the software engineer.",
            ),
        ],
        milestones=[
            Milestone(milestone_name="Design ready", tasks=["Create wireframes"]),
        ],
        risks=["Stakeholder review may take longer than expected."],
    )


def test_reports_include_markdown_and_client_json(tmp_path) -> None:
    inputs = {
        "project_type": "Website",
        "project_objectives": "Create a website for a small business",
        "industry": "Technology",
        "team_members": "- John Doe (Project Manager)\n- Jane Doe (Software Engineer)",
        "project_requirements": "- Create a responsive design\n- Optimize for search engines",
    }
    generated_at = datetime(2026, 10, 21, 17, 46, tzinfo=UTC)

    reports = write_reports(sample_plan(), inputs, tmp_path, generated_at)

    assert reports.markdown == tmp_path / "project_plan.md"
    assert reports.json == tmp_path / "project_plan.json"
    markdown = reports.markdown.read_text(encoding="utf-8")
    assert "# Website project plan" in markdown
    assert "Create wireframes" in markdown
    assert "Bob Smith" in markdown
    assert "Jane is the software engineer." in markdown
    assert "Design ready" in markdown
    assert "Stakeholder review may take longer than expected." in markdown
    assert "- Estimated hours: 40" in markdown

    document = json.loads(reports.json.read_text(encoding="utf-8"))
    assert list(document) == ["schema_version", "generated_at", "project", "plan"]
    assert document["schema_version"] == SCHEMA_VERSION == "1.0"
    assert document["generated_at"] == "2026-10-21T17:46:00Z"
    assert document["project"]["team_members"] == [
        "John Doe (Project Manager)",
        "Jane Doe (Software Engineer)",
    ]
    assert document["project"]["project_requirements"] == [
        "Create a responsive design",
        "Optimize for search engines",
    ]
    validated = ProjectPlan.model_validate(document["plan"])
    assert [task.task_name for task in validated.tasks] == [
        "Create wireframes",
        "Build pages",
    ]
    assert reports.json.read_text(encoding="utf-8").startswith("{\n  ")
