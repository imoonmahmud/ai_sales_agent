import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
        api_key=os.getenv('GROQ_API_KEY'))

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

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def search_company(name):
    return {
        'name': name,
        'industry': 'Technology',
        'employees': 180000,
        'website': 'https://www.google.com',
        'headquarters': 'Mountain View, California',
        'founded': 1998
    }

def run_agent(goal):
    company_info = None

    while True:
        if company_info is None:
            print("Agent: I don't have company info yet. Searching...")
            company_info = search_company(goal)
            print(f"Agent: Got it -> {company_info}")
        else:
            print("Agent: I have enough info. Summarizing...")
            summary = ask_llm(f"Summarize this company info in one sentence: {company_info}")
            print(f"Agent: {summary}")
            break

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
                    model="openai/gpt-oss-120b",
                    tools=tools,
                    messages=messages
                )
        
        message = response.choices[0].message

        if message.tool_calls:
            call = message.tool_calls[0]
            args = json.loads(call.function.arguments)

            # run the real function
            result = search_company(**args)

            # tell the model what is asked for
            messages.append(message)

            # what is got back
            messages.append({
                'role': 'tool',
                'tool_call_id': call.id,
                'content': json.dumps(result)
            })


            # ask again with the real data available
            final_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                tools=tools,
                messages=messages
            )
            print(final_response.choices[0].message.content)
        else:
            print(f"No too needed. Answer: {message.content}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    ask_llm_with_tools('Look up information on Google')