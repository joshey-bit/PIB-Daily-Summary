from langchain_community.chat_models import ChatOpenAI
import os
import dotenv
from typing import Optional

dotenv.load_dotenv(dotenv_path=".env")

class ChatOpenAICustom(ChatOpenAI):
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        openai_api_key: Optional[str] = None,
        openai_api_base: str = "https://api.openai.com/v1",
        **kwargs
    ):
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        super().__init__(
            openai_api_base=openai_api_base,
            openai_api_key=openai_api_key,
            model_name=model_name,
            **kwargs
        )

def get_llm():
    return ChatOpenAICustom(model_name="gpt-4o-mini")

llm = get_llm()
