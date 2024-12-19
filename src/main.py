from llm import ollama_interface
from agents import CoordinatorAgent

USER_REQUEST = "Instead of printing, the ev.py should use logging. Change it to use proper python logging!"

if __name__ == '__main__':

    llm_interface = ollama_interface.OllamaInterface()
    coordinator = CoordinatorAgent.CoordinatorAgent(USER_REQUEST, llm_interface)
    coordinator.run()