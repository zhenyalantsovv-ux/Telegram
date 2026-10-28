import os
import re
import base64
import io
from pathlib import Path
from PIL import Image

APP_NAME = os.getenv("APP_NAME", "ZapretGram")
ICON_B64 = os.getenv("ICON_B64", "")

STRINGS = Path("TMessagesProj/src/main/res/values/strings.xml")

# 1) Меняем название
content = STRINGS.read_text(encoding="utf-8")
content = re.sub(
    r'<string name="app_name">.*?</string>',
    f'<string name="app_name">{APP_NAME}</string>',
    content,
)
STRINGS.write_text(content, encoding="utf-8")
print(f"✅ Название изменено на: {APP_NAME}")

# 2) Меняем иконки во всех размерах
if ICON_B64:
    img = Image.open(io.BytesIO(base64.b64decode(ICON_B64))).convert("RGBA")
    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, size in sizes.items():
        resized = img.resize((size, size), Image.LANCZOS)
        for name in ("ic_launcher.png", "ic_launcher_round.png"):
            out = Path(f"TMessagesProj/src/main/res/{folder}/{name}")
            out.parent.mkdir(parents=True, exist_ok=True)
            resized.save(out, "PNG")
    print("✅ Иконки заменены")
else:
    print("⚠️ ICON_B64 пустой — иконка не менялась")
