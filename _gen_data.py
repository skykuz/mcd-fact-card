# -*- coding: utf-8 -*-
"""T4 数据唯一数据源：同时生成 menu.json 与内嵌兜底 JS 片段，保证两者绝对一致。"""
import json, io, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# (id, name, category, calories, protein, sodium)
CAT = {
    "burger": "汉堡",
    "side": "小食",
    "drink": "饮料",
    "dessert": "甜品",
    "breakfast": "早餐",
}

ITEMS = [
    # ---- 汉堡 ----
    ("hamburger",                  "汉堡包",                 "burger", 250, 12.5, 510),
    ("cheeseburger",               "吉士汉堡",               "burger", 300, 15.0, 700),
    ("double-cheeseburger",        "双层吉士汉堡",           "burger", 430, 24.0, 920),
    ("big-mac",                    "巨无霸",                 "burger", 550, 25.8, 1010),
    ("filet-o-fish",               "麦香鱼",                 "burger", 390, 16.0, 660),
    ("mccrispy-chicken",           "麦香鸡",                 "burger", 400, 17.0, 800),
    ("double-mccrispy",            "双层麦香鸡",             "burger", 520, 27.0, 1050),
    ("spicy-chicken-burger",       "麦辣鸡腿堡",             "burger", 570, 26.0, 1100),
    ("grilled-chicken-burger",     "板烧鸡腿堡",             "burger", 430, 24.0, 890),
    ("spicy-grilled-chicken",      "麻辣板烧鸡腿堡",         "burger", 450, 24.5, 950),
    ("bacon-double-beef",          "培根蔬萃双层牛堡",       "burger", 600, 32.0, 1180),
    ("angus-beef-burger",          "安格斯厚牛堡",           "burger", 800, 40.0, 1380),
    ("double-angus-cheese",        "双层安格斯厚牛芝士堡",   "burger", 950, 50.0, 1700),
    ("garden-veggie-burger",       "田园蔬萃堡",             "burger", 350, 12.0, 720),

    # ---- 小食 ----
    ("mcnuggets-5",                "麦乐鸡（5块）",          "side", 220, 10.5, 400),
    ("mcnuggets-10",               "麦乐鸡（10块）",         "side", 440, 19.0, 780),
    ("mcnuggets-20",               "麦乐鸡（20块）",         "side", 880, 38.0, 1560),
    ("fries-small",                "薯条（小份）",           "side", 230, 3.0, 130),
    ("fries-medium",               "薯条（中份）",           "side", 330, 4.0, 180),
    ("fries-large",                "薯条（大份）",           "side", 430, 5.0, 220),
    ("twister-fries",              "扭扭薯条",               "side", 340, 4.5, 300),
    ("spicy-wings-2",              "麦辣鸡翅（2块）",        "side", 190, 12.0, 500),
    ("spicy-wings-4",              "麦辣鸡翅（4块）",        "side", 380, 24.0, 1000),
    ("spicy-chicken-leg",          "麦辣鸡腿",               "side", 260, 20.0, 620),
    ("popcorn-chicken-medium",     "劲爆鸡米花（中份）",     "side", 380, 20.0, 890),
    ("popcorn-chicken-large",      "劲爆鸡米花（大份）",     "side", 500, 26.0, 1150),
    ("corn-cup-small",             "玉米杯（小）",           "side", 70, 2.0, 5),
    ("corn-cup-large",             "玉米杯（大）",           "side", 130, 4.0, 10),
    ("garden-salad",               "田园蔬菜沙拉",           "side", 100, 3.0, 200),

    # ---- 饮料 ----
    ("coke-small",                 "可口可乐（小杯）",       "drink", 110, 0.0, 10),
    ("coke-medium",                "可口可乐（中杯）",       "drink", 150, 0.0, 15),
    ("coke-large",                 "可口可乐（大杯）",       "drink", 210, 0.0, 20),
    ("coke-zero-medium",           "零度可乐（中杯）",       "drink", 0, 0.0, 20),
    ("sprite-medium",              "雪碧（中杯）",           "drink", 140, 0.0, 15),
    ("fanta-medium",               "芬达（中杯）",           "drink", 150, 0.0, 20),
    ("minute-maid-orange",         "美汁源果粒橙（中杯）",   "drink", 160, 1.0, 15),
    ("ice-tea-medium",             "冰爽茶（中杯）",         "drink", 90, 0.0, 10),
    ("lemon-black-tea",            "柠檬红茶（中杯）",       "drink", 100, 0.0, 10),
    ("milk",                       "纯牛奶",                 "drink", 130, 7.0, 100),
    ("hot-soy-milk",               "热豆浆",                 "drink", 120, 8.0, 60),
    ("americano-medium",           "美式咖啡（中杯）",       "drink", 15, 0.3, 10),
    ("latte-medium",               "拿铁（中杯）",           "drink", 120, 6.0, 90),
    ("iced-latte-medium",          "冰拿铁（中杯）",         "drink", 130, 5.5, 85),
    ("cappuccino-medium",          "卡布奇诺（中杯）",       "drink", 110, 5.5, 85),
    ("mocha-medium",               "摩卡（中杯）",           "drink", 200, 7.0, 110),
    ("hot-chocolate-medium",       "热巧克力（中杯）",       "drink", 190, 6.5, 120),

    # ---- 甜品 ----
    ("taro-pie",                   "香芋派",                 "dessert", 240, 3.0, 200),
    ("pineapple-pie",              "菠萝派",                 "dessert", 250, 3.0, 210),
    ("apple-pie",                  "苹果派",                 "dessert", 240, 2.5, 200),
    ("chocolate-pie",              "巧克力派",               "dessert", 260, 3.5, 210),
    ("cone-vanilla",               "甜筒（原味）",           "dessert", 180, 4.0, 80),
    ("cone-chocolate",             "甜筒（巧克力）",         "dessert", 220, 4.5, 90),
    ("sundae-chocolate",           "巧克力新地",             "dessert", 340, 6.0, 120),
    ("sundae-strawberry",          "草莓新地",               "dessert", 300, 5.5, 110),
    ("mcflurry-original",          "麦旋风（原味）",         "dessert", 330, 6.0, 150),
    ("mcflurry-oreo",              "麦旋风（奥利奥）",       "dessert", 380, 7.0, 180),
    ("mcflurry-strawberry",        "麦旋风（草莓）",         "dessert", 360, 6.5, 170),
    ("mcflurry-matcha",            "麦旋风（抹茶）",         "dessert", 370, 6.5, 165),

    # ---- 早餐 ----
    ("egg-cheese-mcmuffin",        "吉士蛋麦满分",           "breakfast", 300, 16.0, 700),
    ("sausage-mcmuffin",           "猪柳麦满分",             "breakfast", 380, 18.0, 900),
    ("sausage-egg-mcmuffin",       "猪柳蛋麦满分",           "breakfast", 450, 22.0, 1000),
    ("bacon-egg-mcmuffin",         "烟肉蛋麦满分",           "breakfast", 330, 18.0, 830),
    ("double-egg-cheese-mcmuffin", "双层吉士蛋麦满分",       "breakfast", 400, 23.0, 950),
    ("hash-brown-2",               "薯饼（2块）",            "breakfast", 230, 3.0, 400),
    ("hotcakes-3",                 "热香饼（3块）",          "breakfast", 350, 8.0, 520),
    ("sausage-hotcakes",           "猪柳热香饼",             "breakfast", 550, 20.0, 1100),
    ("congee",                     "皮蛋瘦肉粥",             "breakfast", 180, 8.0, 600),
]

