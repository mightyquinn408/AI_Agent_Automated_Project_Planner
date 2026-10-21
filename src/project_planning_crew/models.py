"""Structured output models for the project planning crew."""

from pydantic import BaseModel, Field, model_validator


class PlannedTask(BaseModel):
    """A scheduled task with an explicit assignment."""

    task_name: str = Field(description="Short, unique name for the task")
    description: str = Field(description="Detailed scope and expected deliverable")
    estimated_time_hours: float = Field(gt=0, description="Estimated effort in hours")
    assigned_team_members: list[str] = Field(
        min_length=1,
        description="Team members assigned to the task",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Names of tasks that must finish first",
    )
    start_day: int = Field(ge=1, description="Planned project day on which work starts")
    end_day: int = Field(ge=1, description="Planned project day on which work ends")
    allocation_rationale: str = Field(
        description="Why these team members are appropriate for this task"
    )

    @model_validator(mode="after")
    def end_must_not_precede_start(self) -> "PlannedTask":
        if self.end_day < self.start_day:
            raise ValueError("end_day must be greater than or equal to start_day")
        return self


class Milestone(BaseModel):
    """A named project milestone and the tasks that complete it."""

    milestone_name: str = Field(description="Name of the milestone")
    tasks: list[str] = Field(min_length=1, description="Task names included in the milestone")


class ProjectPlan(BaseModel):
    """Final structured project plan produced by the crew."""

    tasks: list[PlannedTask] = Field(min_length=1, description="Scheduled and allocated tasks")
    milestones: list[Milestone] = Field(
        min_length=1,
        description="Major project milestones",
    )
    risks: list[str] = Field(
        default_factory=list,
        description="Important estimation or delivery risks",
    )
