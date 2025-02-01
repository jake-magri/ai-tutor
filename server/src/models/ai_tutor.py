import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables from a .env file
load_dotenv()

class AITutor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided either as a parameter or via the OPENAI_API_KEY environment variable.")

        self.client = ChatOpenAI(openai_api_key=self.api_key)

        def get_session_history():
            return []

        self.chain = RunnableWithMessageHistory(llm=self.client, runnable=self.client, get_session_history=get_session_history)

    def start_conversation(self, user_input: str) -> str:
        response = self.chain.invoke(input=user_input)
        return response

if __name__ == '__main__':
    tutor = AITutor()
    test_prompt = "Hello, how do I solve this math problem?"
    print("User:", test_prompt)
    print("Tutor:", tutor.start_conversation(test_prompt))