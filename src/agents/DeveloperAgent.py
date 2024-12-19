import os

class DeveloperAgent():
    def __init__(self, user_request, llm_interface ):
        self.id = 2
        self.name = "Developer"
        self.user_request = user_request
        self.llm_interface = llm_interface
        self.prompt = """
                        This is the user request: [ $$user_request ].
                        This is the content of an existing code file that needs to be changed so that the user requirement is fulfilled: [ $$content ].
                        This is what you did so far: [ $$context ]
                        Respond with the full code that this content has to be replaced with. Only respond with runnable code, don't reply anything else. 
                      """

    def run(self, files_to_touch):
        project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_project")
        context = ""
        summary = []

        for file_meta in files_to_touch:
            # Normalize the file name by removing any leading slashes or backslashes
            normalized_filename = file_meta["fileName"].lstrip("\\/")

            file_path = os.path.join(project_path, normalized_filename)

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # If file exists, load content; otherwise, start with empty string
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
            else:
                content = ""

            # Prepare prompt
            prompt = self.prompt.replace("$$user_request", self.user_request)
            prompt = prompt.replace("$$content", content)
            prompt = prompt.replace("$$context", context)

            # Get new content from LLM
            new_content = self.llm_interface.generate_response(prompt)

            # Overwrite/create the file with new content
            with open(file_path, "w") as file:
                file.write(new_content)
            
            summary_entry = f"Modified/Created file: {file_meta['fileName']}"
            summary.append(summary_entry)
            print(summary_entry)

            # Update context to include changes for subsequent files
            context += f"\nModified File {file_meta['fileName']} with following content: {file_meta['reason']}\n{new_content}"
        return "\n".join(summary)
