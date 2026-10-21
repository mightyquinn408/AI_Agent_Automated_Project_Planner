from crewai import Process

from project_planning_crew.crew import ProjectPlanningCrew
from project_planning_crew.models import ProjectPlan


def test_crew_wiring_without_llm_call(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used")

    crew = ProjectPlanningCrew().crew()

    assert crew.process == Process.sequential
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3
    assert [task.name for task in crew.tasks] == [
        "task_breakdown",
        "time_resource_estimation",
        "resource_allocation",
    ]
    assert crew.tasks[-1].output_pydantic is ProjectPlan
    assert crew.tasks[1].context == [crew.tasks[0]]
    assert crew.tasks[2].context == [crew.tasks[0], crew.tasks[1]]
