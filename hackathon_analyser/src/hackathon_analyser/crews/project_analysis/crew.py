from typing import List
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field

class Project(BaseModel):
    title: str = Field(..., description="The title of the project.")
    date: str = Field(..., description="The date of the project.")
    summary: str = Field(..., description="The short summary of the project.")
    like: int = Field(..., description="The number of likes the project has.")
    url: str = Field(..., description="The URL of the project.")
    complexity: int = Field(...,le=10,ge=0, description="A score for the complexity to build of the project (0-10).")
    tags: List[str] = Field(..., description="Tags of the project (eg. Website, Mobile app, AI Agent, ...).")
    
@CrewBase
class ProjectAnalysis():
	"""Contact Analylis crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	@agent
	def project_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['project_analyst'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
		)
  
	@task
	def summarise_project(self) -> Task:
		return Task(
			config=self.tasks_config['summarise_project'],
			agent=self.project_analyst(),
     		output_pydantic=Project,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Contact Analylis crew"""
		print('OK')
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			verbose=False,
   			memory=False
		)
