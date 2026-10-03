from ollama import chat


response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "What is IPv6? Explain in one sentence."
        }
    ]
)


print(response.message.content)
