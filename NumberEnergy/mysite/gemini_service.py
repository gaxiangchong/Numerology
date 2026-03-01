"""
Gemini API + File Search for Pro users: answer questions using the knowledge base.
Set GOOGLE_GEMINI_API_KEY (or GEMINI_API_KEY) and optionally GEMINI_FILE_SEARCH_STORE_NAME.
"""
import os

def _get_api_key():
    return os.environ.get("GOOGLE_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

def _get_store_name():
    return os.environ.get("GEMINI_FILE_SEARCH_STORE_NAME", "").strip()

def is_available():
    """Return True if Gemini can be used (API key set)."""
    return bool(_get_api_key())

def ask(question: str, number_context: str | None = None) -> str:
    """
    Ask Gemini a question, optionally with context about a number/car plate.
    Uses the configured file search store if GEMINI_FILE_SEARCH_STORE_NAME is set.
    """
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Gemini API key not configured. Set GOOGLE_GEMINI_API_KEY or GEMINI_API_KEY.")

    # Prefer explicit google.genai import (avoids conflict with other 'google' packages)
    try:
        import google.genai as genai
        from google.genai import types
    except (ImportError, ModuleNotFoundError):
        from google import genai
        from google.genai import types

    client = genai.Client(api_key=api_key)
    store_name = _get_store_name()

    # Build user message: question + optional number/plate context
    if number_context:
        contents = f"""The user has analyzed this number or car plate in our numerology app: "{number_context}"

User question: {question}

Answer based on the knowledge base (易数/numerology) and the given number context. Be concise and helpful."""
    else:
        contents = question

    try:
        if store_name:
            # Use File Search tool with knowledge base (file_search_store_names)
            try:
                tool = types.Tool(
                    file_search=types.FileSearch(file_search_store_names=[store_name])
                )
            except (AttributeError, TypeError):
                # Older SDK: FileSearchRetrievalResource(file_search_stores=[...])
                tool = types.Tool(
                    file_search=types.FileSearchRetrievalResource(
                        file_search_stores=[store_name]
                    )
                )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(tools=[tool]),
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
            )
        if response and response.text:
            return response.text.strip()
        return "No response from the model."
    finally:
        try:
            client.close()
        except Exception:
            pass