# 唯一性校验
ids = [i[0] for i in ITEMS]
names = [i[1] for i in ITEMS]
assert len(ids) == len(set(ids)), "id 重复: " + str([x for x in ids if ids.count(x) > 1])
assert len(names) == len(set(names)), "name 重复: " + str([x for x in names if names.count(x) > 1])
for it in ITEMS:
    assert it[3] >= 0 and it[4] >= 0 and it[5] >= 0, f"负值: {it}"
    assert it[2] in CAT, f"未知分类: {it}"

BASE = os.path.dirname(os.path.abspath(__file__))

menu = {
    "version": 2,
    "source": "麦当劳公开营养信息的近似估值（仅供对比演示，非官方实时数据）",
    "unit": {"calories": "kcal", "protein": "g", "sodium": "mg"},
    "categories": [{"id": k, "name": v} for k, v in CAT.items()],
    "items": [
        {"id": i, "name": n, "category": c, "calories": ca, "protein": p, "sodium": s}
        for (i, n, c, ca, p, s) in ITEMS
    ],
}

with io.open(os.path.join(BASE, "menu.json"), "w", encoding="utf-8") as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)
    f.write("\n")

# ============ 资产数据（T5）：与内嵌兜底同源生成 ============
import time
NOW = int(time.time() * 1000)
H = 3600 * 1000
D = 24 * H

