import argparse
import json
import os
import schedule
import time

parser = argparse.ArgumentParser(description="정기 점검 작업")
parser.add_argument("--every", type=int, default=2, help="몇 초마다 돌릴지")
args = parser.parse_args()

THRESHOLD = 1


def load_done():
    if os.path.exists("processed_ids.json"):
        with open("processed_ids.json", encoding="utf-8") as f:
            return json.load(f)
    return []


def job():
    with open("normalized_logs.json", encoding="utf-8") as f:
        rows = json.load(f)

    count = {}                                # 룰 ① — 계정마다 실패 횟수를 센다 (9/29)
    for row in rows:
        if row["level"] == "WARN":
            user = row["user"]
            if user in count:
                count[user] = count[user] + 1
            else:
                count[user] = 1

    done = load_done()
    sent = 0

    for user in count:
        if count[user] >= THRESHOLD:
            event_id = f"brute_force:{user}"
            # 1. event_id 가 done 에 없으면 (not in)
            if event_id not in done:
                # 2. "[전송]" 과 event_id 를 출력하고, done 에 event_id 를 append 하고, sent 에 1 을 더하세요
                print("[전송]", event_id)
                done.append(event_id)
                sent += 1



    with open("processed_ids.json", "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)

    print(f"점검 완료 — 새 경보 {sent}건")


# 3. job 을 args.every 초마다 부르게 등록하세요
schedule.every(args.every).seconds.do(job)

for i in range(4):
    schedule.run_pending()
    time.sleep(1)
