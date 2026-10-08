import llm_client                                             # 오전에 만든 llm_client.py 를 불러온다
import notifier                                               # 3교시에 만든 notifier.py 를 불러온다
import report_generator                                       # 오후에 만든 report_generator.py 를 불러온다

# 1. 문제 5-3 의 assert 세 줄을 옮기세요 (sample · two 도 함께)
sample = [{"id": "E01", "risk_level": "High", "summary": "로그인 실패 4회"}]   # 대문자가 섞인 요약 한 건
two = [{"id": "E02", "risk_level": "low", "summary": "새 IP 로그인"}, {"id": "E03", "risk_level": "medium", "summary": "심야 접속"}]   # 요약 두 건

assert report_generator.make_lines(sample) == "- [HIGH] E01 로그인 실패 4회\n", "make_lines 결과가 다르다"

assert report_generator.make_lines([]) == "", "빈 리스트는 빈 문자열이어야 한다"

assert len(report_generator.make_lines(two).split("\n")) == 3, "한 건에 한 줄이어야 한다"

# 2. 문제 5-4 의 assert 세 줄을 옮기세요 (config 도 함께)
config = {"approve_severity": "high"}                       # 기준만 있으면 판정할 수 있다

assert notifier.needs_approval("high", config) is True, "high 는 True 여야 한다"

assert notifier.needs_approval("low", config) is False, "low 는 False 여야 한다"

assert notifier.needs_approval("critical", config) is True, "처음 보는 위험도는 True 여야 한다"

# 3. 문제 5-5 의 assert 세 줄을 옮기세요 (fenced 도 함께)
fenced = "```json\n{\"tool\": \"lock_account\"}\n```"          # LLM 이 자주 보내는 모양 — 코드 블록에 싸인 JSON

assert llm_client.parse_llm_json(fenced) == {"tool": "lock_account"}, "parse_llm_json 결과가 다르다"

assert llm_client.parse_llm_json("그럴듯한 문장입니다") is None, "parse_llm_json 결과가 다르다"

assert llm_client.parse_llm_json("") is None, "parse_llm_json 결과가 다르다"
print("[테스트 통과] 9건 모두")                                       # 여기까지 오면 아홉 줄이 모두 참이었다
