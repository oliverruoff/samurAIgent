from agents import CoordinatorAgent, AnalyzerAgent
from llm import ollama_interface

USER_REQUEST = "Create a interface to ChatGPT."

if __name__ == '__main__':

    # Initialize LLM interface
    llm_interface = ollama_interface.OllamaInterface()

    # Initialize agents
    analyzer_agent = AnalyzerAgent.AnalyzerAgent(llm_interface)  

    list_of_agents = [None, analyzer_agent] #add agents here - None on 0, too keep the ids correct

    print('List of agents:', list_of_agents)

    coordinator_agent = CoordinatorAgent.CoordinatorAgent(llm_interface, USER_REQUEST, list_of_agents)

    coordinator_agent.run("")