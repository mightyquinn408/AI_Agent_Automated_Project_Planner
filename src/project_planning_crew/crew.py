"""Crew definition for project planning, estimation, and allocation."""

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from project_planning_crew.models import ProjectPlan


@CrewBase
class ProjectPlanningCrew:
    """Coordinate three specialists to produce a structured project plan."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def project_planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_planning_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def estimation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["estimation_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def resource_allocation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resource_allocation_agent"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def task_breakdown(self) -> Task:
        return Task(
            config=self.tasks_config["task_breakdown"],  # type: ignore[index]
            agent=self.project_planning_agent(),
        )

    @task
    def time_resource_estimation(self) -> Task:
        return Task(
            config=self.tasks_config["time_resource_estimation"],  # type: ignore[index]
            agent=self.estimation_agent(),
            context=[self.task_breakdown()],
        )

    @task
    def resource_allocation(self) -> Task:
        return Task(
            config=self.tasks_config["resource_allocation"],  # type: ignore[index]
            agent=self.resource_allocation_agent(),
            context=[self.task_breakdown(), self.time_resource_estimation()],
            output_pydantic=ProjectPlan,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
