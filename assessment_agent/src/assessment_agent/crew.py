from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.skills import discover_skills, activate_skill
import os, yaml 
from pathlib import Path

from pydantic import BaseModel, Field, conint
from typing import List, Literal

class ScoreItem(BaseModel):
    sub_capability: str
    score: conint(ge=1, le=10)
    # Existing fields (keep as-is)
    justification: str = Field(
        ...,
        description="Short scoring justification from scoring agent"
    )
    evidence: List[str]

class ScoreBlock(BaseModel):
    focus_area: str
    trait: str
    scores: List[ScoreItem]

@CrewBase
class AssessmentAgent():
    """AssessmentAgent crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    config_folder = "src/assessment_agent/config/"
    skills = [activate_skill(s) for s in discover_skills(Path("src/skills"))]
    
    @agent
    def researcher(self) -> Agent:

        return Agent(
            config=self.agents_config['scoring_agent'],  
            system_prompt = open(os.path.join(self.config_folder, 'custom_raw_scoring_agent_prompt_overwrite.md')).read(),
            skills = self.skills,
            verbose=True
        )

    @agent
    def justification_agent(self) -> Agent:

        return Agent(
            config=self.agents_config['justification_agent'],
            verbose=True
        )

    def build_scoring_tasks(self): 

        scoring_task_list = ['functional_governance_accurate']
        for f in scoring_task_list:
            scoring_ref_file_name = os.path.join(self.config_folder,f"raw_scoring_{f}.md")

            score_task = Task(name = f"Scoring Task: {f}", 
                               agent = self.agents[0], 
                              description = open(scoring_ref_file_name).read(),
                              expected_output = "Structured JSON with scores, justification, confidence, and evidence for each sub-capability",
                              output_json=ScoreBlock,
                           )

            self.tasks.append(score_task) 

            justification_ref_file_name = os.path.join(self.config_folder,f"raw_justification_task.md")

            justification_task = Task(name = f"Justification Task: {f}", 
                                    agent = self.agents[1], 
                                    description = open(justification_ref_file_name).read(),
                                    expected_output = "Structured Markdown justification with no additional commentary or JSON.",
                                    markdown=True, output_file = f"output/raw_scoring_justification_{f}.md",
                                    context = [score_task])

            self.tasks.append(justification_task) 
        

    @crew
    def crew(self) -> Crew:
        """Creates the AssessmentAgent crew"""
        self.build_scoring_tasks()
        print(self.agents)
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
            tracing=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
