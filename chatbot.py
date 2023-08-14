import openai
from typing import Dict
from utils import load_config
from exceptions import OpenAIRequestError, OpenAIResponseError


class ChatBot:
    """
    Chatbot class that communicates with the OpenAI API.
    """

    def __init__(self, api_key: str, model: str):
        """
        Initialize the ChatBot with the given API key and model.

        Args:
            api_key (str): The OpenAI API key.
            model (str): The model to use for the chat.
        """
        self.api_key = api_key
        self.api_model = model
        openai.api_key = self.api_key
        self.chatgpt = openai.ChatCompletion.create(
            model=self.api_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}
            ],
        )

    def get_usage(self) -> Dict[str, int]:
        """
        Get the usage information for the API key.

        Returns:
            dict: The usage information.

        Raises:
            OpenAIRequestError: If there is an error in the API request.
            OpenAIResponseError: If there is an error in the API response.
        """
        try:
            usage = openai.Usage.retrieve()
        except Exception as e:
            raise OpenAIRequestError(f"Error in API request: {str(e)}")

        if 'usage' not in usage:
            raise OpenAIResponseError("Missing 'usage' in API response")

        return usage['usage']

    def send_message(self, message: str) -> Dict[str, str]:
        """
        Send a message to the chatbot and get a response.

        Args:
            message (str): The message to send.

        Returns:
            dict: The chatbot's response.

        Raises:
            OpenAIRequestError: If there is an error in the API request.
            OpenAIResponseError: If there is an error in the API response.
        """
        if not message:
            raise ValueError('Message cannot be empty')
        
        try:
            response = openai.ChatCompletion.create(
                model=self.api_model,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
        except Exception as e:
            raise OpenAIRequestError(f"Error in API request: {str(e)}")

        if 'choices' not in response or not response['choices'] or 'message' not in response['choices'][0] or 'content' not in response['choices'][0]['message']:
            raise OpenAIResponseError(
                "Missing 'choices' or 'message' or 'content' in API response")

        return response['choices'][0]['message']['content']
