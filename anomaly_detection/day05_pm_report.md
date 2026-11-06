# 4과목 Day 5 도커 컴포즈로 서버 두 대 켜기 · 웹 서버 로그 만들기 · 오후 (곽도현 · 2026-11-06(금))

> **쓰는 법**
> - 문제를 풀 때마다 그 문제 제목 아래 질문에 답합니다.
> - 질문마다 `쓸 내용:` 에 무엇을 쓰면 되는지 적혀 있습니다. 그대로 `답:` 뒤에 씁니다.
> - 출력이나 코드를 붙여 넣는 질문은 `답:` 아래 빈 코드 상자에 붙여 넣고, 설명은 `답:` 뒤에 씁니다.
> - 「왜」를 묻는 질문은 한 단어로 끝내지 말고, 내 화면에서 본 값이나 배운 내용을 근거로 이유까지 씁니다.
> - 🔍 는 이 교시에서 꼭 알아야 할 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 이라고 씁니다. 🔍 가 없는 질문도 못 적으면 같은 말을 씁니다.

---

## 5교시 · 도커 복습 · 컴포즈로 서버 두 대 한 번에 켜기

### 문제 5-1 · 서버 한 대를 복습하고 컴포즈로 두 대 켜기

- (가) 5교시 순서의 서버 켜기 · 확인 명령(`docker images` 부터 `curl` 까지)과 그 결과를 친 순서대로 붙여 넣고, 서비스 이름 두 개와 각 서비스의 포트를 적어 주세요.
  - 쓸 내용: ① 명령과 결과를 친 순서대로(코드 상자에 붙여 넣기): `docker images` · `docker run` · `docker ps` · `docker stop` · `docker compose up -d` · `docker compose ps` · `curl` 두 개 (`docker pull` 은 받았을 때만, `pwd` · `touch` · `ls` 는 붙이지 않아도 됩니다) ② 서비스 이름 두 개 ③ 각 서비스의 포트
  - 답: 서비스 이름은 `web1` · `web2`이고, 포트는 `web1`이 8083, `web2`가 8081이다. 내 PC에서 `mysite-lab-control-plane` 컨테이너가 `127.0.0.1:8080`을 쓰고 있어서 `web1`은 안내문의 8080 대신 8083으로 바꿨다.

```
$ docker images nginx:1.28
IMAGE        ID             DISK USAGE   CONTENT SIZE   EXTRA
nginx:1.28   146adea4768b        240MB         65.8MB
$ docker run -d --rm -p 8083:80 --name web-run nginx:1.28
e86330f1e41d910c612138e2bf8febadc56e13fd8176f801ab1394b05147e875
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                   CREATED             STATUS                  PORTS                                                  NAMES
e86330f1e41d   nginx:1.28             "/docker-entrypoint.…"   1 second ago        Up Less than a second   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp                web-run
222915b5ccda   kindest/node:v1.37.0   "/usr/local/bin/entr…"   About an hour ago   Up About an hour        127.0.0.1:55537->6443/tcp, 127.0.0.1:8080->30080/tcp   mysite-lab-control-plane
$ docker stop web-run
web-run
$ docker compose up -d
 Network anomaly_detection_default Creating
 Network anomaly_detection_default Creating
 Network anomaly_detection_default Created
 Network anomaly_detection_default Created
 Container anomaly_detection-web2-1 Creating
 Container anomaly_detection-web1-1 Creating
 Container anomaly_detection-web2-1 Created
 Container anomaly_detection-web1-1 Created
 Container anomaly_detection-web2-1 Starting
 Container anomaly_detection-web1-1 Starting
 Container anomaly_detection-web2-1 Started
 Container anomaly_detection-web1-1 Started
$ docker compose ps
NAME                       IMAGE        COMMAND                   SERVICE   CREATED        STATUS                  PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      1 second ago   Up Less than a second   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      1 second ago   Up Less than a second   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8083
200
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081
200
```

