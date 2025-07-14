from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()


class AgentModelConfig(BaseModel):
    """
    Configuration model for an individual AI agent.

    Attributes:
        model (str): The model name (e.g., gpt-4, gpt-3.5-turbo).
        temperature (float): Sampling temperature for generation.
        max_tokens (int): Maximum tokens allowed in the response.
    """
    model: Literal["gpt-3.5-turbo", "gpt-4"]
    temperature: float = Field(..., ge=0.0, le=1.0)
    max_tokens: int = Field(..., gt=0)

class Settings(BaseSettings):
    """
    Global settings for the TestMind backend system.

    Includes structured model configuration for all agents.
    """

    conversation_agent: AgentModelConfig = Field(
        default=AgentModelConfig(
            model="gpt-4",
            temperature=0.8,
            max_tokens=1500
        ),
        description="Configuration for the conversation agent"
    )

    question_agent: AgentModelConfig = Field(
        default=AgentModelConfig(
            model="gpt-3.5-turbo",
            temperature=0.0,
            max_tokens=1000
        ),
        description="Configuration for the question agent"
    )

    answer_agent: AgentModelConfig = Field(
        default=AgentModelConfig(
            model="gpt-4",
            temperature=0.3,
            max_tokens=2000
        ),
        description="Configuration for the answer agent"
    )

    report_agent: AgentModelConfig = Field(
        default=AgentModelConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=1500
        ),
        description="Configuration for the report agent"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"


# === Singleton Instance ===

@lru_cache
def get_settings() -> Settings:
    """
    Get the singleton settings instance.

    Returns:
        Settings: The application configuration settings object.
    """
    return Settings()

@lru_cache
def get_api_key() -> str | None:
    """
    Get the OpenAI API key from environment variables.

    This function retrieves the OpenAI API key from the system environment
    variables. The API key is required for authenticating with OpenAI's
    services to use their language models (GPT-3.5-turbo, GPT-4, etc.)
    in the TestMind workflow.

    Returns:
        str | None: The OpenAI API key if found in environment variables,
                    None if the API key is not set.
    """
    return os.getenv("OPENAI_API_KEY")