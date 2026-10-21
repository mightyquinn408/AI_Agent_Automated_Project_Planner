import pytest
from pydantic import ValidationError

from project_planning_crew.models import Milestone, PlannedTask, ProjectPlan


def valid_task() -> PlannedTask:
    return PlannedTask(
        task_name="Create wireframes",
        description="Design responsive page wireframes.",
        estimated_time_hours=16,
        assigned_team_members=["Bob Smith"],
        dependencies=[],
        start_day=1,
        end_day=2,
        allocation_rationale="Bob is the team's designer.",
    )


def test_project_plan_serializes_with_pydantic_v2() -> None:
    plan = ProjectPlan(
        tasks=[valid_task()],
        milestones=[
            Milestone(
                milestone_name="Design ready",
                tasks=["Create wireframes"],
            )
        ],
        risks=["Stakeholder review may take longer than expected."],
    )

    assert plan.model_dump()["tasks"][0]["assigned_team_members"] == ["Bob Smith"]


def test_task_rejects_reverse_schedule() -> None:
    with pytest.raises(ValidationError, match="end_day"):
        PlannedTask(
            task_name="Invalid task",
            description="An invalid schedule.",
            estimated_time_hours=1,
            assigned_team_members=["Jane Doe"],
            start_day=3,
            end_day=2,
            allocation_rationale="Jane owns implementation.",
        )


def test_task_requires_positive_effort() -> None:
    payload = valid_task().model_dump()
    payload["estimated_time_hours"] = 0

    with pytest.raises(ValidationError):
        PlannedTask.model_validate(payload)
