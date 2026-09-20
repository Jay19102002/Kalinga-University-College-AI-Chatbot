import httpx
import json

BASE_API = "http://localhost:8000/api"
SESSION_ID = "live_verification_session"

TEST_QUERIES = [
    "What is the admission procedure?",
    "What entrance exam is required?",
    "What is the fee for BBA?",
    "What about MBA?",
    "Does the university provide scholarships?",
    "Which companies recruit students?",
    "What is the highest package?",
    "What are recent research papers in Computer Science?",
    "Tell me about Ideathon 6.0 event",
    "Show me patents filed by Kalinga University",
    "What is the weather tomorrow?"
]

def run_live_tests():
    print("=== LIVE FASTAPI CHATBOT & DATABASE API VERIFICATION ===")
    
    # 1. Test Database Stats
    try:
        stats_resp = httpx.get(f"{BASE_API}/database/stats")
        if stats_resp.status_code == 200:
            stats = stats_resp.json()
            print(f"[DATABASE STATS]: Total records: {stats.get('total_records')}, FTS indexed: {stats.get('fts_indexed_documents')}")
        else:
            print(f"[DATABASE STATS FAILED]: {stats_resp.status_code}")
    except Exception as e:
        print(f"Error connecting to database stats: {e}")

    # 2. Test FTS Global Search
    try:
        search_resp = httpx.get(f"{BASE_API}/database/search?q=computer")
        if search_resp.status_code == 200:
            s_data = search_resp.json()
            print(f"[DATABASE FTS SEARCH 'computer']: Found {s_data.get('count')} results")
        else:
            print(f"[SEARCH FAILED]: {search_resp.status_code}")
    except Exception as e:
        print(f"Error connecting to database search: {e}")

    # 3. Test Chat Queries
    for q in TEST_QUERIES:
        try:
            resp = httpx.post(f"{BASE_API}/chat", json={"message": q, "session_id": SESSION_ID})
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n[QUERY]: {q}")
                print(f" -> Intent: {data['intent']} (Conf: {data['confidence']:.2f})")
                print(f" -> Answer: {data['answer'][:100]}...")
                print(f" -> Sources: {[s['title'] for s in data['sources']]}")
            else:
                print(f"FAILED query '{q}': Status {resp.status_code}")
        except Exception as e:
            print(f"Error querying chat: {e}")

if __name__ == "__main__":
    run_live_tests()
