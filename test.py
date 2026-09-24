from main import search_company, extract_fields, qualify_lead
seed_list = [
    "Microsoft",
    "Tesla, Inc.",
    "Netflix",
    "Nike, Inc.",
    "Spotify",
    "Zoom (software)",
    "Etsy"
]

for name in seed_list:
    result = search_company(name)
    if result:
        fields = extract_fields(result['summary'])
        print(f"--- {name} ---")
        print(f"Summary: {result['summary'][:150]}...")
        print(f"Extracted: {fields}")
        leads = qualify_lead(fields)
        print(leads)
        # print(f"Score: {leads['score']}")
        # print(f"Status: {leads['status']}")
        # print(f"Reseans: {leads['reasons']}")
    else:
        print(f"--- {name}: no data found ---\n")




