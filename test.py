from main import client

def ask_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        print(response)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

ask_llm("what's 2+2?")