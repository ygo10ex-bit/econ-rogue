"""把 CISSP 模板改造成「經濟 通關」模板（一次性 patch）。

用法：
    <python> econ-rogue/tools/patch_template.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "src", "template.html")


def sub_once(t, old, new, label):
    n = t.count(old)
    assert n == 1, f"[{label}] 期望 1 次匹配，實際 {n} 次"
    return t.replace(old, new)


def re_sub_once(t, pattern, new, label):
    out, n = re.subn(pattern, lambda m: new, t, flags=re.S)
    assert n == 1, f"[{label}] 期望 1 次匹配，實際 {n} 次"
    return out


DICT_NEW = """const DICT={
 'MC':'邊際成本（Marginal Cost）：多生產一單位所增加的成本',
 'MB':'邊際利益（Marginal Benefit）：多消費一單位所獲得的利益',
 'MR':'邊際收入（Marginal Revenue）：多賣一單位所增加的收入',
 'AR':'平均收入（Average Revenue），在完全競爭下等於價格',
 'TC':'總成本（Total Cost）＝總固定成本＋總可變成本',
 'TFC':'總固定成本（Total Fixed Cost）',
 'TVC':'總可變成本（Total Variable Cost）',
 'ATC':'平均總成本（Average Total Cost）＝TC ÷ 產量',
 'AVC':'平均可變成本（Average Variable Cost）＝TVC ÷ 產量',
 'AFC':'平均固定成本（Average Fixed Cost）＝TFC ÷ 產量',
 'SMC':'短期邊際成本（Short-run Marginal Cost）',
 'SRAC':'短期平均成本（Short-run Average Cost）',
 'LRAC':'長期平均成本（Long-run Average Cost）',
 'CS':'消費者盈餘（Consumer Surplus）＝願付最大數額－實際支付',
 'PS':'生產者盈餘（Producer Surplus）＝實收數額－最低願收數額',
 'TS':'總社會盈餘（Total Social Surplus）＝CS＋PS',
 'DWL':'淨損失／無謂損失（Deadweight Loss）：缺乏效率而白白流失的總盈餘',
 'PED':'需求價格彈性（Price Elasticity of Demand）',
 'YED':'需求收入彈性（Income Elasticity of Demand）',
 'XED':'需求交叉價格彈性（Cross-price Elasticity of Demand）',
 'PES':'供應價格彈性（Price Elasticity of Supply）',
 'HHI':'赫芬達爾－赫希曼指數（Herfindahl-Hirschman Index）：市場集中度',
 'MRP':'邊際收入產品（Marginal Revenue Product）',
 'P':'價格（Price）',
 'Q':'數量（Quantity）'
};"""

ITEMS_NEW = """const ITEMS=[
{id:'marker',name:'螢光筆',rarity:'C',price:7,flat:2,desc:'每題基礎分 +2。'},
{id:'sticky',name:'便利貼',rarity:'C',price:10,flat:3,desc:'每題基礎分 +3。'},
{id:'calc',name:'計數機',rarity:'C',price:9,flat:2,comboMin:4,comboFlat:4,desc:'每題 +2；連擊 ≥4 時再加 +4。'},
{id:'coffee',name:'提神咖啡',rarity:'C',price:8,maxHp:1,desc:'生命上限 +1。'},
{id:'admit',name:'准考證',rarity:'C',price:6,hints:1,desc:'每關開場多 1 次提示。'},
{id:'eraser',name:'橡皮擦',rarity:'C',price:7,skips:1,desc:'每關開場多 1 次跳過。'},
{id:'tuition',name:'補習優惠券',rarity:'C',price:10,shopDisc:0.15,desc:'商店售價與刷新費用 −15%。'},
{id:'abacus',name:'小算盤',rarity:'C',price:9,goldPerCorrect:1,desc:'每答對一題多賺 1 金幣。'},
{id:'errorfile',name:'錯題夾',rarity:'C',price:8,failRefund:4,desc:'關卡失敗返還 4 金幣。'},
{id:'flashcard',name:'速記卡',rarity:'C',price:9,flat:1,goldFlat:{per:20,cap:5},desc:'每題 +1；每 20 金幣再加 +1，最多 +5。'},
{id:'textbook',name:'經濟學原理',rarity:'U',price:16,flat:6,desc:'每題基礎分 +6。'},
{id:'demandcurve',name:'需求曲線尺',rarity:'U',price:15,firstMult:1.6,desc:'每關第 1 題分數 ×1.6。'},
{id:'supplycurve',name:'供應曲線尺',rarity:'U',price:15,lastMult:1.6,desc:'每關最後一題分數 ×1.6。'},
{id:'margin',name:'邊際筆記',rarity:'U',price:17,comboPer:8,desc:'每題額外加「當前連擊數」，最多 +8。'},
{id:'combocharm',name:'連擊徽章',rarity:'U',price:17,comboMin:5,comboMult:1.15,desc:'連擊 ≥5 時，分數再 ×1.15。'},
{id:'midterm',name:'期中考卷',rarity:'U',price:16,posMult:{4:1.25,5:1.25,6:1.25},desc:'每關第 4–6 題分數 ×1.25。'},
{id:'slide',name:'計算尺',rarity:'U',price:18,mult:1.2,desc:'分數固定 ×1.2。'},
{id:'lucky',name:'幸運橡皮',rarity:'U',price:14,critAdd:0.08,desc:'暴擊率 +8%（基礎 5%）。'},
{id:'portfolio',name:'投資組合',rarity:'U',price:16,critMult:2.5,desc:'暴擊倍率由 ×2 提升到 ×2.5。'},
{id:'shield',name:'學分護盾',rarity:'U',price:15,shield:1,desc:'每關擋掉 1 次答錯（不扣血）。'},
{id:'retake',name:'補考機會',rarity:'U',price:18,revive:1,desc:'每關剩最後 1 命時免死一次。'},
{id:'backpack',name:'大書包',rarity:'U',price:14,shopSlots:1,desc:'商店多 1 個道具格子。'},
{id:'profnotes',name:'教授私人筆記',rarity:'R',price:28,flat:10,desc:'每題基礎分 +10。'},
{id:'nobel',name:'諾貝爾筆記',rarity:'R',price:32,mult:1.5,desc:'分數固定 ×1.5。'},
{id:'battery',name:'連擊電池',rarity:'R',price:30,comboMin:3,comboMult:1.3,desc:'連擊 ≥3 時，分數再 ×1.3。'},
{id:'timer',name:'時間延長器',rarity:'R',price:24,bossTime:1,desc:'章末 Boss 戰多 5 分鐘。'},
{id:'perfection',name:'滿分執念',rarity:'R',price:26,goldPerCorrect:3,endGold:8,desc:'每答對一題 +3 金幣，過關額外 +8 金幣。'}
];"""

MENU_NEW = """function viewMenu(){
  const cleared=CHS.filter(c=>c.n<=2&&S.boss[c.n]).length;
  return `<div class="hdr"><div class="logo">經濟 <span>通關</span></div>
  <div class="tagline">市場與效率 · 構築型肉鴿 · 題庫 ${BANK.length} 題 · v1.0（2026-10-29）</div></div>
  <div class="panel"><div class="ptitle">通關條件</div>
   <div class="cond ${cleared===2?'on':''}">① 兩章關卡全清並擊敗章末 Boss（${cleared}/2）</div>
   <div class="cond ${S.mockPass>=2?'on':''}">② 模擬考 ≥700 兩次（${S.mockPass}/2，最好 ${S.best}）</div>
   <div class="cond">金幣 <b>${S.gold}</b> · 道具 ${S.items.length}/${SLOTS} · 已答 ${S.tot.q} 題（正確率 ${S.tot.q?Math.round(S.tot.c/S.tot.q*100):0}%）</div>
   ${itemBar()}
  </div>
  <div class="grid">
   <button class="btn primary" data-act="map">開始闖關</button>
   <button class="btn" data-act="mock">模擬考試</button>
   <button class="btn" data-act="cards">必背速查</button>
   <button class="btn" data-act="review">錯題本（${wrongCount()}）</button>
   <button class="btn ghost" data-act="import">導入題庫</button>
   <button class="btn ghost danger" data-act="reset">重置進度</button>
  </div>
  <div class="small" style="margin-top:14px">題庫依課堂筆記 Ch12（市場與市場結構）與 Ch13（效率、公平與政府的角色）編寫。後期關卡目標分陡增，光答對不夠，要靠道具構築。</div>`;
}"""

CARDS_NEW = """function viewCards(){
  const c=(t,items,trap)=>`<div class="card"><h4>${t}</h4><ul>${items.map(i=>`<li>${i}</li>`).join('')}</ul>${trap?`<div class="trap">⚠ ${trap}</div>`:''}</div>`;
  return `<div class="hdr"><div class="logo" style="font-size:22px">必背速查</div><div class="tagline">考前 20 分鐘只看這幾張</div></div>
  ${c('四種市場結構',['壟斷：只有 1 個賣家 · 進入受限制 · 市場資訊不完全','寡頭壟斷：少數生產者 · 商品同質或異質 · 進入困難','壟斷性競爭：很多賣家 · 異質商品 · 進出容易','完全競爭：很多賣家 · 同質商品 · 進出容易 · 資訊完全'])}
  ${c('誰能影響價格',['壟斷／寡頭壟斷／壟斷性競爭＝定價者 price maker','完全競爭＝受價者 price taker','完全競爭市場沒有價格競爭，也沒有非價格競爭','競爭程度：壟斷最低 → 寡頭 → 壟斷性競爭 → 完全競爭最高'],'只有完全競爭是受價者')}
  ${c('利益與需求',['總利益＝消費某一數量的全部利益','邊際利益＝多消費一單位的額外利益＝願付最高價','邊際利益曲線就是需求曲線，向下傾斜','買到價格＝邊際利益為止'],'邊際看「多一單位」，不是平均')}
  ${c('成本與供應',['總成本＝固定成本＋可變成本','邊際成本＝多生產一單位的成本＝最低願收價','邊際成本曲線就是供應曲線','生產到價格＝邊際成本為止'],'固定成本不影響邊際成本')}
  ${c('兩個盈餘',['消費者盈餘＝願付最大數額 − 實際支付','生產者盈餘＝實收數額 − 最低願收數額','價格下跌：消費者盈餘增，生產者盈餘減','圖上面積：CS 在價格線上方，PS 在價格線下方']) }
  ${c('效率與淨損失',['效率：價格＝邊際利益＝邊際成本','此時總社會盈餘＝消費者盈餘＋生產者盈餘 最大','市價高於均衡價 → 交易量不足 → 出現淨損失','淨損失是雙方合計變少，不是單方吃虧']) }
  ${Object.keys(S.glossary).length?`<div class="card"><h4>生詞本（查過的術語）</h4>
    ${Object.entries(S.glossary).sort((a,b)=>b[1]-a[1]).map(([t,n])=>`<div class="mrow"><b>${t}</b><span>${esc(DICT[t]||'（未收錄）')}　<span class="small">查過 ${n} 次</span></span></div>`).join('')}</div>`:''}
  <div class="row"><button class="btn small ghost" data-act="menu">← 返回主菜單</button></div>`;
}"""

IMPORT_NEW = """function viewImport(){
  return `<div class="hdr"><div class="logo" style="font-size:22px">導入題庫</div><div class="tagline">把自己的題目轉成 JSON 後粘進來</div></div>
  <div class="panel"><div class="small">每題字段：<br><code>id, ch, level, tag, diff, q, opts[4], ans(0-3), exp, src</code><br>
  level 用 <code>1-1</code>…<code>2-4</code>；同 id 會覆蓋舊題。</div>
  <textarea id="importbox" placeholder='[{"id":"x-001","ch":2,"level":"2-3","tag":"成本","diff":3,"q":"題幹","opts":["A","B","C","D"],"ans":1,"exp":"解析","src":"自製"}]'></textarea>
  <div class="row"><button class="btn primary small" data-act="import-text">粘貼導入</button>
    <button class="btn small" data-act="import-file">選擇 JSON 文件</button>
    <button class="btn small ghost" data-act="menu">返回</button></div>
  <div class="small" style="margin-top:10px">文件會存進瀏覽器本地。</div></div>`;
}"""


def main():
    with open(TPL, encoding="utf-8") as fh:
        t = fh.read()
    orig_len = len(t)

    t = sub_once(t, "<title>CISSP 通關 · 1–3 章</title>", "<title>經濟 通關 · 市場與效率</title>", "title")
    t = re_sub_once(t, r"const DICT=\{.*?\n\};", DICT_NEW, "DICT")
    t = sub_once(
        t,
        "const SKEY='cissp_rogue_v3', CKEY='cissp_custom_bank_v1', SLOTS=5;",
        ITEMS_NEW + "\nconst SKEY='econ_rogue_v1', CKEY='econ_custom_bank_v1', SLOTS=5;",
        "SKEY/ITEMS",
    )
    t = re_sub_once(t, r"function viewMenu\(\)\{.*?\n\}\n\nfunction viewMap", MENU_NEW + "\n\nfunction viewMap", "viewMenu")
    t = re_sub_once(t, r"function viewCards\(\)\{.*?\n\}\nfunction viewImport", CARDS_NEW + "\nfunction viewImport", "viewCards")
    t = re_sub_once(t, r"function viewImport\(\)\{.*?\n\}\n\n/\* ================= 流程", IMPORT_NEW + "\n\n/* ================= 流程", "viewImport")
    t = sub_once(
        t,
        '<div class="small" style="margin-top:10px">考試模式：不給反饋、可上下翻題、連續計時 180 分鐘。道具不生效。滿分 1000，700 通過。</div>',
        '<div class="small" style="margin-top:10px">考試模式：不給反饋、可上下翻題、連續計時 60 分鐘。道具不生效。滿分 1000，700 通過。</div>',
        "mock-note",
    )
    t = sub_once(t, "雖然只是 100 題，也別太得意。", "雖然只是 50 題，也別太得意。", "mock-all-right")
    t = sub_once(
        t,
        "const qs=pick(BANK,Math.min(100,BANK.length));",
        "const qs=pick(BANK,Math.min(50,BANK.length));",
        "mock-size",
    )
    t = sub_once(
        t,
        "answers:new Array(qs.length).fill(null),deadline:Date.now()+180*60*1000};",
        "answers:new Array(qs.length).fill(null),deadline:Date.now()+60*60*1000};",
        "mock-time",
    )
    t = sub_once(
        t,
        "· 道具 ${S.items.length}/${SLOTS}${disc?` · 教授筆記 −${Math.round(disc*100)}%`:''}</div>",
        "· 道具 ${S.items.length}/${SLOTS}${disc?` · 補習優惠 −${Math.round(disc*100)}%`:''}</div>",
        "shop-disc-label",
    )

    with open(TPL, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)
    print("patched:", TPL, orig_len, "->", len(t), "chars")
    print("ITEMS count:", t.count("rarity:'"))
    print("has ITEMS def:", "const ITEMS=[" in t)
    print("has DICT econ:", "'DWL'" in t)


if __name__ == "__main__":
    main()
