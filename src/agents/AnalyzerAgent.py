from .BaseAgent import BaseAgent

class AnalyzerAgent(BaseAgent):
    """
    AnalyzerAgent is a specific implementation of BaseAgent that
    initializes with predefined attributes, acting as a analyzer among multiple agents.
    """

    def __init__(self, llm_interface):
        super().__init__(
            id=1,
            name="Analyzer",
            expected_input="{\"instructions\":\"\"}",
            output="",
            description="Analyzes an existing project and precisely lists the files that have to be modified or created to fullfill a user requirement.",
            prompt="""You're are an analyzer agent of a IT development agent team. 
                      There is a project, consisting of the following files: [ /.gitignore, /prints/printing.py, /ev.py, README.md ].
                      Based on these instructions: [ $$instructions ] you prepare your output, exactly showing which files would have to be modified and which files would have to be created (in case).
                      Precisely provide the file paths etc. and exactly explain what would have to be done and where. Don't come up with things.
            """,
            chat = [],
            llm_interface = llm_interface
        )

    def prepare_prompt(self, instructions):
        self.prompt = self.prompt.replace("$$instructions", instructions)
        return self.prompt

    def run(self, instructions):
        """
        The AnalyzerAgent processes input data and coordinates multiple tasks or agents.
        
        :return: Coordinated result.
        """
        prompt = self.prepare_prompt(instructions)
        response = self.llm_interface.generate_response(prompt)
        return response
