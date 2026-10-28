import os
import re
import io
import base64
from pathlib import Path
from PIL import Image

# ---------- Параметры из формы ----------
APP_NAME = os.getenv("APP_NAME", "ZapretGram")
ICON_B64 = os.getenv("ICON_B64", "")

PROXY_ENABLED = os.getenv("PROXY_ENABLED", "false").lower() == "true"
DISABLE_PROXY_ON_VPN = os.getenv("DISABLE_PROXY_ON_VPN", "false").lower() == "true"
HIDE_PHONE = os.getenv("HIDE_PHONE", "false").lower() == "true"
DISABLE_ADS = os.getenv("DISABLE_ADS", "false").lower() == "true"
GHOST_MODE = os.getenv("GHOST_MODE", "false").lower() == "true"

ROOT = Path(".")

print("=" * 60)
print(f"ZapretGram patch.py запущен")
print(f"APP_NAME = {APP_NAME}")
print(f"PROXY_ENABLED = {PROXY_ENABLED}")
print(f"DISABLE_PROXY_ON_VPN = {DISABLE_PROXY_ON_VPN}")
print(f"HIDE_PHONE = {HIDE_PHONE}")
print(f"DISABLE_ADS = {DISABLE_ADS}")
print(f"GHOST_MODE = {GHOST_MODE}")
print("=" * 60)

# ---------- 1. Название приложения ----------
strings_path = ROOT / "TMessagesProj/src/main/res/values/strings.xml"
if strings_path.exists():
    content = strings_path.read_text(encoding="utf-8")
    content = re.sub(
        r'<string name="app_name">.*?</string>',
        f'<string name="app_name">{APP_NAME}</string>',
        content,
    )
    strings_path.write_text(content, encoding="utf-8")
    print(f"[OK] app_name = {APP_NAME}")
else:
    print(f"[ERROR] не найден {strings_path}")

# ---------- 2. Иконка ----------
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
        folder_path = ROOT / f"TMessagesProj/src/main/res/{folder}"
        folder_path.mkdir(parents=True, exist_ok=True)
        for name in ("ic_launcher.png", "ic_launcher_round.png"):
            out = folder_path / name
            resized.save(out, "PNG")
    print(f"[OK] иконка заменена во всех размерах")
else:
    print("[WARN] ICON_B64 пустой — иконка не менялась")

# ---------- 3. Дополнительные флаги (пока частично) ----------

# Ghost mode — добавляем флаг в BuildVars.
# ВАЖНО: сама логика "не отправлять прочитано" должна быть реализована
# в коде клиента. Этот патч только создаёт переменную-флаг,
# но пока она нигде не используется — сборка пройдёт, но эффекта не будет.
if GHOST_MODE:
    buildvars = ROOT / "TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java"
    if buildvars.exists():
        c = buildvars.read_text(encoding="utf-8")
        if "ZAPRETGRAM_GHOST_MODE" not in c:
            c = c.replace(
                "public class BuildVars {",
                "public class BuildVars {\n"
                "    public static final boolean ZAPRETGRAM_GHOST_MODE = true;",
            )
            buildvars.write_text(c, encoding="utf-8")
            print("[OK] GHOST_MODE флаг добавлен в BuildVars.java (требует доработки логики)")
    else:
        print(f"[WARN] не найден BuildVars.java")

if HIDE_PHONE:
    print("[INFO] HIDE_PHONE: нужна доработка логики приватности в коде клиента")

if DISABLE_ADS:
    print("[INFO] DISABLE_ADS: нужна доработка логики спонсорских каналов")

if PROXY_ENABLED:
    print("[INFO] PROXY_ENABLED: требует полноценной интеграции SOCKS5-прокси.")
    print("       Рекомендуется использовать форк NekoX вместо официального кода.")

if DISABLE_PROXY_ON_VPN:
    print("[INFO] DISABLE_PROXY_ON_VPN: работает только вместе с PROXY_ENABLED")

print("=" * 60)
print("Патчинг завершён успешно")
print("=" * 60)
