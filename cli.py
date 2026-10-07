# cli.py
import argparse, os, json
from PIL import Image
import generator as gen
import atlas as at

def hex_to_rgba(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="output")
    p.add_argument("--palette", default=None, help="JSON с палитрой")
    args = p.parse_args()

    os.makedirs(f"{args.out}/sprites", exist_ok=True)

    palette = {
        "primary": "#4CAF50",
        "border": "#FFFFFF",
        "accent": "#FFC107",
    }
    if args.palette:
        with open(args.palette) as f:
            palette.update(json.load(f))

    fill = hex_to_rgba(palette["primary"])
    border = hex_to_rgba(palette["border"])

    sprites = {}

    # Кнопки разных размеров
    for w, h in [(128, 48), (192, 64), (256, 80)]:
        sprites[f"btn_{w}x{h}"] = gen.rounded_rect(w, h, 12, 2, fill, border)

    # Иконки
    sprites["icon_circle"] = gen.icon_circle(64, fill, border, 3)

    # Градиент-панель
    sprites["panel_gradient"] = gen.gradient(
        256, 128, hex_to_rgba(palette["primary"]), hex_to_rgba(palette["accent"])
    )

    # Тень
    sprites["shadow"] = gen.shadow(128, 48, 12)

    # Сохраняем отдельные PNG
    for name, img in sprites.items():
        img.save(f"{args.out}/sprites/{name}.png")

    # Атлас
    at.pack(sprites, f"{args.out}/atlas.png", f"{args.out}/atlas.json")
    print(f"Готово: {args.out}/atlas.png + atlas.json")

if __name__ == "__main__":
    main()