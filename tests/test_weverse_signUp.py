import os
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()

TEST_EMAIL = os.getenv("WEVERSE_EMAIL")
TEST_PASSWORD = os.getenv("WEVERSE_PASSWORD")
WID_API_PATH = "users/v1.0/users/me"


def test_signup_and_get_wid(page: Page) -> None:
    page.goto("https://weverse.io/")
    page.get_by_role("button", name="로그인").click()
    page.get_by_role("button", name="회원가입").click()
    page.get_by_role("button", name="이메일로 가입하기").click()

    page.get_by_role("textbox", name="이메일 required").fill(TEST_EMAIL)
    page.get_by_role("button", name="인증코드 받기").click()

    while True:
        code = input("\n이메일로 받은 인증코드를 입력 후 Enter를 눌러주세요: ")
        page.get_by_role("textbox", name="인증코드 required").fill(code)
        page.get_by_role("button", name="인증코드 확인").click()

        try:
            page.get_by_text("인증코드를 다시 확인해 주세요").wait_for(timeout=3000)
            print("인증코드가 틀렸습니다. 다시 입력해주세요.")
            page.locator('[class*="dialog-button-area"]').get_by_role("button", name="확인").click()
            page.get_by_role("textbox", name="인증코드 required").clear()
        except Exception:
            break

    page.get_by_role("textbox", name="비밀번호 required").fill(TEST_PASSWORD)
    page.get_by_role("textbox", name="비밀번호 확인 required").fill(TEST_PASSWORD)

    page.get_by_role("button", name="다음").click()
    page.get_by_role("checkbox", name="모두 동의").click()
    page.get_by_role("button", name="가입하기").click()
    page.get_by_role("button", name="확인", exact=True).click()

    with page.expect_response(lambda r: WID_API_PATH in r.url) as resp:
        page.get_by_role("button", name="시작하기").click()

    wid = resp.value.json().get("wid")
    assert wid is not None, "WID를 찾을 수 없습니다."

    print(f"ID : {TEST_EMAIL}")
    print(f"PW : {TEST_PASSWORD}")
    print(f"WID: {wid}")