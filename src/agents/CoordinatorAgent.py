import json

from agents import AnalyzerAgent, DeveloperAgent
from Utils import json_helper

class CoordinatorAgent():

    def __init__(self, user_request, llm_interface):
        self.id = 0
        self.name = "Coordinator"
        self.chat = []
        self.user_request = user_request
        self.llm_interface = llm_interface
        
    def run(self):
        # Finding out which files have to be adjusted / created
        analyzer = AnalyzerAgent.AnalyzerAgent(self.user_request, self.llm_interface)
        analyzer_response = analyzer.run()

        print('Analyzer_response:\n', analyzer_response)

        files_to_touch = json_helper.extract_json_from_text(analyzer_response)

        print("Parsed analyzer response:", files_to_touch)

        developer = DeveloperAgent.DeveloperAgent(self.user_request, self.llm_interface)
        developer_reponse = developer.run(files_to_touch)

        print('Developer Response:\n', developer_reponse)