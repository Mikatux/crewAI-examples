from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Synthesizer():
	"""Synthesizer crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	@agent
	def project_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['project_analyst'],
			verbose=True,
		)
  
	@task
	def synthesize_all(self) -> Task:
		return Task(
			config=self.tasks_config['synthesize_all'],
			agent=self.project_analyst(),
		)

	@crew
	def crew(self) -> Crew:
		"""Synthesizer crew"""
		print('OK')
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			verbose=False,
   			memory=False
		)
