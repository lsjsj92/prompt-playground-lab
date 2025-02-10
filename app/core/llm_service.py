import os
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION
)

# OpenAI 설정 (LangChain)
def get_openai_llm(model_name):
    return ChatOpenAI(model=model_name)

# Azure OpenAI 설정 (LangChain)
def get_azure_llm(model_name):
    return AzureChatOpenAI(
        azure_deployment=model_name,
        api_version=AZURE_OPENAI_API_VERSION
    )

# OpenAI API 호출 함수
def call_llm_api(api_provider: str, model_name: str, system_message: str, user_message: str):
    if api_provider == "OpenAI":
        llm = get_openai_llm(model_name)
    elif api_provider == "Azure OpenAI":
        llm = get_azure_llm(model_name)
    else:
        raise ValueError(f"지원하지 않는 API 제공자: {api_provider}")

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ]
    result = llm.invoke(messages)
    token_info = result.response_metadata["token_usage"]

    return {
        "llm_result": result.content,
        "llm_token_info": {
            "completion_tokens": token_info["completion_tokens"],
            "prompt_tokens": token_info["prompt_tokens"],
            "total_tokens": token_info["total_tokens"]
        }
    }
