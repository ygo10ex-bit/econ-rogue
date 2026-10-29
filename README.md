# 經濟 通關 · 市場與效率

一個**單文件網頁答題遊戲**，用「答題 + 目標分 + 道具構築」複習經濟學筆記。

- 線上玩（手機可直接開）：**https://ygo10ex-bit.github.io/econ-rogue/**
- 本地玩：雙擊 `經濟通關.html`
- 題庫依據：課堂筆記 **Ch12 市場與市場結構**、**Ch13 效率、公平與政府的角色**

---

## 內容規模

| 項目 | 數量 |
|---|---|
| 章 | 2 |
| 關卡 | 8（每章 4 關 + 1 個章末 Boss） |
| 題目 | 128（每關 16 題，抽 6 題） |
| 道具 | 27 件（普通 / 稀有 / 傳說） |
| 術語詞庫 | 24 條（MC、MB、TC、CS、PS、DWL…） |
| 單文件體積 | 約 79 KB |

## 怎麼玩

1. 答對得分，答錯扣血、斷連擊；分數達標才過關。
2. 分數 =（10 + 道具加成）× 連擊倍率 × 道具乘區 × 暴擊。
3. 連擊倍率 = 1 + 0.25 ×（連擊數 − 1），封頂 ×4；**連擊跨關保留**。
4. 每關通關後三選一拿道具，再進商店買；道具欄 5 格。
5. 章末 Boss：20 題、15 分鐘，目標分 450（第一章）／650（第二章）。
6. 通關條件：兩章全部關卡 + 兩個 Boss 通過，且模擬考 ≥700 兩次。

卡關就回去刷前幾關：分數夠高會給 2–3 星，金幣拿去買乘區道具，後面的關才過得了。

## 目錄結構

```
econ-rogue/
├─ index.html                 # 構建產物（GitHub Pages 入口，勿手改）
├─ 經濟通關.html                # 同一份內容，本地雙擊用
├─ build.py                   # 構建：structure + ch*.json → 注入 template
├─ deploy.py                  # 構建 → 建庫（若無）→ 推送 → 開 Pages
├─ src/
│  ├─ template.html           # 遊戲本體（UI + 計分 + 道具 + 詞庫）
│  ├─ structure.json          # 章節與關卡配置（章名、關卡名、目標分、概念卡、陷阱）
│  └─ ch1-a / ch1-b / ch2-a / ch2-b.json   # 題庫（共 128 題）
└─ tools/patch_template.py    # 一次性：把原始模板改造成經濟版（已跑過，無需再跑）
```

## 改題庫

題目格式（`src/ch*.json`，多個文件會合併成一個池）：

```json
{
  "id": "2-3-17",
  "ch": 2,
  "level": "2-3",
  "tag": "成本",
  "diff": 3,
  "q": "題幹",
  "opts": ["A", "B", "C", "D"],
  "ans": 1,
  "exp": "解析（答題後顯示）",
  "src": "課堂筆記 Ch13"
}
```

硬性規則（`build.py` 會檢查）：`id` 全域唯一、`opts` 剛好 4 個、`ans` 是 0–3、`level` 必須存在於 `structure.json`、`ch` 要跟 `level` 前綴一致。

### 構建

系統 python 是商店佔位，用 DSH 自帶的：

```powershell
$py = "$env:USERPROFILE\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
& $py econ-rogue\build.py
```

### 上線

```powershell
& $py econ-rogue\deploy.py            # 構建 + 推送 + 確保 Pages 開啟
& $py econ-rogue\deploy.py --no-build # 只推送
```

上線後 GitHub Pages 約 1 分鐘重建；手機上記得下拉刷新或清站點緩存。

## 改關卡

只改 `src/structure.json`：

- `chapters[].bossTarget`：章末 Boss 目標分
- `levels[].target`：該關目標分（第 1 章 45–80、第 2 章 120–190 是目前曲線）
- `levels[].card`：開場概念卡（3–5 條）
- `levels[].trap`：概念卡底部的陷阱提示

## 已知限制

- 進度存在瀏覽器 `localStorage`（key `econ_rogue_v1`），換裝置或清緩存就歸零。
- 單文件部署，沒有後端；題目全部隨 HTML 下發，所以「答案」在前端可見（複習工具，不防作弊）。
- 手機上第一次打開建議用 Wi-Fi 或 4G 都行，頁面約 79 KB，很快。
