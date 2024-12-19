import requests
import json
from .llm_interface import LLMInterface

class OllamaInterface(LLMInterface):
    """
    Eine LLM-Implementierung für Ollama.
    """
    def __init__(self, model_name="llama3-groq-tool-use", base_url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.base_url = base_url

    def generate_response(self, prompt: str) -> str:
        """
        Sendet einen Prompt an die Ollama API und gibt die Antwort zurück.
        """
        payload = {"model": self.model_name, "prompt": prompt}
        try:
            response = requests.post(self.base_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), stream=True)
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        json_object = json.loads(line.decode('utf-8'))
                        full_response += json_object.get('response', '')
                return full_response.strip()
            else:
                raise Exception(f"Ollama API Fehler: {response.status_code} - {response.text}")
        except Exception as e:
            return f"Fehler bei der Ollama-Anfrage: {e}"
