import schedule
import time
from simple_salesforce import Salesforce
from datetime import datetime
import sys

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# ── YOUR CREDENTIALS ── fill these in ──────────────────────────
SF_USERNAME      = "suganeshdhana842@agentforce.com"
SF_PASSWORD      = "Qwerzx@#12345"
SF_SECURITY_TOKEN = "GGzhRLKs7CIuRkowwvxzpa1JT"
OUTPUT_FILE      = "cases_log.txt"
# ───────────────────────────────────────────────────────────────

# Connect to Salesforce
sf = Salesforce(
    username=SF_USERNAME,
    password=SF_PASSWORD,
    security_token=SF_SECURITY_TOKEN
)

# Keep track of cases we've already seen
seen_case_ids = set()

def check_new_cases():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for new cases...")
    print("start", seen_case_ids)

    # Query Salesforce for cases (most recent 50)
    result = sf.query(
        "SELECT Id, CaseNumber, Subject, Status, CreatedDate, Priority "
        "FROM Case ORDER BY CreatedDate DESC LIMIT 50"
    )

    records = result['records']
    new_cases = []

    for case in records:
        case_id = case['Id']
        print("start")
        print("csid" + case_id)
        if case_id not in seen_case_ids:
            print('after check' + case_id)
            seen_case_ids.add(case_id)
            new_cases.append(case)

    if new_cases:
        print(f"  Found {len(new_cases)} new case(s)! Writing to file...")
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            for case in new_cases:
                line = (
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Case #{case['CaseNumber']} | "
                    f"Subject: {case['Subject']} | "
                    f"Status: {case['Status']} | "
                    f"Priority: {case['Priority']} | "
                    f"Created: {case['CreatedDate']}\n"
                )
                f.write(line)
                print(f"  >> {line.strip()}")
    else:
        print("  No new cases found.")

# Run once immediately on start
check_new_cases()

# Then run every 3 minutes
schedule.every(2).minutes.do(check_new_cases)

print("\nMonitoring started. Script checks every 3 minutes. Press Ctrl+C to stop.\n")

while True:
    schedule.run_pending()
    time.sleep(10)

