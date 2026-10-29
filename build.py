"""構建「經濟 通關」單文件遊戲。

用法：
    <python> econ-rogue/build.py

輸入：
    econ-rogue/src/structure.json   章節與關卡配置
    econ-rogue/src/ch*.json          題庫（多個文件合併成一個池子）
    econ-rogue/src/template.html     遊戲本體（含兩個 JSON 佔位符）

輸出：
    econ-rogue/經濟通關.html         本地打開用
    econ-rogue/index.html            部署到 GitHub Pages 用（倉庫根目錄）
"""
import glob
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "經濟通關.html")
DIST = os.path.join(ROOT, "index.html")


def main():
    bank = []
    files = sorted(glob.glob(os.path.join(SRC, "ch*.json")))
    if not files:
        print("找不到題庫：src/ch*.json")
        return 1
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        assert isinstance(data, list), f"{os.path.basename(f)} 不是陣列"
        print(f"  {os.path.basename(f):16s} {len(data):3d} 題")
        bank += data

    ids = [q["id"] for q in bank]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    assert not dup, f"題目 id 重複：{dup[:10]}"

    with open(os.path.join(SRC, "structure.json"), encoding="utf-8") as fh:
        structure = json.load(fh)
    level_ids = {lvl["id"] for lvl in structure.get("levels", [])}
    chapter_ns = [c["n"] for c in structure.get("chapters", [])]

    for q in bank:
        assert len(q["opts"]) == 4, f'{q["id"]}: 選項不是 4 個'
        assert q["ans"] in (0, 1, 2, 3), f'{q["id"]}: ans 不合法'
        assert len(set(q["opts"])) == 4, f'{q["id"]}: 有重複選項'
        assert q["level"] in level_ids, f'{q["id"]}: level {q["level"]} 不在 structure 裡'
        assert str(q["ch"]) == q["level"].split("-")[0], f'{q["id"]}: ch 與 level 前綴不一致'
        assert q.get("q") and q.get("exp"), f'{q["id"]}: 缺 q 或 exp'

    # 每關題量檢查：抽 6 題，池子太小會一直重複
    for lid in sorted(level_ids):
        n = sum(1 for q in bank if q["level"] == lid)
        flag = "" if n >= 12 else "  ⚠ 題量偏少"
        print(f"  level {lid}: {n} 題{flag}")
    for n in chapter_ns:
        cnt = sum(1 for q in bank if q["ch"] == n)
        assert cnt >= 20, f"第 {n} 章只有 {cnt} 題，Boss 抽 20 題會不夠"

    body = json.dumps(bank, ensure_ascii=False, separators=(",", ":"))
    struct_body = json.dumps(structure, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(SRC, "template.html"), encoding="utf-8") as fh:
        tpl = fh.read()
    assert "__BANK_JSON__" in tpl and "__STRUCTURE_JSON__" in tpl, "模板缺佔位符"
    html = tpl.replace("__STRUCTURE_JSON__", struct_body).replace("__BANK_JSON__", body)

    for path in (OUT, DIST):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print("寫入:", path, len(html), "chars")

    print(f"完成：{len(structure['chapters'])} 章 / {len(level_ids)} 關 / {len(bank)} 題")
    return 0


if __name__ == "__main__":
    sys.exit(main())
