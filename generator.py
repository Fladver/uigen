from PIL import Image, ImageDraw, ImageFilter
import math

# ---------- утилиты ----------

def hex_to_rgba(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def _blank(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ---------- базовые фигуры ----------

def rounded_rect(w, h, radius=8, thickness=2, fill=(255,255,255,255), border=(0,0,0,255)):
    img = _blank(w, h)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(0,0),(w-1,h-1)], radius=radius, fill=border)
    if thickness > 0:
        d.rounded_rectangle(
            [(thickness, thickness), (w-1-thickness, h-1-thickness)],
            radius=max(0, radius-thickness), fill=fill
        )
    else:
        d.rounded_rectangle([(0,0),(w-1,h-1)], radius=radius, fill=fill)
    return img

def circle(size, fill=(255,255,255,255), border=None, thickness=2):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    if border:
        d.ellipse([(0,0),(size-1,size-1)], fill=border)
        d.ellipse([(thickness,thickness),(size-1-thickness,size-1-thickness)], fill=fill)
    else:
        d.ellipse([(0,0),(size-1,size-1)], fill=fill)
    return img

def star(size, points=5, fill=(255,215,0,255), border=None, thickness=2):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2
    outer = size / 2 - 1
    inner = outer * 0.45
    verts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / points
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(verts, fill=fill, outline=border, width=thickness if border else 0)
    return img

def heart(size, fill=(255,80,120,255), border=None, thickness=2):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    s = size / 100
    def pt(x, y): return (x * s, y * s)
    verts = [
        pt(50, 90), pt(10, 50), pt(10, 30), pt(20, 15),
        pt(35, 10), pt(50, 25), pt(65, 10), pt(80, 15),
        pt(90, 30), pt(90, 50),
    ]
    d.polygon(verts, fill=fill, outline=border, width=thickness if border else 0)
    return img

def diamond(size, fill=(120,200,255,255), border=None, thickness=2):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    h = size - 1
    verts = [(size/2, 0), (h, size/2), (size/2, h), (0, size/2)]
    d.polygon(verts, fill=fill, outline=border, width=thickness if border else 0)
    return img

# ---------- иконки-символы ----------

def icon_coin(size, fill=(255,200,50,255), border=(180,130,20,255)):
    img = circle(size, fill=fill, border=border, thickness=3)
    d = ImageDraw.Draw(img)
    d.text((size*0.38, size*0.28), "$", fill=(120,80,10,255))
    return img

