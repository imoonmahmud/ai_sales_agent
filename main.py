import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq
from database import add_lead

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
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    headers = {
        "User-Agent": "AISalesAgentLearningProject/1.0 (your_email@example.com)"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('type') == 'disambiguation':
                print(f"'{name}' is ambiguous on Wikipedia - try a more specific name")
                return None
            else:
                return {
                    'name': data.get('title'),
                    'summary': data.get('extract'),
                    'wikipedia_url': data.get('content_urls', {}).get('desktop', {}).get('page')
                }
        elif response.status_code == 404:
            print(f"No Wikipedia page found for '{name}'")
            return None
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def extract_fileds(summary_text):
    prompt = f"""Extract the following fields from this text.
    If a field is not explicitly mentioned in the text, respond with "unknown" 
    for that field. Do not guess or use outside knowledge.

    Text: "{summary_text}"

    Fields: industry, headquarters, employee_count, founded_year

    Respond in this exact format:
    industry: ...
    headquarters: ...
    employee_count: ...
    founded_year: ..."""

    return ask_llm(prompt)

def run_agent(goal):
    company_info = None

    while True:
        if company_info is None:
            print("Agent: I don't have company info yet. Searching...")
            company_info = search_company(goal)
            add_lead(
                company_info['name'],
                company_info['industry'],
                company_info['employees'],
                company_info['website'],
                'agent_search',
                None
            )
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
    run_agent('Google')