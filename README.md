# Weverse 자동화 테스트

Playwright + pytest 기반으로 Weverse 회원가입(이메일로 시작하기) 및 포스트 작성/수정/삭제 자동화 테스트를 구현하였습니다.

## 환경 설정 (패키지 및 Playwright 브라우저 설치)

```bash
pip install -r requirements.txt
playwright install chromium
```

## .env 파일 설정

`.env` 파일에 회원가입 및 로그인에 사용할 ID와 PW 정보를 넣어주세요.

```
WEVERSE_EMAIL=이메일@example.com
WEVERSE_PASSWORD=비밀번호
```

## 테스트 실행

`-s` 옵션은 테스트 실행 중 터미널 입력을 가능하게 합니다. 이메일 인증코드 입력이 필요하므로 반드시 포함후 실행 부탁드립니다.

```bash
# 회원가입 + WID 추출
pytest tests/test_weverse_signUp.py -s

# 포스트 작성/수정/삭제
pytest tests/test_weverse_post.py -s
```

## 시현영상
회원가입

https://github.com/user-attachments/assets/c6eecc98-f6bf-4c63-97a0-1e0569ebfa69

포스트 작성/수정/삭제

https://github.com/user-attachments/assets/8a284c51-e5df-4807-bdf5-356215b3fb2d


## 참고사항

- 이메일 인증코드는 현재 테스트 실행 중 터미널에서 수동으로 입력하는 방식으로 구현했습니다. 자동화 관점에서 한계가 있다는 점을 인지하고 있으며, IMAP 프로토콜을 활용해 이메일을 직접 파싱하고 인증코드를 추출하는 방식으로 개선하고 싶습니다. 입사 후 IMAP 연동을 직접 구현해보겠습니다.
- 테스트 실행 중 이메일 인증코드 입력이 요구됩니다. 터미널에 표시되는 안내에 따라 입력 부탁드립니다.
- 포스트 작성 시 최초 1회 휴대폰 본인인증이 필요하여 수동 인증 이후, `test_weverse_post.py`를 실행하는 구조로 구현했습니다.
