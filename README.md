# uigen — процедурный генератор UI-спрайтов

Инструмент для генерации UI-спрайтов и атласов из JSON-конфига.
На выходе — PNG + JSON-атлас, готовые к импорту.

## Установка

    python3 -m venv .venv
    source .venv/bin/activate
    pip install pillow

## Запуск

    .venv/bin/python cli.py --config ui_config.json --out output

## Формат конфига (ui_config.json)

    {
      "palette": {
        "primary": "#4CAF50",
        "border": "#FFFFFF",
        "accent": "#FFC107"
      },
      "buttons": [[128, 48], [192, 64]],
      "icons": ["heart", "star", "coin", "plus", "check", "cross", "diamond"],
      "bars": [[128, 12], [200, 16]],
      "extras": ["checkbox", "checkbox_on", "toggle_on", "toggle_off",
                 "arrow_right", "arrow_left", "avatar_circle", "avatar_frame", "shadow"]
    }

## Доступные генераторы (generator.py)

### Базовые фигуры
- `rounded_rect(w, h, radius, thickness, fill, border)` — кнопки, панели
- `circle(size, fill, border, thickness)` — круглые иконки
- `star(size, points, fill, border, thickness)` — звёзды
- `heart(size, fill, border, thickness)` — сердца
- `diamond(size, fill, border, thickness)` — ромбы

### Иконки
- `icon_coin(size)` — монета
- `icon_plus(size, fill)` / `icon_minus(size, fill)`
- `icon_check(size, fill)` / `icon_cross(size, fill)`

### Панели и фоны
- `gradient(w, h, top, bottom, horizontal=False)`
- `pattern_stripes(w, h, a, b, stripe, diagonal)`
- `pattern_checker(w, h, a, b, cell)`
- `pattern_dots(w, h, bg, dot_color, spacing, radius)`

### Бары
- `progress_bar(w, h, fill_ratio, bg, fill, radius)`
- `progress_bar_9slice(w, h, bg, fill, radius)`

### Рамки и тени
- `frame(w, h, thickness, color, inner)`
- `frame_ornate(w, h, color, corner)`
- `shadow(w, h, radius, blur, alpha)`

### Аватары
- `avatar_circle(size, fill, border)`
- `avatar_frame(size, color)`

### Контролы
- `checkbox(size, checked, fill, border)`
- `toggle(w, h, on, on_color, off_color)`
- `slider_knob(size, fill, border)`
- `arrow(size, direction, fill)`

### Утилиты
- `hex_to_rgba("#RRGGBB", a=255)` — конвертация цвета
- `build_from_config(cfg)` — собрать весь набор из JSON-конфига

## Цвета

Все цвета — RGBA-кортежи `(r, g, b, a)` или hex-строки `"#RRGGBB"` через `hex_to_rgba`.

## Атлас

`atlas.pack(sprites, out_png, out_json)` — полочная упаковка + JSON:
    {
      "size": [W, H],
      "frames": {
        "name": {"x": ..., "y": ..., "w": ..., "h": ...}
      }
    }

## Как расширять

1. Добавь функцию в `generator.py`. Она должна возвращать `PIL.Image`.
2. Добавь её в `build_from_config` под нужную секцию.
3. Обнови этот README.
4. Запусти `cli.py` — новые спрайты появятся в атласе.

## Инструкция для Aider

Когда пользователь просит новый UI:
1. Прочитай этот README, чтобы знать доступные функции.
2. Задай вопросы: цвета (primary/border/accent), размеры кнопок, нужные иконки, бары, extras.
3. Собери `ui_config.json` из ответов.
4. Запусти `.venv/bin/python cli.py --config ui_config.json --out output`.
5. Если нужной функции нет — добавь её в `generator.py` и обнови README.
