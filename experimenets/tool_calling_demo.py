import json
from llm import client
from research import search_company

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_company",
            "description": "Search for basic information about a company by its name. Use this tool when you need information about a company such as its industry, employee count, website, headquarters, or founding year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the company to search for."
                    }
                },
                "required": ["name"]
            }
        }
    }
]


def ask_llm_with_tools(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", tools=tools, messages=messages
        )
        message = response.choices[0].message
        if message.tool_calls:
            call = message.tool_calls[0]
            args = json.loads(call.function.arguments)
            result = search_company(**args)
            messages.append(message)
            messages.append({
                'role': 'tool', 'tool_call_id': call.id, 'content': json.dumps(result)
            })
            final_response = client.chat.completions.create(
                model="openai/gpt-oss-120b", tools=tools, messages=messages
            )
            print(final_response.choices[0].message.content)
        else:
            print(f"No tool needed. Answer: {message.content}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    ask_llm_with_tools('Look up information on Google')