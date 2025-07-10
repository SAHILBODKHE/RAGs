import requests
import json
import time

API_URL = "http://localhost:8000/generate-sql/"
USER_ID = "abc-123"

test_queries = [
    "Show my upcoming premium payments due in the next 30 days",
    "List all my dental claims with procedure codes from the last 2 years",
    "What's my remaining drug coverage limit for this year?",
    "Show all claims that are still pending approval",
    "List all hospital visits where the admission was in 2023 but claims weren't submitted until 2024",
    "Show my vision coverage details and used amounts",
    "Find all claims where the approved amount was less than 80% of claimed amount",
    "List my policies that will expire in the next 3 months",
    "Show my highest value claim in each category (drug, dental, vision, hospital)",
    "List all communications sent to me about claim denials in the last year",
    "Show my monthly premium payment history for my active policies",
    "Find all pre-authorization requests that were approved after the service date",
    "List claims that were submitted more than 30 days after the service date",
    "Show my provider's plan details including all coverage limits",
    "List all documents I've uploaded for claims in the last 6 months"
]

results = []

for idx, query in enumerate(test_queries, 1):
    payload = {
        "user_input": query,
        "user_id": USER_ID
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Query {idx}: {query}\n{result['sql']}\n")
        results.append({
            "query": query,
            "result": result
        })
    except Exception as e:
        print(f"❌ Query {idx} failed: {query}\nError: {str(e)}\n")
        results.append({
            "query": query,
            "error": str(e)
        })
    time.sleep(0.5)  # optional delay between requests

# Save all results
with open("query_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n📝 All queries executed. Results saved to 'query_results.json'")