from pathlib import Path

import pytest
from crewai_cli.deploy.validate import DeployValidator

from project_planning_crew.main import example_inputs, resolve_inputs


def test_kickoff_inputs_cover_the_yaml_contract() -> None:
    assert set(example_inputs()) == {
        "project_type",
        "project_objectives",
        "industry",
        "team_members",
        "project_requirements",
    }


def test_resolve_inputs_overrides_without_changing_defaults() -> None:
    original = example_inputs()["project_type"]

    resolved = resolve_inputs({"project_type": "Mobile app"})

    assert resolved["project_type"] == "Mobile app"
    assert example_inputs()["project_type"] == original


def test_resolve_inputs_rejects_unknown_or_blank_values() -> None:
    with pytest.raises(ValueError, match="Unknown crew inputs"):
        resolve_inputs({"budget": "1000"})
    with pytest.raises(ValueError, match="cannot be blank"):
        resolve_inputs({"industry": "  "})


def test_project_passes_amp_predeploy_validation() -> None:
    project_root = Path(__file__).parents[1]
    validator = DeployValidator(project_root)

    validator.run()

    assert validator.errors == []
