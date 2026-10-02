import argparse
import json
from flask import Flask, request

# 1. parser 를 만들고, --port 인자(정수, 기본값 5000)를 받고, args 에 parse_args() 결과를 담으세요


app = Flask(__name__)
received = []

parser = argparse.ArgumentParser()
# 1. --port 인자를 받으세요. type=int 를 쓰지 않고, 기본값은 글자 "5000" 입니다
parser.add_argument("--port", default="5000", help="열어 둘 포트 번호")
args = parser.parse_args()

@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.get_json()
    received.append(event)
    with open("received_alerts.json", "w", encoding="utf-8") as f:
        json.dump(received, f, ensure_ascii=False, indent=2)
    if "rule" in event:
        print("[수신]", event["rule"])
    # 2. {"status": "ok", "count": received 의 길이} 와 200 을 return 하세요
    return {"status": "ok", "count": len(received)}, 200

app.run(port=args.port, debug=True)
# 3. args 로 받은 포트로 app 을 실행하세요
