import requests
from llm import ask_llm

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


def extract_fields(summary_text):
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

    response_text = ask_llm(prompt)

    fields = {}
    for line in response_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()

    return fields