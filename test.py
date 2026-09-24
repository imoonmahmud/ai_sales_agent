from main import search_company, extract_fileds
seed_list = [
    "Microsoft",
    "Tesla",
    "Netflix",
    "Nike",
    "Spotify",
    "Zoom (software)",
    "Etsy"
]

for name in seed_list:
    result = search_company(name)
    if result:
        fields = extract_fileds(result['summary'])
        print(f"--- {name} ---")
        print(f"Summary: {result['summary'][:150]}...")
        print(f"Extracted: {fields}")
    else:
        print(f"--- {name}: no data found ---\n")



