from typing import Type
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from exa_py import Exa
import requests
import os

class EXAAnswerToolSchema(BaseModel):
    query: str = Field(..., description="The question you want to ask Exa.")

class EXAAnswerTool(BaseTool):
    name: str = "Ask Exa a question"
    description: str = "A tool that asks Exa a question and returns the answer."
    args_schema: Type[BaseModel] = EXAAnswerToolSchema
    answer_url: str = "https://api.exa.ai/answer"
    headers: dict = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": os.getenv("EXA_API_KEY")
    }

    def _run(self, query: str):
        try:
            response = requests.post(
                self.answer_url,
                json={"query": query, "text": True},
                headers=self.headers,
            )
            response.raise_for_status() 
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Log the HTTP error
            print(f"Response content: {response.content}")  # Log the response content for more details
            raise
        except Exception as err:
            print(f"Other error occurred: {err}")  # Log any other errors
            raise

        response_data = response.json()
        answer = response_data["answer"]
        citations = response_data.get("citations", [])
        output = f"Answer: {answer}\n\n"
        if citations:
            output += "Citations:\n"
            for citation in citations:
                output += f"- {citation['title']} ({citation['url']})\n"

        return output

def create_researcher(llm_option):
    # Configure the LLM based on selection
    if llm_option == "GROQ":
        llm = LLM(
            api_key=os.getenv("GROQ_API_KEY"),
            model="groq/deepseek-r1-distill-llama-70b"
        )
    else:
        llm = LLM(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="o1"
        )

    # Create the researcher agent
    researcher = Agent(
        role='Research Analyst',
        goal='Conduct thorough research on given topics',
        backstory='Expert at analyzing and summarizing complex information',
        tools=[EXAAnswerTool()],
        llm=llm,
        verbose=True
    )
    
    return researcher

def create_research_task(researcher, task_description):
    return Task(
        description=task_description,
        expected_output="""A detailed Executive Summary of the research findings.
        The summary should be concise and focus on the most important aspects of the research.
        The format should be markdown without the "```" and include the following sections:
        - Executive Summary
        - Key Findings
        - Recommendations
        - Citations
        """,
        agent=researcher
    )

def run_research(researcher, task):
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    
    return crew.kickoff()
