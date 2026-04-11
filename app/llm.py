import os

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI


def get_llm(
    *,
    provider: str = "google",
    model: str | None = None,
    temperature: float = 0,
):
    provider = provider or os.getenv("LLM_PROVIDER", "google")

    if provider == "google":
        return ChatGoogleGenerativeAI(
            model=model or os.getenv("LLM_MODEL", "gemini-2.5-flash"),
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    # if provider == "openai":
    #     return ChatOpenAI(
    #         model=model or os.getenv("LLM_MODEL", "gpt-4o-mini"),
    #         temperature=temperature,
    #         api_key=os.getenv("OPENAI_API_KEY"),
    #     )

    raise ValueError(f"Unsupported LLM provider: {provider}")