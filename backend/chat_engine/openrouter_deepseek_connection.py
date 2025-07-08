from langchain_community.chat_models import ChatOpenAI
import os
import getpass
import dotenv
from pydantic import SecretStr

# %%
#get from .env file
dotenv.load_dotenv(dotenv_path=".env")

# %%
from typing import Optional

class ChatOpenRouter(ChatOpenAI):
    def __init__(
        self,
        model_name: str,
        openai_api_key: Optional[str] = None,
        openai_api_base: str = "https://openrouter.ai/api/v1",
        **kwargs
    ):
        openai_api_key = openai_api_key or os.getenv("OPENROUTER_API_KEY")
        super().__init__(
            openai_api_base=openai_api_base,
            openai_api_key=openai_api_key,
            model_name=model_name,
            **kwargs
        )


def get_llm():
    return ChatOpenRouter(model_name="deepseek/deepseek-chat-v3-0324:free")

llm = get_llm()