- (나) 🔍 서버 두 대를 `docker run` 으로 켜는 것과 `compose.yaml` 과 `docker compose up -d` 로 켜는 것을 비교해, 컴포즈가 더 나은 점을 두 가지 적어 주세요.
  - 쓸 내용: ① 컴포즈가 더 나은 점 두 가지
  - 답: ① `docker run`은 서버마다 긴 명령을 따로 쳐야 하지만, 컴포즈는 `docker compose up -d` 한 줄로 서버 두 대를 한 번에 켜고 끌 수 있다.
    ② 포트 · 이미지 버전 같은 옵션이 파일에 남아서, 옵션을 외우거나 다시 치다가 틀릴 일이 줄고 누가 켜도 같은 서버가 켜진다. 파일을 저장소에 올리면 설정 기록으로도 남는다.

- (다) 🔍 보안 사고가 난 뒤 감사팀이 「사고 당시와 같은 구성으로 서버를 다시 켜 보라」고 요청했습니다. 팀원 한 명은 3주 전에 긴 `docker run` 명령을 직접 쳐서 서버를 켰는데 그 명령을 기억하지 못합니다. 다른 팀은 `compose.yaml` 을 깃허브에 올려 두었습니다. 두 팀이 같은 구성을 다시 켤 수 있는지 비교하고, 파일에 `nginx:1.28` 처럼 버전을 적어 두는 것이 이런 재현에 왜 중요한지 적어 주세요.
  - 쓸 내용: ① 두 팀의 차이 ② 버전을 적어 두는 것이 재현에 중요한 이유
  - 답: ① `docker run` 팀은 명령을 기록하지 않아 포트 · 이름 · 이미지 버전을 알 수 없으므로 같은 구성을 다시 켠다고 보장할 수 없다. 컴포즈 팀은 깃허브의 `compose.yaml`로 `docker compose up -d` 한 줄이면 같은 구성을 다시 켤 수 있고, 언제 무엇을 바꿨는지도 기록으로 확인할 수 있다.
    ② `nginx:1.28`처럼 버전을 적으면 몇 주 뒤에도 같은 버전으로 켤 수 있어 사고 당시와 환경이 같아진다. `nginx`처럼 이름만 적으면 그때의 최신 버전을 받아 동작이 달라질 수 있고, 다른 조건이 섞여 재현 결과를 믿기 어렵다.

- (라) 🔍 팀원 세 명이 같은 `compose.yaml` 로 서버를 켰는데 한 명의 PC 에서만 `8081` 번 포트를 다른 프로그램이 쓰고 있어서 `web2` 가 켜지지 않았습니다. 이 사람이 파일의 어느 줄을 어떻게 바꾸면 되는지 적고, 바꿔도 서버 안에서는 여전히 `80` 번 포트로 동작하는 이유를 적어 주세요. 이 사람이 `curl` 로 확인할 때 달라지는 점도 적어 주세요.
  - 쓸 내용: ① 바꿀 줄과 바꾼 모양 ② 서버 안은 그대로 80 인 이유 ③ curl 주소의 달라지는 점
  - 답: ① `web2`의 `- "8081:80"`에서 왼쪽 숫자만 비어 있는 번호로 바꾼다. 예: `- "8090:80"`
    ② 콜론 왼쪽은 내 컴퓨터의 포트이고 오른쪽은 서버(컨테이너) 안의 포트이다. 왼쪽만 바꿨으므로 서버 안은 그대로 80번으로 동작한다.
    ③ 이 사람은 `curl` 주소의 포트를 바꾼 왼쪽 번호로 써야 한다. 예: `http://localhost:8090`. 다른 팀원은 그대로 8081번으로 확인한다.

## 6교시 · 서버마다 접속 범위 정하기 · 설정 바꿔 적용하기

### 문제 6-1 · 서버마다 접속 범위를 정해 컴포즈 파일로 적용하기

