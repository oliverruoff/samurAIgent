from abc import ABC, abstractmethod
from time import ctime

class BaseAgent(ABC):
    """
    BaseAgent is an abstract base class for all agents.
    """
    def __init__(self,
                 id,
                 name,
                 expected_input,
                 output,
                 description,
                 prompt,
                 chat,
                 llm_interface
                 ):
        self.id = id
        self.name = name
        self.description = description
        self.expected_input = expected_input
        self.output = output
        self.prompt = prompt
        self.chat = chat
        self.llm_interface = llm_interface

    @abstractmethod
    def run(self, instructions):
        """
        The main logic of the agent. Must be implemented by subclasses.

        :return: The result of the agent's operation, adhering to the output format.
        """
        pass

    def prepare_prompt(self):
        """
        This replaces placeholders in the prompt.
        Has to be implemented in the inheriting classes
        """
        pass

    def get_info(self):
        """
        Returns basic information about the agent, including input and output formats.

        :return: Dictionary with agent information.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "input_format": self.expected_input
        }
    
    def add_chat_message(self, sender_id, sender_name, sender_message):
        new_message = {
            "time": ctime(),
            "id": sender_id,
            "name": sender_name,
            "message": sender_message
        }

        print("New message:\n",new_message)

        self.chat.append(new_message)