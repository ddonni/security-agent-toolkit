
# day05 경보 판단

## 이상한 줄

- 줄 번호(여러 개면 모두): 2번 3번
- 이유: 웹에서 내부망  DB 로 바로 접속한 기록이 있음

## 고친 구성도

```
INTERNET ─:WEB (443 open)─── FW ──┬── DMZ    ( WEB )
                                  |             |
                                  |				: DB (3306 from WEB only)
                                  |				▽
                                  └── INSIDE ( DB )
```
