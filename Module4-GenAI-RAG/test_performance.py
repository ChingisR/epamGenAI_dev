import requests
import time
import statistics
import json

# Configuration
API_URL = "http://localhost:8000/query"

# TEST CASES based on the uploaded CVs
TEST_CASES = [
    # 1. Chingis Rustemov (Specific Achievement & Role)
    {
        "query": "Who received the 'PR Professional' Award for the Best Corporate Solution in Central Asia?",
        "expected_name": "Chingis",
        "context": "Chingis Rustemov_CV"
    },
    {
        "query": "Who is an IT (AI) Architect at IQ Solutions?",
        "expected_name": "Chingis",
        "context": "Chingis Rustemov_CV"
    },

    # 2. Sarah Jenkins (Architecture & Tech Stack)
    {
        "query": "Which candidate designed a Data Mesh connecting 5 distinct business domains?",
        "expected_name": "Sarah",
        "context": "Sarah Jenkins_CV"
    },
    {
        "query": "Who has experience with Azure Purview and GDPR Compliance?",
        "expected_name": "Sarah",
        "context": "Sarah Jenkins_CV"
    },

    # 3. James O'Connell (Data Science & Business Impact)
    {
        "query": "Who used XGBoost for customer churn prediction to retain $2M in revenue?",
        "expected_name": "James",
        "context": "James O'Connell_CV"
    },

    # 4. Elena Rodriguez (Computer Vision & Edge AI)
    {
        "query": "Who optimized YOLOv8 models for NVIDIA Jetson devices?",
        "expected_name": "Elena",
        "context": "Elena Rodriguez_CV"
    },

    # 5. Priya Gupta (Streaming Data Engineering)
    {
        "query": "Which engineer specializes in real-time pipelines using Apache Flink and Kafka?",
        "expected_name": "Priya",
        "context": "Priya Gupta_CV"
    },

    # 6. Kenji Sato (dbt & Modern Data Stack)
    {
        "query": "Who is an Analytics Engineer advocating for the Modern Data Stack using dbt and Snowflake?",
        "expected_name": "Kenji",
        "context": "Kenji Sato_CV"
    },

    # 7. Dr. Aris Chen (LLMs & NLP)
    {
        "query": "Who has a PhD in Computational Linguistics and fine-tuned Llama-2 models?",
        "expected_name": "Aris",
        "context": "Dr. Aris Chen_CV"
    },

    # 8. Elias Thorne (Cloud Architecture)
    {
        "query": "Who led the migration of 200+ on-prem apps to AWS as a Chief Architect?",
        "expected_name": "Elias",
        "context": "Elias Thorne_CV"
    },

    # 9. Linda Wei (Accounting & SAP)
    {
        "query": "Find a CPA with experience in SAP S/4HANA migration.",
        "expected_name": "Linda",
        "context": "Linda Wei_CV"
    },

    # 10. Robert Miller (Lakehouse & Spark)
    {
        "query": "Who managed a 2PB Delta Lake on Azure?",
        "expected_name": "Robert",
        "context": "Robert Miller_CV"
    }
]

def run_tests():
    latencies = []
    hits = 0
    total_tests = len(TEST_CASES)

    print(f"{'QUERY':<60} | {'STATUS':<10} | {'TIME (s)':<10}")
    print("-" * 90)

    for test in TEST_CASES:
        query_str = test['query']
        print(f"Asking: {query_str[:55]:<55}... ", end="", flush=True)
        
        start_time = time.time()
        try:
            # Send the query to your backend
            response = requests.post(API_URL, json={"query": query_str}, timeout=300)
            
            # Calculate duration
            duration = time.time() - start_time
            latencies.append(duration)
            
            if response.status_code == 200:
                ai_answer = response.json().get("response", "")
                
                # Check if the expected name is present in the answer (case-insensitive)
                if test['expected_name'].lower() in ai_answer.lower():
                    hits += 1
                    status = "✅ PASS"
                else:
                    status = "❌ FAIL"
                
                print(f"{status:<10} | {duration:.2f}s")
                
                # For failures, print debug info
                if status == "❌ FAIL":
                    print(f"   -> Expected: {test['expected_name']}")
                    print(f"   -> AI Said:  {ai_answer.strip()[:100]}...")
            else:
                print(f"⚠️ ERR {response.status_code}")
                print(f"   -> {response.text}")

        except Exception as e:
            print(f"⚠️ ERROR: {e}")

    # Summary Statistics
    if latencies:
        avg_latency = statistics.mean(latencies)
        hit_rate = (hits / total_tests) * 100
        
        print("-" * 90)
        print(f"🏆 PERFORMANCE SUMMARY")
        print(f"   - Total Questions: {total_tests}")
        print(f"   - Successful Hits: {hits}")
        print(f"   - Accuracy Rate:   {hit_rate:.1f}%")
        print(f"   - Average Latency: {avg_latency:.2f} seconds")
        print("-" * 90)

if __name__ == "__main__":
    print("🚀 Running Resume RAG Benchmark...")
    # Add a small delay to ensure backend is ready if just started
    time.sleep(2)
    run_tests()