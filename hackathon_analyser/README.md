# AI Crew for analysing devpost winner projects
## Introduction
This project demonstrates the use of the CrewAI framework to automate the analysis of prioject and a quick summary to understand what is common in this projects. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

By [@mikatux](https://github.com/miktaux)

- [CrewAI Framework](#crewai-framework)
- [Running the script](#running-the-script)
- [Details & Explanation](#details--explanation)
- [License](#license)

## CrewAI Framework
[CrewAI](https://github.com/crewAIInc/crewAI) is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to analyse the winning project, associate some tags to each and create a summary.

## Running the Script
It uses gemini-flash by default so you should have access to that to run it.

***Disclaimer:** This will use gemini-flash unless you change it to use a different model, and by doing so it can be ran at no cost on the free tier.*

- **Install Dependencies**: Install [CrewAI](https://github.com/crewAIInc/crewAI?tab=readme-ov-file#1-installation) and run `crewai install`.
- **Configure Environment**: Copy `.env.example` and set up the environment variables for [Gemini](https://aistudio.google.com/app/apikey).
- **Customize**: Modify `src/hackathon_analyser/main.py` to add custom inputs for your agents and tasks.
- **Customize Further**: Check `src/hackathon_analyser/project_analysis` to update your agents and `src/hackathon_analyser/synthesizer` to update your tasks.
- **Execute the Script**: Run `crewai kickoff` and check the output 🪄.

## Details & Explanation
- **Running the Script**: Execute `crewai kickoff`. The script will leverage the CrewAI framework to analyse the last 10 winning projects.
- **Key Components**:
  - `src/hackathon_analyser/main.py`: Main script file.
  - `src/hackathon_analyser/project_analysis/crew.py`: The crew that analyse project one by one to give some tag, complexity etc...
  - `src/hackathon_analyser/synthesizer/crew.yaml`: The crew that analyse all the projects information to give a summary to the user

## License
This project is released under the MIT License.