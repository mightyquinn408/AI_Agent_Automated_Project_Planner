#!/usr/bin/env python
"""Command-line entry point for the project planning crew."""

from project_planning_crew.crew import ProjectPlanningCrew
from project_planning_crew.models import ProjectPlan
from project_planning_crew.reporting import write_reports


def example_inputs() -> dict[str, str]:
    """Return the example project supplied with the original course lesson."""

    return {
        "project_type": "Website",
        "project_objectives": "Create a website for a small business",
        "industry": "Technology",
        "team_members": """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
""".strip(),
        "project_requirements": """
- Create a responsive design that works well on desktop and mobile devices
- Implement a modern, visually appealing user interface with a clean look
- Develop a user-friendly navigation system with intuitive menu structure
- Include an "About Us" page highlighting the company's history and values
- Design a "Services" page showcasing the business's offerings with descriptions
- Create a "Contact Us" page with a form and integrated map for communication
- Implement a blog section for sharing industry news and company updates
- Ensure fast loading times and optimize for search engines (SEO)
- Integrate social media links and sharing capabilities
- Include a testimonials section to showcase customer feedback and build trust
""".strip(),
    }


def resolve_inputs(overrides: dict[str, str] | None = None) -> dict[str, str]:
    """Merge a kickoff payload over the example inputs."""

    resolved = example_inputs()
    if not overrides:
        return resolved
    unknown = sorted(set(overrides) - set(resolved))
    if unknown:
        raise ValueError(f"Unknown crew inputs: {', '.join(unknown)}")
    blank = sorted(key for key, value in overrides.items() if not str(value).strip())
    if blank:
        raise ValueError(f"Crew inputs cannot be blank: {', '.join(blank)}")
    resolved.update(overrides)
    return resolved


def run(inputs: dict[str, str] | None = None) -> dict[str, object]:
    """Run the crew and return the versioned client document.

    CrewAI AMP calls this function. Optional inputs override the included
    example, and the returned document is the automation result.
    """

    runtime_inputs = resolve_inputs(inputs)
    result = ProjectPlanningCrew().crew().kickoff(inputs=runtime_inputs)
    plan = result.pydantic
    if not isinstance(plan, ProjectPlan):
        raise RuntimeError("The crew did not return the expected structured ProjectPlan output")
    reports = write_reports(plan, runtime_inputs)
    print(reports.markdown)
    print(reports.json)
    return reports.document


if __name__ == "__main__":
    run()
