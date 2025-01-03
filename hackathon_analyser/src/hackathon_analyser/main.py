#!/usr/bin/env python
import json
import os
from typing import List
import requests

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
from litellm import BaseModel, Field

from flask import Flask, request, jsonify
from waitress import serve
import firebase_admin
from firebase_admin import firestore

if os.environ.get('USE_FIRESTORE') == 'True':
    app = firebase_admin.initialize_app()
    db = firestore.client()


from .crews.project_analysis.crew import ProjectAnalysis
from .crews.synthesizer.crew import Synthesizer



class Project_Simple(BaseModel):
    title: str = Field(..., description="The title of the project.")
    description: str = Field(..., description="The description of the project.")
    like: int = Field(..., description="The number of likes the project has.")
    url: str = Field(..., description="The URL of the project.")

class DreamState(BaseModel):
    projects: List[Project_Simple] = []

class DreamFlow(Flow[DreamState]):

    @start()
    def get_projects(self):
        data = requests.get("https://devpost.com/software/search?query=is%3Awinner").json()
        projects_for_kickoff = []
        for project in data['software']:
            projects_for_kickoff.append({"project": project})
        # slice 10 first 
        return projects_for_kickoff[:10]

    @listen(get_projects)
    def fetch_project_information(self, projects_for_kickoff):
        project_infos = ProjectAnalysis().crew().kickoff_for_each(projects_for_kickoff)
        projects = []
        print(project_infos[0].pydantic)
        for project in project_infos:
            projects.append(project.pydantic.__dict__)
        return projects

    @listen(fetch_project_information)
    def save_contact(self, projects):
        print("Saving retreived info")
        with open("project.json", "w") as f:
            f.write(json.dumps({"projects":projects}))

    @listen(fetch_project_information)
    def synthesize_projects_list(self, projects):
        project_infos = Synthesizer().crew().kickoff(inputs={"projects": projects})
        print(project_infos)
        return project_infos

def kickoff():
    dream_flow = DreamFlow()
    dream_flow.kickoff()

def plot():
    dream_flow = DreamFlow()
    dream_flow.plot()

    
def run_http():
    serve(app, host="0.0.0.0", port=os.environ.get("PORT", 8080))

# Initialize the Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def data_handler():
    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        dream_flow = DreamFlow()
        result = dream_flow.kickoff()        
        task_id = data.get('task_id')
        if os.environ.get('USE_FIRESTORE') == 'True' and task_id:
            db.collection('Tasks').document(task_id).update({
                "postContent": result.raw,
                "status": "completed"
            })
        return result.raw, 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

  