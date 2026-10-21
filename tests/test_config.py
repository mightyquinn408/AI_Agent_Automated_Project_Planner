from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).parents[1] / "src" / "project_planning_crew" / "config"


def test_agent_and_task_keys() -> None:
    agents = yaml.safe_load((CONFIG_DIR / "agents.yaml").read_text())
    tasks = yaml.safe_load((CONFIG_DIR / "tasks.yaml").read_text())

    assert list(agents) == [
        "project_planning_agent",
        "estimation_agent",
        "resource_allocation_agent",
    ]
    assert list(tasks) == [
        "task_breakdown",
        "time_resource_estimation",
        "resource_allocation",
    ]


def test_all_runtime_inputs_are_used() -> None:
    config_text = "\n".join(
        path.read_text() for path in (CONFIG_DIR / "agents.yaml", CONFIG_DIR / "tasks.yaml")
    )

    for placeholder in (
        "project_type",
        "project_objectives",
        "industry",
        "team_members",
        "project_requirements",
    ):
        assert f"{{{placeholder}}}" in config_text