- (가) 1번과 5번의 `docker compose ps` 출력을 붙여 넣고, 접속 범위가 바뀐 기존 서비스와 새로 추가된 서비스를 따로 적어 주세요.
  - 쓸 내용: ① 1번 출력(코드 상자에 붙여 넣기) ② 5번 출력(코드 상자에 붙여 넣기) ③ 접속 범위가 바뀐 기존 서비스 ④ 새로 추가된 서비스
  - 답: 접속 범위가 바뀐 기존 서비스는 `web2`이고(`0.0.0.0:8081` → `127.0.0.1:8081`), 새로 추가된 서비스는 `web3`이다(`127.0.0.1:8082`). `web1`은 `0.0.0.0:8083` 그대로이다. 내 PC에서는 처음 적용할 때 `web2`가 `Recreated` 뒤 `127.0.0.1:8081` 포트 오류로 켜지지 않았다. 8081을 쓰는 프로그램은 없었고(`netstat`에 LISTENING 없음), 몇 초 뒤 `docker compose -f compose.secure.yaml up -d`를 다시 치자 켜져서 `curl`도 `200`이 나왔다. 5번 출력은 다시 친 뒤의 출력이다.

1번 출력

```
NAME                       IMAGE        COMMAND                   SERVICE   CREATED         STATUS         PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      4 seconds ago   Up 3 seconds   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      4 seconds ago   Up 3 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
```

5번 출력

```
NAME                       IMAGE        COMMAND                   SERVICE   CREATED          STATUS          PORTS
anomaly_detection-web1-1   nginx:1.28   "/docker-entrypoint.…"   web1      18 seconds ago   Up 17 seconds   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp
anomaly_detection-web2-1   nginx:1.28   "/docker-entrypoint.…"   web2      14 seconds ago   Up 3 seconds    127.0.0.1:8081->80/tcp
anomaly_detection-web3-1   nginx:1.28   "/docker-entrypoint.…"   web3      14 seconds ago   Up 12 seconds   127.0.0.1:8082->80/tcp
```

- (나) 🔍 `"8081:80"` 과 `"127.0.0.1:8081:80"` 은 누가 접속할 수 있는지가 어떻게 다른가요? 관리 화면이나 데이터베이스 서버를 이렇게 설정하는 이유도 적어 주세요.
  - 쓸 내용: ① 두 포트 줄에서 누가 접속할 수 있는지의 차이 ② 관리 화면 · 데이터베이스를 이렇게 설정하는 이유
  - 답: ① `"8081:80"`은 주소를 적지 않아 내 PC뿐 아니라 같은 네트워크의 다른 PC도 접속할 수 있다. `"127.0.0.1:8081:80"`은 맨 앞의 `127.0.0.1`이 내 컴퓨터를 뜻하므로(루프백 주소) 내 PC에서만 접속할 수 있다.
    ② 관리 화면이나 데이터베이스는 필요한 사람만 쓰는 서버이다. 밖에 열어 두면 스캐너가 `/phpmyadmin` 같은 주소를 찾아 들어올 수 있으므로, 꼭 열어야 하는 서버만 열고 나머지는 `127.0.0.1:`로 제한한다.

- (다) 🔍 `up -d` 의 출력에서 `web1` 은 `Running`, `web2` 는 `Recreated`, `web3` 은 `Created` 였습니다. 서버마다 출력이 다른 이유와, 운영 중인 서비스의 설정을 바꿀 때 이것이 왜 도움이 되는지 적어 주세요.
  - 쓸 내용: ① 서버마다 출력이 다른 이유 ② 서버를 끊지 않고 바꿀 수 있는 것의 쓸모
  - 답: ① `web1`은 설정이 바뀌지 않아 그대로 두었으므로 `Running`이다. `web2`는 실패한 것이 아니라 포트 줄이 바뀌어서 기존 서버를 새 설정으로 다시 만들었으므로 `Recreated`이다. `web3`은 파일에 새로 추가된 서버라서 `Created`이다.
    ② 설정을 바꿔도 바뀐 서버만 다시 만들어지고 나머지는 끊기지 않는다. 그래서 운영 중인 `web1`을 멈추지 않고 다른 서버의 보안 설정을 고칠 수 있다.

### 마무리 · 오늘 만든 것을 깃허브에 올리기

- (가) `git status` 를 쳤을 때 `.env` 나 `.venv` 가 보였는지, 보였다면 어떻게 했는지 적어 주세요.
  - 쓸 내용: ① `.env` · `.venv` 가 보였는지 ② 보였다면 한 조치
  - 답: ① `git status`에 `.env`와 `.venv`는 보이지 않았다. `.gitignore`에 이미 적혀 있다. ② 보이지 않았으므로 따로 조치하지 않았다.
