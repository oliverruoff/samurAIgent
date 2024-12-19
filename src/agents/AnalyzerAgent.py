import os

class AnalyzerAgent():

    def __init__(self, user_request, llm_interface):
        self.id = 1
        self.name = "Analyzer"
        self.user_request = user_request
        self.llm_interface = llm_interface
        self.prompt = """
                            This is the user request: [ $$user_request ].
                            This is the structure of the project the user wants to implement its requirements: \n[ $$user_project_structure ].
                            Find the files that have to be created / modified to fulfill the user requirements.
                            When you think an existing file has to be modified, take type = modify. If you think for the users request a new file has to be created,
                            take the type = create.
                            Keep the full file name, including its path, write path separators as single slashes.
                            Only answer in a json list format like: [{"fileName":"...", "type": "modify", "reason": "..."}, {"fileName":"...", "type": "create", "reason": "..."}]
                            Don't write anything else than the json. 
        """

    def _get_project_structure(self, path):
        # Walk through the project directory and build a human-readable list
        structure_lines = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                # Represent files
                relative_file_path = os.path.relpath(os.path.join(root, filename), path)
                structure_lines.append("\\"+relative_file_path)

        # Join everything into a single string
        return "\n".join(structure_lines)
        
    def run(self):
        current_file_dir = os.path.dirname(__file__)  # Directory of AnalyzerAgent.py
        project_path = os.path.abspath(os.path.join(current_file_dir, '..', 'user_project'))
        user_project_structure = self._get_project_structure(project_path)

        prompt = self.prompt.replace('$$user_request', self.user_request)
        prompt = prompt.replace('$$user_project_structure', user_project_structure)
        
        llm_response = self.llm_interface.generate_response(prompt)
        return llm_response
