import os


def generate_text(prompt, response_schema=None, temperature=0.2, max_output_tokens=500):
    """
    Generate text using the configured AI provider.

    Local development: AI_PROVIDER=ollama
    Cloud deployment: AI_PROVIDER=gemini
    """
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if provider == "ollama":
        from ollama import chat

        options = {
            "temperature": temperature,
            "num_predict": max_output_tokens,
        }

        request = {
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
            "messages": [{"role": "user", "content": prompt}],
            "options": options,
        }

        if response_schema is not None:
            request["format"] = response_schema.model_json_schema()

        response = chat(**request)
        return response.message.content.strip()

    if provider == "gemini":
        from google import genai
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your environment variables."
            )

        client = genai.Client(api_key=api_key)

        config = {
            "max_output_tokens": max_output_tokens,
        }

        if response_schema is not None:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            contents=prompt,
            config=types.GenerateContentConfig(**config),
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()

    raise ValueError(
        f"Unsupported AI_PROVIDER '{provider}'. Choose 'ollama' or 'gemini'."
    )
