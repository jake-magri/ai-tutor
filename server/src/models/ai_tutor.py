import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables from a .env file
load_dotenv()

class AITutor:
    def __init__(self, api_key: str = None):
        """
        Initialize the AI Tutor with the provided OpenAI API key.
        If no key is provided, it will be loaded from the environment variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided either as a parameter or via the OPENAI_API_KEY environment variable.")

        # Create a ChatOpenAI instance using the provided API key.
        # ChatOpenAI is preferred for conversational models.
        self.client = ChatOpenAI(openai_api_key=self.api_key)

        # Define a function to get session history (you may need to implement this).
        def get_session_history():
            # Implement your logic to get session history here.
            # For now, we'll use an empty list as a placeholder.
            return []

        # Initialize the conversation chain with the language model and session history.
        self.chain = RunnableWithMessageHistory(llm=self.client, runnable=self.client, get_session_history=get_session_history)

    def start_conversation(self, user_input: str) -> str:
        """
        Process the user input and return the tutor's response.
        
        Args:
            user_input (str): The input prompt from the user.
        
        Returns:
            str: The AI tutor's response.
        """
        response = self.chain.invoke(input=user_input)
        return response

# The following block is for simple local testing.
if __name__ == '__main__':
    tutor = AITutor()  # Ensure OPENAI_API_KEY is set in your .env or passed as an argument.
    test_prompt = "Hello, how do I solve this math problem?"
    print("User:", test_prompt)
    print("Tutor:", tutor.start_conversation(test_prompt))