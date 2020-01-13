# The product names must match those from the vars.py of cryptic-device.
# Prices are given in milli morphcoins!
game_info: dict = {
    "items": {
        # Mainboards
        "Zero MX One": {"price": 85_000, "related_ms": "device", "category": ["Mainboards", "Zero Socket"]},
        "Zero MX Pro": {"price": 96_000, "related_ms": "device", "category": ["Mainboards", "Zero Socket"]},
        "Zetta Ultimate M150": {"price": 109_000, "related_ms": "device", "category": ["Mainboards", "Zetta Socket"]},
        "Zeus Professional X2": {"price": 160_000, "related_ms": "device", "category": ["Mainboards", "Zeus Socket"]},
        "Zeus Professional X3": {"price": 190_000, "related_ms": "device", "category": ["Mainboards", "Zeus Socket"]},
        # Processor
        "CoreOne A100": {"price": 140_000, "related_ms": "device", "category": ["Processor", "1-Core"]},
        "CoreOne A110": {"price": 152_000, "related_ms": "device", "category": ["Processor", "1-Core"]},
        "DualCore M101": {"price": 190_000, "related_ms": "device", "category": ["Processor", "2-Core"]},
        "QuadCore TX900": {"price": 326_000, "related_ms": "device", "category": ["Processor", "4-Core"]},
        "QuadCore TX950": {"price": 352_000, "related_ms": "device", "category": ["Processor", "4-Core"]},
        # Processor-Cooler
        "CPU Cooler Mini": {"price": 62_000, "related_ms": "device", "category": ["Cooler", None]},
        "CPU Cooler Plus": {"price": 75_000, "related_ms": "device", "category": ["Cooler", None]},
        "CPU Cooler Pro": {"price": 102_000, "related_ms": "device", "category": ["Cooler", None]},
        # RAM
        "Crossfire One": {"price": 102_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX100": {"price": 112_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX110": {"price": 117_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX120": {"price": 129_000, "related_ms": "device", "category": ["RAM", "DDR1"]},
        "Crossfire ZX200": {"price": 144_000, "related_ms": "device", "category": ["RAM", "DDR2"]},
        "Crossfire ZX210": {"price": 119_000, "related_ms": "device", "category": ["RAM", "DDR2"]},
        "Crossfire ZX220": {"price": 175_000, "related_ms": "device", "category": ["RAM", "DDR3"]},
        "Crossfire P50": {"price": 200_000, "related_ms": "device", "category": ["RAM", "DDR4"]},
        "Crossfire P60": {"price": 210_000, "related_ms": "device", "category": ["RAM", "DDR4"]},
        # Graphic cards
        "Forcevid MX1000": {"price": 164_000, "related_ms": "device", "category": ["Graphic cards", "GDDR1"]},
        "Zetta TX2066": {"price": 208_000, "related_ms": "device", "category": ["Graphic cards", "GDDR1"]},
        "Zetta TX2066 Pro": {"price": 265_000, "related_ms": "device", "category": ["Graphic cards", "GDDR2"]},
        # Disks
        "HDD Elements Zero A": {"price": 88_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "HDD Elements Zero B": {"price": 94_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "HDD Elements Two": {"price": 104_000, "related_ms": "device", "category": ["Disks", "HDD"]},
        "SSD 20GB MX": {"price": 238_000, "related_ms": "device", "category": ["Disks", "SSD"]},
        "SSD 100GB M.2": {"price": 372_000, "related_ms": "device", "category": ["Disks", "M.2"]},
        # PowerPack
        "Crossfire XSOne 500 Watt": {"price": 98_000, "related_ms": "device", "category": ["Power pack", None]},
        "Zeus X10 Pro": {"price": 124_000, "related_ms": "device", "category": ["Power pack", None]},
        # Case
        "Mini-ITX": {"price": 145_000, "related_ms": "device", "category": ["Case", None]},
        "Mini-ATX": {"price": 185_000, "related_ms": "device", "category": ["Case", None]},
        "ATX": {"price": 202_000, "related_ms": "device", "category": ["Case", None]},
    }
}

shop_categories: dict = {}
for name, item in game_info["items"].items():
    category_name, subcategory_name = item["category"]
    category = shop_categories.setdefault(category_name, {"items": {}, "categories": {}})
    if subcategory_name is None:
        category["items"][name] = {k: v for k, v in item.items() if k != "category"}
        continue

    subcategory = category["categories"].setdefault(subcategory_name, {"items": {}, "categories": {}})
    subcategory["items"][name] = {k: v for k, v in item.items() if k != "category"}
