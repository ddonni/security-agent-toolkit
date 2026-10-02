# 1. "brute_force 보냄 " 을 줄을 바꾸지 않고 출력하세요
echo -n "brute_force 보냄 "
curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" \
  -d '{"rule":"brute_force"}' http://127.0.0.1:5001/webhook
echo
# 2. "password_spraying 보냄 " 을 줄을 바꾸지 않고 출력하세요
echo -n "password_spraying 보냄 "
curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" \
  -d '{"rule":"password_spraying"}' http://127.0.0.1:5001/webhook
echo
# 3. "night_login 보냄 " 을 줄을 바꾸지 않고 출력하세요
echo -n "night_login 보냄 "
curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" \
  -d '{"rule":"night_login"}' http://127.0.0.1:5001/webhook
echo
