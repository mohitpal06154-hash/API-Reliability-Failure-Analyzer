import requests
import time
import pandas as pd
import os

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
SLA_THRESHOLD = 0.5  # 500ms SLA

results = []

def test_api(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    
    start_time = time.time()
    response = requests.get(url)
    latency = time.time() - start_time

    status = response.status_code
    valid_response = status == 200

    performance_issue = latency > SLA_THRESHOLD

    results.append({
        "Endpoint": endpoint,
        "Status Code": status,
        "Latency (sec)": round(latency, 4),
        "Valid Response": valid_response,
        "Performance Issue": performance_issue
    })

# Positive Test Cases
for i in range(1, 20):
    test_api(i)

# Negative Test Cases
test_api(9999)   # Non-existing ID
test_api("abc")  # Invalid input

# Save Results
if not os.path.exists("results"):
    os.makedirs("results")

df = pd.DataFrame(results)
df.to_csv("results/api_report.csv", index=False)

print("Testing Completed. Report saved in results/api_report.csv")
