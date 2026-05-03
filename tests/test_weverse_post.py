import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

IMAGE_PATH = Path(__file__).parent.parent / "data" / "image.jpeg"
VIDEO_PATH = Path(__file__).parent.parent / "data" / "video.mov"

load_dotenv()

TEST_EMAIL = os.getenv("WEVERSE_EMAIL")
TEST_PASSWORD = os.getenv("WEVERSE_PASSWORD")


def _login(page: Page) -> None:
    page.goto("https://weverse.io/")
    page.get_by_role("button", name="로그인").click()
    page.get_by_role("button", name="이메일로 로그인").click()

    page.get_by_role("textbox", name="your@email.com").fill(TEST_EMAIL)
    page.get_by_role("textbox", name="비밀번호").fill(TEST_PASSWORD)
    page.get_by_role("button", name="로그인").click()
    page.get_by_role("textbox", name="인증코드").click()

    while True:
        code = input("\n이메일로 받은 인증코드를 입력 후 Enter를 눌러주세요: ")
        page.get_by_role("textbox", name="인증코드").fill(code)
        page.get_by_role("button", name="인증코드 확인").click()

        try:
            page.locator('[class*="common-modal"]').get_by_role("button", name="확인").wait_for(timeout=3000)
            page.locator('[class*="common-modal"]').get_by_role("button", name="확인").click()
            break
        except Exception:
            print("인증코드가 틀렸습니다. 다시 입력해주세요.")
            page.get_by_role("textbox", name="인증코드").clear()


def test_post(page: Page) -> None:
    #로그인
    _login(page)

    #임의의 커뮤니티 가입
    page.get_by_role("button").filter(has_text="커뮤니티 찾기").click()
    page.locator('[class*="global-search-community-list-view"]').first.click()
    page.locator("#iwma").get_by_role("button", name="가입하기").click()
    page.get_by_label("wev3 modal").locator("button").filter(has_text="가입하기").click()

    #커뮤니티 프로필 페이지로 이동
    page.locator('[class*="global-header-profile"]').click()

    #포스트 등록
    POST_TEXT1 = "좋아좋아"
    page.get_by_text("팬들과 이야기를 나눠보세요").click()
    page.get_by_text("위버스에 남겨보세요…").fill(POST_TEXT1)
    page.get_by_label("attach photo", exact=True).set_input_files(IMAGE_PATH)
    expect(page.locator(".confirm_button")).to_be_enabled()
    page.locator(".confirm_button").click()
    page.locator("button").filter(has_text="등록").click()

    #포스트 등록 확인
    expect(page.locator('[class*="post-module-_-wrapper"]').filter(has_text=POST_TEXT1)).to_be_visible()

    #포스트 수정
    POST_TEXT2="완전 좋아!!"
    page.locator('[class*="post-module-_-wrapper"]').filter(has_text=POST_TEXT1).get_by_role("button", name="more").click()
    page.locator('[class*="menu-_-text"]', has_text="수정하기").click()
    expect(page.locator('[class*="wev-editor-slot-view-_-container"]')).to_be_visible()
    page.locator("button").filter(has_text="delete image").click()
    page.locator('[class*="wev-editor-slot-view-_-container"]').get_by_text(POST_TEXT1).fill(POST_TEXT2)
    page.get_by_label("attach video", exact=True).set_input_files(VIDEO_PATH)
    expect(page.locator(".confirm_button")).to_be_enabled(timeout=60000)
    page.locator(".confirm_button").click()
    page.locator("button").filter(has_text="등록").click()

    #포스트 수정 확인
    expect(page.locator('[class*="post-module-_-wrapper"]').filter(has_text=POST_TEXT2)).to_be_visible()

    #포스트 삭제
    page.locator('[class*="post-module-_-wrapper"]').filter(has_text=POST_TEXT2).get_by_role("button", name="more").click()
    page.locator('[class*="menu-_-text"]', has_text="삭제하기").click()
    expect(page.locator('[class*="common-modal-_-modal"]')).to_be_visible()
    page.locator('[class*="common-modal-_-modal"]').locator("button").filter(has_text="확인").click()

    #포스트 삭제 확인
    expect(page.locator('[class*="profile-content-empty-_-container"]')).to_be_visible()
    expect(page.get_by_text("아직 작성한 포스트가 없습니다.")).to_be_visible()
    page.wait_for_timeout(5000)

