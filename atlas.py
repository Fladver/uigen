# atlas.py
from PIL import Image
import json, os

def pack(sprites: dict, out_png: str, out_json: str, padding=2, max_width=2048):
    """
    sprites: {"name": PIL.Image}
    Простая полочная упаковка без внешних либ.
    """
    items = sorted(sprites.items(), key=lambda kv: -kv[1].height)
    x = y = 0
    row_h = 0
    positions = {}

    for name, img in items:
        w, h = img.size
        if x + w + padding > max_width:
            x = 0
            y += row_h + padding
            row_h = 0
        positions[name] = (x, y, w, h)
        x += w + padding
        row_h = max(row_h, h)

    total_h = y + row_h + padding
    atlas = Image.new("RGBA", (max_width, total_h), (0, 0, 0, 0))

    for name, img in items:
        px, py, _, _ = positions[name]
        atlas.paste(img, (px, py))

    atlas.save(out_png)

    meta = {
        "size": [max_width, total_h],
        "frames": {
            name: {"x": p[0], "y": p[1], "w": p[2], "h": p[3]}
            for name, p in positions.items()
        },
    }
    with open(out_json, "w") as f:
        json.dump(meta, f, indent=2)

    return meta