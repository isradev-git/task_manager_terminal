"""
Guard: ningún fichero versionado puede contener un bot token de Telegram.

Este repo tuvo un token hardcodeado en telegram_bot.py durante meses y acabó
siendo robado. Este check existe para que no vuelva a pasar.

Uso:  python test_no_secrets.py
"""

import re
import subprocess

# ponytail: solo tokens de Telegram. Si algún día entran claves AWS/OpenAI,
# usa gitleaks en vez de ampliar esta regex a mano.
TELEGRAM_TOKEN = re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return out.splitlines()


def find_secrets():
    hits = []
    for path in tracked_files():
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for n, line in enumerate(f, 1):
                    if TELEGRAM_TOKEN.search(line):
                        hits.append(f"{path}:{n}")
        except (IsADirectoryError, FileNotFoundError):
            continue
    return hits


if __name__ == "__main__":
    # El detector tiene que detectar: token de ejemplo con la forma real.
    assert TELEGRAM_TOKEN.search("1234567890:" + "A" * 35), "regex rota"
    assert not TELEGRAM_TOKEN.search("TU_BOT_TOKEN_DE_BOTFATHER"), "falso positivo"

    hits = find_secrets()
    assert not hits, "Token de Telegram en ficheros versionados:\n  " + "\n  ".join(hits)
    print("OK: sin tokens de Telegram en los ficheros versionados")
