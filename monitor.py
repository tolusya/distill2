import difflib
from pathlib import Path

from fetcher import fetch_static, fetch_rendered
from notify import send_telegram
from sites import SITES

STATE_DIR = Path(__file__).parent / "state"
MAX_DIFF_CHARS = 3000


def get_text(site):
    if site["mode"] == "static":
        return fetch_static(site["url"], site["selector"])
    return fetch_rendered(site["url"], site["selector"])


def make_diff(old, new):
    lines = []
    for line in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=1):
        if line.startswith(("+++", "---", "@@")):
            continue
        lines.append(line)

    diff = "\n".join(lines)
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n…(обрезано)"
    return diff


def check_site(site):
    name = site["name"]
    state_file = STATE_DIR / f"{name}.txt"
    new_text = get_text(site)

    if not state_file.exists():
        state_file.write_text(new_text, encoding="utf-8")
        print(f"[{name}] первый запуск, снимок сохранён")
        return

    old_text = state_file.read_text(encoding="utf-8")
    if new_text == old_text:
        print(f"[{name}] без изменений")
        return

    header = f"🔔 {name}: изменения"
    keyword = site.get("keyword")
    if keyword and keyword in new_text and keyword not in old_text:
        header = f"🔥 {name}: появилось «{keyword}»!"

    message = f"{header}\n{site['url']}\n\n{make_diff(old_text, new_text)}"

    if send_telegram(message):
        state_file.write_text(new_text, encoding="utf-8")
        print(f"[{name}] изменения отправлены")


def main():
    STATE_DIR.mkdir(exist_ok=True)

    for site in SITES:
        name = site["name"]
        error_file = STATE_DIR / f"{name}.error"

        try:
            check_site(site)
        except Exception as e:
            print(f"[{name}] ошибка: {e}")
            if not error_file.exists():
                short_error = str(e)[:500]
                send_telegram(f"⚠️ {name}: проверка не работает\n{site['url']}\n\n{short_error}")
                error_file.write_text(str(e), encoding="utf-8")
            continue

        if error_file.exists():
            send_telegram(f"✅ {name}: снова работает")
            error_file.unlink()


if __name__ == "__main__":
    main()