# (id, name, face, unit, count, estimate单份估值元, 过期偏移[毫秒]，None=无时间戳)
ASSETS = [
    ("mm-save-8",         "麦麦省满减券（满30减8）", 8,    "元", 2, 8.0,   6 * H),
    ("breakfast-50",      "早餐套餐 5 折券",         9,    "元", 1, 9.0,   8 * H),
    ("cone-exchange",     "积分商城免费兑换券（甜筒）", 1,  "张", 1, 6.0,   19 * H),
    ("nuggets-bogo",      "麦乐鸡买一送一券",        22,   "元", 1, 22.0,  3 * D),
    ("upsize-free",       "免费升杯券",              3,    "元", 3, 3.0,   5 * D),
    ("points-1280",       "会员积分",                1280, "分", 1, 12.8,  30 * D),
    ("lucky-draw-3",      "抽奖次数",                3,    "次", 1, 5.0,   -1 * D),   # 已过期（覆盖过期分支）
    ("birthday-burger",   "生日免费汉堡券（待激活）", 25,   "元", 1, 25.0,  None),     # 无时间戳（覆盖未知时间分支）
]

aids = [a[0] for a in ASSETS]
assert len(aids) == len(set(aids)), "资产 id 重复"

assets = {
    "version": 1,
    "source": "模拟的麦当劳用户资产数据（演示用，非真实账户数据）",
    "generatedAt": NOW,
    "note": "过期时间戳 = 生成时刻 + 相对偏移；重跑 _gen_data.py 可刷新为当前时间基准",
    "unit": {"estimate": "元"},
    "items": [
        {
            "id": i, "name": n, "face": f, "unit": u, "count": c,
            "estimate": e,
            "expireAt": (NOW + off) if off is not None else None,
        }
        for (i, n, f, u, c, e, off) in ASSETS
    ],
}

with io.open(os.path.join(BASE, "assets.json"), "w", encoding="utf-8") as f:
    json.dump(assets, f, ensure_ascii=False, indent=2)
    f.write("\n")

# 注入 index.html 的内嵌兜底（幂等：用区间标记，可反复运行）
lines = []
for it in assets["items"]:
    exp = "null" if it["expireAt"] is None else str(it["expireAt"])
    lines.append(
        '      {"id":"%s","name":"%s","face":%s,"unit":"%s","count":%s,"estimate":%s,"expireAt":%s}'
        % (it["id"], it["name"], it["face"], it["unit"], it["count"], it["estimate"], exp)
    )
assets_js = '    "generatedAt": %d,\n    "items": [\n%s\n    ]\n' % (NOW, ",\n".join(lines))

html_path = os.path.join(BASE, "index.html")
html = io.open(html_path, encoding="utf-8").read()
S, E = "/* ASSETS_EMBEDDED_START */", "/* ASSETS_EMBEDDED_END */"
assert S in html and E in html, "index.html 缺少资产嵌入区间标记"
i0 = html.index(S) + len(S)
i1 = html.index(E)
html = html[:i0] + "\n" + assets_js + "  " + html[i1:]
io.open(html_path, "w", encoding="utf-8").write(html)

print("餐品总数:", len(ITEMS))
from collections import Counter
cnt = Counter(i[2] for i in ITEMS)
for k, v in cnt.items():
    print(f"  {CAT[k]}({k}): {v} 条")
print("menu.json:", os.path.getsize(os.path.join(BASE, "menu.json")), "B")

print("\n资产总数:", len(ASSETS))
n_expired = sum(1 for a in ASSETS if a[6] is not None and a[6] <= 0)
n_urgent = sum(1 for a in ASSETS if a[6] is not None and 0 < a[6] < 24 * H)
n_unknown = sum(1 for a in ASSETS if a[6] is None)
print(f"  即将过期(<24h): {n_urgent} 条 | 已过期: {n_expired} 条 | 无时间戳: {n_unknown} 条")
print("assets.json:", os.path.getsize(os.path.join(BASE, "assets.json")), "B")
print("index.html:", os.path.getsize(html_path), "B")
print("id/name 唯一性: OK")
