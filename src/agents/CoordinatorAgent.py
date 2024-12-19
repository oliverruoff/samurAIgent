import json

from .BaseAgent import BaseAgent

class CoordinatorAgent(BaseAgent):
    """
    CoordinatorAgent is a specific implementation of BaseAgent that
    initializes with predefined attributes, acting as a coordinator among multiple agents.
    """

    def __init__(self, llm_interface, user_request, list_of_agents):
        super().__init__(
            id=0,
            name="Coordinator",
            expected_input="",
            output="{\"agent_id_to_address\":\"\", \"instructions\":\"<text>\"}",
            description="Coordinates input and output flows among multiple agents.",
            prompt=f"""You're are a coordinator agent of a IT development agent team. This is the list of agents: [ $$agents ].
                      The context is a code repository that the user wants to be modified or created.
                      Your most important goal is to solve the user request, which is the following: [ $$request ].
                      This is the chat between the agents so far: [ $$chat ]
                      Based on the request and the agents list and their expected inputs and the chat so far, you chose the next agent and 
                      provide precise instructions. Make the instructions for the next agent as good as possible. 
                      Build up the project step by step, think exactly about what a specific agent can achieve. For example an analyzer agent
                      cannot implement something. Use the agents as their description suggests it.
                      You answer as json dictionary, in format [ $$output ],
                      you don't answer anything else.
                      When you think the user requirement is fullfilled, or based on the chat history you make no progress, answer only with the word "STOP".
            """,
            chat = [],
            llm_interface = llm_interface
        )
        self.user_request = user_request
        self.list_of_agents = list_of_agents
        

    def prepare_prompt(self):
        self.prompt = self.prompt.replace("$$agents", json.dumps([agent.get_info() for agent in self.list_of_agents if agent != None]))
        self.prompt = self.prompt.replace("$$request", self.user_request)
        self.prompt = self.prompt.replace("$$chat", json.dumps(self.chat))
        self.prompt = self.prompt.replace("$$output", self.output)
        return self.prompt

    def run(self, instructions):
        """
        The CoordinatorAgent processes input data and coordinates multiple tasks or agents.
        
        :return: Coordinated result.
        """
        response = ""
        while response != "STOP":
            prompt = self.prepare_prompt()

            response = self.llm_interface.generate_response(prompt)
            self.add_chat_message(self.id, self.name, response)

            parsed_response = json.loads(response)
            next_agent_id = int(parsed_response["agent_id_to_address"])
            next_agent = self.list_of_agents[next_agent_id]
            instructions = parsed_response["instructions"]

            agent_response = next_agent.run(instructions)
            self.add_chat_message(next_agent.id, next_agent.name, agent_response)


            print("Done.")
