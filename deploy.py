"""把「經濟 通關」發佈到 GitHub Pages（新建倉庫 + 推送 + 開 Pages）。

用法：
    <python> econ-rogue/deploy.py            # 構建 → 建庫 → 推送 → 開 Pages
    <python> econ-rogue/deploy.py --no-build # 只推送，不重新構建

前提：
    - gh CLI 已登錄（目前賬號 ygo10ex-bit）
    - 本機 git 不在 PATH（用 GitHub Desktop 自帶那個）
"""
import glob
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
OWNER = "ygo10ex-bit"
REPO = "econ-rogue"
PAGES_URL = f"https://{OWNER}.github.io/{REPO}/"


def find_git():
    cands = []
    local = os.environ.get("LOCALAPPDATA", "")
    cands += glob.glob(os.path.join(local, "GitHubDesktop", "app-*", "resources", "app", "git", "cmd", "git.exe"))
    cands += [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    raise SystemExit("找不到 git.exe")


GIT = find_git()


def run(cmd, cwd=None, check=True):
    proc = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True)
    out = proc.stdout.decode("utf-8", "replace").strip()
    err = proc.stderr.decode("utf-8", "replace").strip()
    if check and proc.returncode != 0:
        print("命令失敗:", " ".join(cmd))
        print(err or out)
        raise SystemExit(1)
    return proc.returncode == 0, out, err


def gh(args, stdin_data=None):
    proc = subprocess.run(
        ["gh"] + args,
        input=stdin_data,
        capture_output=True,
    )
    return (
        proc.returncode == 0,
        proc.stdout.decode("utf-8", "replace").strip(),
        proc.stderr.decode("utf-8", "replace").strip(),
    )


def main():
    if "--no-build" not in sys.argv:
        print("== 1/5 構建 ==")
        ok, out, err = run([sys.executable, os.path.join(ROOT, "build.py")])
        print(out)

    print("== 2/5 本地 git 倉庫 ==")
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        run([GIT, "init", "-b", "main"])
        print("  已 git init")
    else:
        print("  倉庫已存在")

    gi = os.path.join(ROOT, ".gitignore")
    if not os.path.exists(gi):
        with open(gi, "w", encoding="utf-8") as fh:
            fh.write("__pycache__/\n*.pyc\n.pnpm-store/\n")
        print("  寫入 .gitignore")

    run([GIT, "add", "-A"])
    ok, out, err = run([GIT, "diff", "--cached", "--quiet"], check=False)
    if ok:
        print("  沒有新變動，跳過 commit")
    else:
        run([GIT, "-c", "core.autocrlf=false", "commit", "-m", "feat: 經濟通關 · 市場與效率題庫上線"])
        print("  已 commit")

    print("== 3/5 GitHub 倉庫 ==")
    ok, out, err = gh(["repo", "view", f"{OWNER}/{REPO}", "--json", "name", "--jq", ".name"])
    if ok:
        print(f"  倉庫已存在：{OWNER}/{REPO}")
    else:
        # 不帶 --source：某些 gh 版本在非 cwd 目錄下會誤報 not a git repository
        ok, out, err = gh([
            "repo", "create", f"{OWNER}/{REPO}", "--public",
            "--description", "經濟通關 · 市場與效率 · 繁體中文答題肉鴿（依據課堂筆記 Ch12／Ch13）",
        ])
        if not ok and "already exists" not in (err + out).lower():
            print("  建庫失敗：")
            print(err or out)
            return 1
        print(f"  已建立：{OWNER}/{REPO}")

    print("== 4/5 推送 ==")
    ok, out, err = run([GIT, "remote", "get-url", "origin"], check=False)
    if not ok:
        run([GIT, "remote", "add", "origin", f"https://github.com/{OWNER}/{REPO}.git"])
    # 這台機器 schannel 拿不到憑據、credential helper 也沒配；改用 gh token 臨時塞進 URL + openssl 後端。
    # token 只出現在命令行，不寫進 .git/config。
    tok_ok, tok, _ = gh(["auth", "token"])
    if not tok_ok or not tok:
        print("  拿不到 gh token，請先 gh auth login")
        return 1
    tok_url = f"https://x-access-token:{tok}@github.com/{OWNER}/{REPO}.git"
    ok, out, err = run([GIT, "-c", "http.sslBackend=openssl", "push", tok_url, "main:main"], check=False)
    if ok:
        print("  已推送")
    else:
        print("  推送失敗：")
        print(err or out)
        return 1
    run([GIT, "branch", "--set-upstream-to=origin/main", "main"], check=False)

    print("== 5/5 開啟 GitHub Pages ==")
    ok, out, err = gh(["api", f"repos/{OWNER}/{REPO}/pages"])
    if ok:
        try:
            info = json.loads(out)
            print("  Pages 已存在，狀態:", info.get("status"), info.get("html_url"))
        except Exception:
            print("  Pages 已存在")
    else:
        ok, out, err = gh([
            "api", "-X", "POST", f"repos/{OWNER}/{REPO}/pages",
            "-f", "source[branch]=main", "-f", "source[path]=/",
        ])
        if ok:
            print("  Pages 已啟用（首次構建約 1 分鐘）")
        else:
            print("  啟用 Pages 失敗：")
            print(err or out)
            print("  可到 https://github.com/%s/%s/settings/pages 手動選 main / root" % (OWNER, REPO))

    print()
    print("線上地址（手機點這個就能跳轉）：")
    print("  " + PAGES_URL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
