from agency_swarm import Agency
from ProjectManager.ProjectManager import ProjectManager
from Designer.Designer import Designer
from WebDeveloper.WebDeveloper import WebDeveloper
from Copywriter.Copywriter import Copywriter

# Initialize agents
project_manager = ProjectManager()
designer = Designer()
web_developer = WebDeveloper()
copywriter = Copywriter()

# Create agency with communication flows
agency = Agency(
    [
        project_manager,  # Project Manager is the entry point for communication with the user
        [project_manager, designer],  # Project Manager can communicate with Designer
        [project_manager, web_developer],  # Project Manager can communicate with Web Developer
        [project_manager, copywriter],  # Project Manager can communicate with Copywriter
        [designer, web_developer],  # Designer can communicate with Web Developer
        [designer, copywriter],  # Designer can communicate with Copywriter
        [web_developer, designer],  # Web Developer can communicate with Designer for reviews
    ],
    shared_instructions="agency_manifesto.md",  # Shared instructions for all agents
    temperature=0.7,  # Slightly higher temperature for more creative responses
    max_prompt_tokens=4000  # Maximum tokens in conversation history
)

if __name__ == "__main__":
    agency.demo_gradio()  # Run the agency in demo mode in terminal 