def icon_plus(size, fill=(80,200,120,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    t = size // 5
    d.rectangle([(size//2 - t//2, t), (size//2 + t//2, size - t)], fill=fill)
    d.rectangle([(t, size//2 - t//2), (size - t, size//2 + t//2)], fill=fill)
    return img

def icon_minus(size, fill=(200,80,80,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    t = size // 5
    d.rectangle([(t, size//2 - t//2), (size - t, size//2 + t//2)], fill=fill)
    return img

def icon_check(size, fill=(80,200,120,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    w = max(2, size // 10)
    d.line([(size*0.2, size*0.5), (size*0.42, size*0.72), (size*0.8, size*0.28)],
           fill=fill, width=w, joint="curve")
    return img

def icon_cross(size, fill=(220,80,80,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    w = max(2, size // 10)
    m = size * 0.25
    d.line([(m, m), (size-m, size-m)], fill=fill, width=w)
    d.line([(m, size-m), (size-m, m)], fill=fill, width=w)
    return img

# ---------- панели и фоны ----------

def gradient(w, h, top, bottom, horizontal=False):
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / (w - 1)) if horizontal else (y / (h - 1))
            px[x, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(4))
    return img

def pattern_stripes(w, h, color_a, color_b, stripe=8, diagonal=False):
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            v = (x + y) if diagonal else x
            px[x, y] = color_a if (v // stripe) % 2 == 0 else color_b
    return img

def pattern_checker(w, h, color_a, color_b, cell=8):
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = color_a if ((x // cell) + (y // cell)) % 2 == 0 else color_b
    return img

def pattern_dots(w, h, bg, dot_color, spacing=16, radius=3):
    img = Image.new("RGBA", (w, h), bg)
    d = ImageDraw.Draw(img)
    for y in range(0, h, spacing):
        for x in range(0, w, spacing):
            d.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=dot_color)
    return img

# ---------- бары и прогресс ----------

def progress_bar(w, h, fill_ratio, bg=(60,60,60,255), fill=(80,200,120,255), radius=4):
    img = _blank(w, h)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(0,0),(w-1,h-1)], radius=radius, fill=bg)
    fw = int((w - 2) * max(0, min(1, fill_ratio)))
    if fw > 0:
        d.rounded_rectangle([(1,1),(1+fw, h-2)], radius=max(0, radius-1), fill=fill)
    return img

def progress_bar_9slice(w, h, bg, fill, radius=4):
    """Пустой бар — заливку делаешь в Unity через Image.fillAmount."""
    return rounded_rect(w, h, radius, 2, bg, fill)

# ---------- рамки и тени ----------

def frame(w, h, thickness=6, color=(200,170,100,255), inner=(0,0,0,0)):
    img = _blank(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([(0,0),(w-1,h-1)], fill=color)
    d.rectangle([(thickness,thickness),(w-1-thickness,h-1-thickness)], fill=inner)
    return img

def frame_ornate(w, h, color=(220,190,120,255), corner=10):
    img = _blank(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([(0,0),(w-1,h-1)], outline=color, width=2)
    for cx, cy in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
        d.ellipse([(cx-corner,cy-corner),(cx+corner,cy+corner)], fill=color)
    return img

def shadow(w, h, radius=8, blur=6, alpha=90):
    pad = blur * 2
    img = Image.new("RGBA", (w + pad, h + pad), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(pad,pad),(pad+w,pad+h)], radius=radius, fill=(0,0,0,alpha))
    return img.filter(ImageFilter.GaussianBlur(blur // 2))

# ---------- портреты и аватары ----------

def avatar_circle(size, fill=(120,160,220,255), border=(255,255,255,255)):
    return circle(size, fill=fill, border=border, thickness=3)

def avatar_frame(size, color=(200,170,100,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    d.ellipse([(0,0),(size-1,size-1)], outline=color, width=4)
    return img

# ---------- чекбоксы, тоглы, слайдеры ----------

def checkbox(size, checked=False, fill=(80,200,120,255), border=(200,200,200,255)):
    img = rounded_rect(size, size, radius=4, thickness=2, fill=fill, border=border)
    if checked:
        d = ImageDraw.Draw(img)
        w = max(2, size // 8)
        d.line([(size*0.22, size*0.5), (size*0.42, size*0.72), (size*0.78, size*0.28)],
               fill=(255,255,255,255), width=w, joint="curve")
    return img

def toggle(w, h, on=True, on_color=(80,200,120,255), off_color=(120,120,120,255)):
    img = _blank(w, h)
    d = ImageDraw.Draw(img)
    r = h // 2
    color = on_color if on else off_color
    d.rounded_rectangle([(0,0),(w-1,h-1)], radius=r, fill=color)
    kx = (w - h) if on else 0
    d.ellipse([(kx+2, 2), (kx+h-2, h-2)], fill=(255,255,255,255))
    return img

def slider_knob(size, fill=(255,255,255,255), border=(80,80,80,255)):
    return circle(size, fill=fill, border=border, thickness=3)

# ---------- стрелки и навигация ----------

def arrow(size, direction="right", fill=(60,60,60,255)):
    img = _blank(size, size)
    d = ImageDraw.Draw(img)
    s = size
    if direction == "right":
        pts = [(s*0.3, s*0.2), (s*0.7, s*0.5), (s*0.3, s*0.8)]
    elif direction == "left":
        pts = [(s*0.7, s*0.2), (s*0.3, s*0.5), (s*0.7, s*0.8)]
    elif direction == "up":
        pts = [(s*0.2, s*0.7), (s*0.5, s*0.3), (s*0.8, s*0.7)]
    else:  # down
        pts = [(s*0.2, s*0.3), (s*0.5, s*0.7), (s*0.8, s*0.3)]
    d.polygon(pts, fill=fill)
    return img

# ---------- генератор набора по конфигу ----------

def build_from_config(cfg: dict) -> dict:
    """
    cfg = {
      "palette": {"primary": "#...", "border": "#...", "accent": "#..."},
      "buttons": [[128,48],[192,64]],
      "icons": ["heart","star","coin","plus","check"],
      "bars": [[128,12]],
      "extras": ["checkbox","toggle","arrow_right"]
    }
    Возвращает dict {name: PIL.Image}
    """
    pal = cfg.get("palette", {})
    primary = hex_to_rgba(pal.get("primary", "#4CAF50"))
    border = hex_to_rgba(pal.get("border", "#FFFFFF"))
    accent = hex_to_rgba(pal.get("accent", "#FFC107"))

    out = {}

    for w, h in cfg.get("buttons", []):
        out[f"btn_{w}x{h}"] = rounded_rect(w, h, 12, 2, primary, border)

    icon_map = {
        "heart": lambda: heart(64, fill=accent),
        "star":  lambda: star(64, fill=accent),
        "coin":  lambda: icon_coin(64),
        "plus":  lambda: icon_plus(64, fill=primary),
        "minus": lambda: icon_minus(64),
        "check": lambda: icon_check(64, fill=primary),
        "cross": lambda: icon_cross(64),
        "circle": lambda: circle(64, fill=primary),
        "diamond": lambda: diamond(64, fill=primary),
    }
    for name in cfg.get("icons", []):
        if name in icon_map:
            out[f"icon_{name}"] = icon_map[name]()

    for w, h in cfg.get("bars", []):
        out[f"bar_{w}x{h}_bg"] = progress_bar(w, h, 1.0, bg=(60,60,60,255), fill=(60,60,60,255))
        out[f"bar_{w}x{h}_fill"] = progress_bar(w, h, 1.0, bg=primary, fill=primary)

    extras = {
        "checkbox":      lambda: checkbox(32),
        "checkbox_on":   lambda: checkbox(32, checked=True),
        "toggle_on":     lambda: toggle(64, 32, on=True),
        "toggle_off":    lambda: toggle(64, 32, on=False),
        "arrow_right":   lambda: arrow(48, "right"),
        "arrow_left":    lambda: arrow(48, "left"),
        "arrow_up":      lambda: arrow(48, "up"),
        "arrow_down":    lambda: arrow(48, "down"),
        "avatar_circle": lambda: avatar_circle(96),
        "avatar_frame":  lambda: avatar_frame(96),
        "shadow":        lambda: shadow(128, 48),
    }
    for name in cfg.get("extras", []):
        if name in extras:
            out[name] = extras[name]()

    return out