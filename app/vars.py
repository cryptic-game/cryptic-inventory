# The product names must match those from the vars.py of cryptic-device.
# Prices are given in milli morphcoins!

game_info: dict = {
    "items": {
        # Mainboards
        "Zero MX One": {"id": 100, "price": 85_000, "related_ms": "device", "category": ["Mainboards", "Zero Socket"]},
        "Zero MX Pro": {"id": 101, "price": 96_000, "related_ms": "device", "category": ["Mainboards", "Zero Socket"]},
        "Zetta Ultimate M150": {"id": 102, "price": 109_000, "related_ms": "device",
                                "category": ["Mainboards", "Zetta Socket"]},
        "Zeus Professional X2": {"id": 103, "price": 160_000, "related_ms": "device",
                                 "category": ["Mainboards", "Zeus Socket"]},
        "Zeus Professional X3": {"id": 104, "price": 190_000, "related_ms": "device",
                                 "category": ["Mainboards", "Zeus Socket"]},
        # Processor
        "CoreOne A100": {"id": 200, "price": 140_000, "related_ms": "device", "category": ["Processor", "1-Core"]},
        "CoreOne A110": {"id": 201, "price": 152_000, "related_ms": "device", "category": ["Processor", "1-Core"]},
        "DualCore M101": {"id": 202, "price": 190_000, "related_ms": "device", "category": ["Processor", "2-Core"]},
        "QuadCore TX900": {"id": 203, "price": 326_000, "related_ms": "device", "category": ["Processor", "4-Core"]},
        "QuadCore TX950": {"id": 204, "price": 352_000, "related_ms": "device", "category": ["Processor", "4-Core"]},
        # Processor-Cooler
        "CPU Cooler Mini": {"id": 300, "price": 62_000, "related_ms": "device", "category": ["Cooler", None]},
        "CPU Cooler Plus": {"id": 301, "price": 75_000, "related_ms": "device", "category": ["Cooler", None]},
        "CPU Cooler Pro": {"id": 302, "price": 102_000, "related_ms": "device", "category": ["Cooler", None]},
        # RAM
        "Crossfire One": {"id": 400, "price": 102_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX100": {"id": 401, "price": 112_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX110": {"id": 402, "price": 117_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX120": {"id": 403, "price": 129_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX200": {"id": 404, "price": 144_000, "related_ms": "device", "category": ["RAM", "DDR2"]},
        "Crossfire ZX210": {"id": 405, "price": 119_000, "related_ms": "device", "category": ["RAM", "DDR2"]},
        "Crossfire ZX220": {"id": 406, "price": 175_000, "related_ms": "device", "category": ["RAM", "DDR3"]},
        "Crossfire P50": {"id": 407, "price": 200_000, "related_ms": "device", "category": ["RAM", "DDR4"]},
        "Crossfire P60": {"id": 408, "price": 210_000, "related_ms": "device", "category": ["RAM", "DDR4"]},
        # Graphic cards
        "Forcevid MX1000": {"id": 500, "price": 164_000, "related_ms": "device",
                            "category": ["Graphic cards", "GDDR1"]},
        "Zetta TX2066": {"id": 501, "price": 208_000, "related_ms": "device", "category": ["Graphic cards", "GDDR1"]},
        "Zetta TX2066 Pro": {"id": 502, "price": 265_000, "related_ms": "device",
                             "category": ["Graphic cards", "GDDR2"]},
        # Disks
        "HDD Elements Zero A": {"id": 600, "price": 88_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "HDD Elements Zero B": {"id": 601, "price": 94_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "HDD Elements Two": {"id": 602, "price": 104_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "SSD 20GB MX": {"id": 603, "price": 238_000, "related_ms": "device", "category": ["Disks", "SSD"]},
        "SSD 100GB M.2": {"id": 604, "price": 372_000, "related_ms": "device", "category": ["Disks", "M.2"]},
        # PowerPack
        "Crossfire XSOne 500 Watt": {"id": 700, "price": 98_000, "related_ms": "device",
                                     "category": ["Power pack", None]},
        "Zeus X10 Pro": {"id": 701, "price": 124_000, "related_ms": "device", "category": ["Power pack", None]},
        # Case
        "Mini-ITX": {"id": 800, "price": 145_000, "related_ms": "device", "category": ["Case", None]},
        "Mini-ATX": {"id": 801, "price": 185_000, "related_ms": "device", "category": ["Case", None]},
        "ATX": {"id": 802, "price": 202_000, "related_ms": "device", "category": ["Case", None]},
    }
}

CATEGORY_ORDER = [
    ("Mainboards", ["Zero Socket", "Zetta Socket", "Zeus Socket"]),
    ("Processor", ["1-Core", "2-Core", "4-Core"]),
    ("Cooler", []),
    ("RAM", ["DDR1", "DDR2", "DDR3", "DDR4"]),
    ("Graphic cards", ["GDDR1", "GDDR2"]),
    ("Disks", ["HDD", "SSD", "M.2"]),
    ("Power pack", []),
    ("Case", []),
]
shop_categories: dict = {}
for i, (category, subcategories) in enumerate(CATEGORY_ORDER):
    shop_categories[category] = {
        "items": {},
        "index": i,
        "categories": {},
    }
    for j, subcategory in enumerate(subcategories):
        shop_categories[category]["categories"][subcategory] = {"items": {}, "index": j, "categories": {}}

for name, item in game_info["items"].items():
    category_name, subcategory_name = item["category"]
    category = shop_categories[category_name]
    if subcategory_name is None:
        category["items"][name] = {k: v for k, v in item.items() if k != "category"}
        continue

    subcategory = category["categories"][subcategory_name]
    subcategory["items"][name] = {k: v for k, v in item.items() if k != "category"}
