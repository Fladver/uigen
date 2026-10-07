from PIL import Image, ImageDraw
import os

def preview(sprites: dict, path: str, cols: int = 8, cell: int = 96,
            padding: int = 12, bg=(32, 32, 40, 255), label_color=(220, 220, 220, 255)):
    """Контактный лист со всеми спрайтами и подписями."""
    n = len(sprites)
    rows = (n + cols - 1) // cols
    w = cols * (cell + padding) + padding
    h = rows * (cell + padding + 16) + padding

    sheet = Image.new("RGBA", (w, h), bg)
    draw = ImageDraw.Draw(sheet)

    for i, (name, img) in enumerate(sorted(sprites.items())):
        col = i % cols
        row = i // cols
        x = padding + col * (cell + padding)
        y = padding + row * (cell + padding + 16)

        # Центрируем спрайт в ячейке
        sw, sh = img.size
        scale = min(cell / sw, cell / sh, 1.0)
        if scale < 1.0:
            img = img.resize((int(sw * scale), int(sh * scale)), Image.NEAREST)
            sw, sh = img.size
        ox = x + (cell - sw) // 2
        oy = y + (cell - sh) // 2
        sheet.alpha_composite(img, (ox, oy))

        draw.text((x + 2, y + cell + 2), name[:18], fill=label_color)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    sheet.save(path)
    return path

def pack(sprites: dict, out_png: str, out_json: str, padding: int = 2,
         max_width: int = 2048, nine_slice: dict | None = None):
    """Атлас + JSON. nine_slice = {name: [l, b, r, t]} для 9-slice спрайтов."""
    import json
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

    frames = {}
    for name, p in positions.items():
        frame = {"x": p[0], "y": p[1], "w": p[2], "h": p[3]}
        if nine_slice and name in nine_slice:
            frame["border"] = nine_slice[name]
        frames[name] = frame

    meta = {"size": [max_width, total_h], "frames": frames}
    with open(out_json, "w") as f:
        json.dump(meta, f, indent=2)
    return meta
